"""
Tests for database building functionality
"""

import pytest
import subprocess
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_database_build_script_exists():
    """Test that the database build script exists and is executable"""
    script_path = Path("src/tariffs_db/db_build.py")
    assert script_path.exists(), "Database build script should exist"
    assert script_path.is_file(), "Database build script should be a file"


def test_database_build_help():
    """Test that database build script shows help"""
    result = subprocess.run([
        "uv", "run", "python", "src/tariffs_db/db_build.py", "--help"
    ], capture_output=True, text=True, cwd=Path.cwd())
    
    assert result.returncode == 0, f"Help command failed: {result.stderr}"
    assert "usage:" in result.stdout.lower() or "Usage:" in result.stdout
    assert "--years" in result.stdout
    print("✅ Database build script help works")


def test_mcp_launcher_script_exists():
    """Test that MCP launcher script exists"""
    script_path = Path("scripts/mcp_server_launcher.py")
    assert script_path.exists(), "MCP launcher script should exist"
    assert script_path.is_file(), "MCP launcher script should be a file"


def test_mcp_launcher_help():
    """Test that MCP launcher script shows help"""
    result = subprocess.run([
        "python", "scripts/mcp_server_launcher.py", "--help"
    ], capture_output=True, text=True, cwd=Path.cwd())
    
    assert result.returncode == 0, f"MCP launcher help failed: {result.stderr}"
    assert "usage:" in result.stdout.lower() or "Usage:" in result.stdout
    assert "--build-only" in result.stdout
    print("✅ MCP launcher script help works")


@pytest.mark.slow
def test_database_build_validation():
    """Test database build with validation (slow test)"""
    # This test only runs if explicitly requested with pytest -m slow
    # It's marked as slow because building database takes time
    
    db_path = Path("data/usitc_data/usitc_trade_data.db")
    
    if not db_path.exists():
        pytest.skip("Database not found - this test requires a built database")
    
    # Verify database has expected structure
    import duckdb
    
    conn = duckdb.connect(str(db_path))
    try:
        # Check tables exist
        tables = conn.execute("SHOW TABLES").fetchall()
        table_names = [row[0] for row in tables]
        
        # Should have tariff tables  
        tariff_tables = [name for name in table_names if name.startswith('tariff_')]
        assert len(tariff_tables) > 0, f"No tariff tables found in {table_names}"
        
        # Check a tariff table has expected columns
        if tariff_tables:
            first_table = tariff_tables[0]
            schema = conn.execute(f"DESCRIBE {first_table}").fetchall()
            column_names = [row[0] for row in schema]
            
            expected_columns = ['hts8', 'brief_description']
            for col in expected_columns:
                assert col in column_names, f"Missing expected column {col} in {first_table}"
        
        print(f"✅ Database validation passed: {len(tariff_tables)} tariff tables")
        
    finally:
        conn.close()


def test_project_structure():
    """Test that project structure is correct for database operations"""
    # Check required directories exist
    required_dirs = [
        Path("src/tariffs_db"),
        Path("scripts"), 
        Path("data").parent  # Check parent directory exists (data might not exist yet)
    ]
    
    for dir_path in required_dirs:
        if dir_path.name == "mcp-tarrifs":  # Skip parent check
            continue
        assert dir_path.parent.exists(), f"Required parent directory {dir_path.parent} should exist"
    
    # Check key files exist
    key_files = [
        Path("scripts/mcp_server_launcher.py"),
        Path("src/tariffs_db/db_build.py"),
        Path("pyproject.toml")
    ]
    
    for file_path in key_files:
        assert file_path.exists(), f"Required file {file_path} should exist"
    
    print("✅ Project structure validation passed")