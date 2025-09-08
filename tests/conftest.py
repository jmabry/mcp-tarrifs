"""
Pytest configuration and shared fixtures for MCP Tariffs Server tests
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server.server import MCPUnifiedServer
from mcp_server.core.database_client import UniversalDatabaseClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db_path():
    """Provide path to the real test database"""
    db_path = Path("data/usitc_data/usitc_trade_data.db")
    if db_path.exists():
        return str(db_path)
    else:
        pytest.skip("Database not found. Run: python scripts/mcp_server_launcher.py --build-only")


@pytest.fixture
def temp_logs_dir():
    """Create a temporary logs directory for testing"""
    temp_dir = tempfile.mkdtemp()
    logs_dir = Path(temp_dir) / "logs"
    logs_dir.mkdir(exist_ok=True)
    yield str(logs_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
async def db_client(test_db_path):
    """Create a database client connected to the test database"""
    client = UniversalDatabaseClient(
        db_path=test_db_path,
        read_only=True
    )
    await client.connect()
    yield client
    if hasattr(client, 'close') and callable(client.close):
        try:
            await client.close()
        except:
            pass  # Ignore cleanup errors


@pytest.fixture
async def mcp_server():
    """Create and initialize an MCP server instance"""
    # Set environment variables for server
    os.environ['DB_PATH'] = str(Path("data/usitc_data/usitc_trade_data.db"))
    os.environ['READ_ONLY'] = 'true'
    
    server = MCPUnifiedServer()
    await server.initialize()
    yield server
    
    # Cleanup
    if hasattr(server.db_client, 'close') and callable(server.db_client.close):
        try:
            await server.db_client.close()
        except:
            pass  # Ignore cleanup errors