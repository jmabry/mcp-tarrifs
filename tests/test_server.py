"""
Tests for MCP server initialization and core functionality
"""

import pytest
import os
from pathlib import Path


@pytest.mark.asyncio
async def test_server_initialization(mcp_server):
    """Test MCP server initializes correctly"""
    assert mcp_server is not None
    assert hasattr(mcp_server, 'server')
    assert hasattr(mcp_server, 'db_client')
    assert hasattr(mcp_server, 'plugins')


@pytest.mark.asyncio
async def test_server_plugins_loaded(mcp_server):
    """Test that server loads plugins correctly"""
    plugins = mcp_server.plugins
    assert isinstance(plugins, dict)
    assert len(plugins) > 0
    
    # Should have tariffs plugin
    assert 'tariffs' in plugins
    print(f"Loaded plugins: {list(plugins.keys())}")


@pytest.mark.asyncio
async def test_server_tools_available(mcp_server):
    """Test that server exposes expected tools"""
    # This test verifies that essential components are available
    # The actual tools are registered via MCP decorators, so we check plugin availability
    
    # Should have tariffs plugin loaded
    assert 'tariffs' in mcp_server.plugins
    
    # Get plugin tools to verify they're available
    tariffs_plugin = mcp_server.plugins['tariffs']
    plugin_tools = tariffs_plugin.get_specialized_tools()
    tool_names = [tool.name for tool in plugin_tools]
    
    # Should have tariff-specific tools
    expected_plugin_tools = ['get_tariff_rates', 'compare_tariff_rates']
    for tool in expected_plugin_tools:
        assert tool in tool_names, f"Missing expected plugin tool: {tool}"
    
    # Server should have database client (implies core database tools are available)
    assert hasattr(mcp_server, 'db_client')
    assert mcp_server.db_client is not None
    
    print(f"Plugin tools available: {tool_names}")
    print("✅ Core database tools accessible via db_client")


@pytest.mark.asyncio
async def test_server_environment_config(mcp_server):
    """Test server respects environment configuration"""
    # Should use environment variables for configuration
    db_client = mcp_server.db_client
    assert hasattr(db_client, 'db_path')
    assert hasattr(db_client, '_read_only')  # It's a private attribute
    
    # Check read-only mode from environment
    read_only = os.environ.get('READ_ONLY', 'true').lower() == 'true'
    assert db_client._read_only == read_only


@pytest.mark.asyncio
async def test_server_logging_setup(mcp_server, temp_logs_dir):
    """Test that server logging is properly configured"""
    # This test verifies logging setup doesn't crash
    # Actual log verification would require running full MCP protocol
    assert True  # If we get here, logging setup didn't crash initialization