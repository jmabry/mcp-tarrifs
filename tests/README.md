# MCP Tariffs Server - Test Suite

A comprehensive test suite covering all major components and end-to-end workflows of the MCP Tariffs Server.

## Test Structure

The test suite is organized into logical modules covering different aspects of the system:

### Core Tests
- **`test_database.py`** - Database connectivity, schema validation, and data operations
- **`test_server.py`** - MCP server initialization, plugin loading, and configuration
- **`test_tariffs_plugin.py`** - Tariff-specific tools and analysis functionality
- **`test_database_build.py`** - Database build scripts and project structure validation

### End-to-End Tests  
- **`test_end_to_end.py`** - Complete workflows from server startup through tariff analysis

### Configuration
- **`conftest.py`** - Shared pytest fixtures and test configuration
- **`README.md`** - This file

## Test Coverage

The test suite covers these important flows:

### 1. Database Operations
- ✅ Database connectivity and table listing
- ✅ Schema validation and structure verification  
- ✅ Sample data retrieval and query execution
- ✅ Tariff data structure validation (multi-year, HTS codes)

### 2. Server Functionality
- ✅ MCP server initialization and plugin loading
- ✅ Environment configuration (DB_PATH, READ_ONLY)
- ✅ Tool registration and availability
- ✅ Logging setup and configuration

### 3. Tariff Analysis Tools
- ✅ Product search by description (`get_tariff_rates`)
- ✅ HTS code lookup (`get_tariff_rates` with product_code)
- ✅ Multi-year rate comparisons (`compare_tariff_rates`)
- ✅ Analysis prompts and guidance tools
- ✅ Error handling and edge cases

### 4. End-to-End Workflows
- ✅ Complete server startup → tool execution workflow
- ✅ Multi-year tariff analysis workflow
- ✅ Database exploration workflow (tables → schema → data → queries)
- ✅ HTS code lookup and validation workflow
- ✅ Error recovery and graceful degradation

### 5. Infrastructure
- ✅ Database build script validation
- ✅ MCP launcher script functionality
- ✅ Project structure and file organization

## Running Tests

### Prerequisites

1. **Database Required**: Most tests require the tariff database to be built:
   ```bash
   python scripts/mcp_server_launcher.py --build-only
   ```

2. **Install Test Dependencies**:
   ```bash
   uv add --dev pytest pytest-asyncio pytest-cov
   ```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_database.py
pytest tests/test_end_to_end.py

# Run tests with coverage report
pytest --cov=src --cov-report=html

# Run only fast tests (excludes slow database build tests)
pytest -m "not slow"
```

### Advanced Test Options

```bash
# Run slow tests (includes database build validation)  
pytest -m slow

# Run tests matching a pattern
pytest -k "tariff" 
pytest -k "e2e"

# Stop after first failure
pytest -x

# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto
```

### Individual Test Categories

```bash
# Database and connectivity tests
pytest tests/test_database.py -v

# Server functionality tests  
pytest tests/test_server.py -v

# Tariff plugin tests
pytest tests/test_tariffs_plugin.py -v

# End-to-end workflow tests
pytest tests/test_end_to_end.py -v

# Infrastructure tests
pytest tests/test_database_build.py -v
```

## Test Output Examples

### Successful Test Run
```
tests/test_database.py::test_database_connection PASSED
tests/test_server.py::test_server_initialization PASSED  
tests/test_tariffs_plugin.py::test_get_tariff_rates_tool PASSED
tests/test_end_to_end.py::test_e2e_server_startup_and_tool_execution PASSED

✅ All critical workflows verified
```

### Expected Test Output Features
- **Database validation**: Confirms tables and HTS codes exist
- **Plugin verification**: Checks tariff analysis tools work correctly  
- **E2E workflow validation**: Tests complete user scenarios
- **Error handling**: Verifies graceful failure modes

## Adding New Tests

### Test Organization Principles
1. **Logical grouping** - Group related functionality together
2. **Clear naming** - Use descriptive test names that explain what's being tested
3. **Proper fixtures** - Use shared fixtures from `conftest.py`
4. **Async support** - Mark async tests with `@pytest.mark.asyncio`

### Example Test Structure

```python
@pytest.mark.asyncio
async def test_new_functionality(mcp_server, db_client):
    """Test description explaining what this validates"""
    
    # Arrange
    expected_result = "some value"
    
    # Act  
    result = await some_function(mcp_server, db_client)
    
    # Assert
    assert result == expected_result
    print(f"✅ Test passed: {result}")
```

### Test Categories
- **Unit tests** - Individual component functionality
- **Integration tests** - Component interaction validation
- **End-to-end tests** - Complete user workflow verification
- **Performance tests** - Response time and resource usage (if needed)

## Troubleshooting Tests

### Common Issues

**"Database not found"**:
```bash
# Build the database first
python scripts/mcp_server_launcher.py --build-only
```

**"Module not found"**:
```bash
# Install dependencies
uv sync
uv add --dev pytest pytest-asyncio pytest-cov
```

**"Tests hang or timeout"**:  
- Check database connectivity
- Ensure no other processes are using the database
- Verify MCP server isn't running elsewhere

**"Async warnings"**:
- Tests properly use `@pytest.mark.asyncio`  
- Event loop fixture in `conftest.py` handles async lifecycle

### Debug Mode
```bash
# Run tests with debug output
pytest -s -v --tb=long

# Run single test with maximum detail
pytest tests/test_end_to_end.py::test_e2e_server_startup_and_tool_execution -s -v --tb=long
```

## Continuous Integration

This test suite is designed to work in CI environments:

- **Fast by default** - Most tests complete in seconds
- **Database dependency** - Build database once, use for all tests
- **Isolated execution** - Tests don't interfere with each other  
- **Clear success/failure** - Explicit assertions and helpful error messages

### CI Configuration Example
```yaml
- name: Build database
  run: python scripts/mcp_server_launcher.py --build-only

- name: Run tests  
  run: pytest --cov=src --cov-report=xml

- name: Upload coverage
  # Upload coverage reports...
```

---

**🎯 Goal**: This test suite ensures the MCP Tariffs Server works reliably for users querying 11 years of US tariff data through AI assistants and IDEs.