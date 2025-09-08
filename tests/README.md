# MCP Tariffs Server Tests

Comprehensive test suite for the MCP Tariffs Server covering database operations, server functionality, and end-to-end workflows.

## Test Files

- **`test_mcp_functional.py`** - Main test suite (22 tests)
  - Input validation and error handling
  - Tool functionality (get_tariff_rates, compare_tariff_rates, query_database)  
  - End-to-end user workflows
- **`test_database.py`** - Database connectivity and schema validation (6 tests)
- **`test_server.py`** - MCP server initialization and configuration (5 tests)
- **`test_database_build.py`** - Build scripts and project structure (6 tests)

## Running Tests

```bash
# All tests (39 total)
pytest

# Main functional tests (recommended)
pytest tests/test_mcp_functional.py -v

# Specific categories
pytest tests/test_database.py -v      # Database tests
pytest tests/test_server.py -v        # Server tests

# Integration workflows only
pytest tests/test_mcp_functional.py -m integration -v

# With coverage
pytest --cov=src --cov-report=html
```

## Prerequisites

Most tests require the tariff database:
```bash
python scripts/mcp_server_launcher.py --build-only
```

## What's Tested

**✅ Input Validation (8 tests)**
- Valid/invalid HTS codes and product searches
- Missing parameters and empty strings
- Error handling and edge cases

**✅ Tool Functionality (11 tests)** 
- `get_tariff_rates` - Product/HTS lookups
- `compare_tariff_rates` - Multi-year comparisons
- `query_database` - SQL execution

**✅ User Workflows (3 tests)**
- Beginner: Finding car tariff rates
- Researcher: Multi-year trend analysis  
- Business: Import cost calculations

**✅ Core Components (17 tests)**
- Database connectivity and schema
- Server initialization and plugins
- Build scripts and project structure

## Examples

```python
# Valid inputs
{"product_code": "87036000", "year": 2024}
{"product_search": "automobiles", "year": 2024}

# Invalid inputs (properly handled)  
{"product_search": "", "year": 2024}    # Empty string → validation error
{"year": 2024}                          # Missing params → validation error
```

## MCP Inspector Testing (Optional)

Interactive testing with MCP Inspector:
```bash
npx @modelcontextprotocol/inspector

# Connect using:
# Command: uv
# Args: ["run", "python", "scripts/mcp_server_launcher.py"]  
```

## Troubleshooting

**Database not found:** `python scripts/mcp_server_launcher.py --build-only`  
**Import errors:** Ensure running from project root  
**Test failures:** Verify database contains expected HTS codes for 2022-2024