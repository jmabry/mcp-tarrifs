# USITC Tariff Data MCP Server

Query 11 years of US tariff data through AI assistants using MCP (Model Context Protocol).

## Quick Start

1. **Build database:**
   ```bash
   python scripts/mcp_server_launcher.py --build-only
   ```

2. **Configure your MCP client** (Claude, Cursor, etc.):
   ```json
   {
     "name": "usitc-tariffs",
     "command": "uv", 
     "args": ["run", "python", "scripts/mcp_server_launcher.py"],
     "env": {}
   }
   ```

3. **Query tariff data:**
   - "What's the tariff rate for cars from Germany?"
   - "Compare steel tariff rates over the past 3 years"
   - "Show me HTS codes for electronics"

## Available Tools

- **get_tariff_rates** - Find tariff rates by HTS code or product search
- **compare_tariff_rates** - Compare rates across multiple years
- **query_database** - Direct SQL queries on tariff database

## Data Coverage

- **Years**: 2015-2024 (11 years)
- **Records**: 142K+ tariff entries
- **Source**: USITC Annual Tariff Database
- **Database**: DuckDB (local file)

## Development

```bash
# Run tests
pytest

# Start development server
python scripts/mcp_server_launcher.py

# Build database with specific years
python src/tariffs_db/db_build.py --years 5
```

## Client Configuration Examples

### Claude Desktop
```json
{
  "mcpServers": {
    "usitc-tariffs": {
      "command": "uv",
      "args": ["run", "python", "scripts/mcp_server_launcher.py"],
      "cwd": "/path/to/mcp-tarrifs"
    }
  }
}
```

### Cursor
```json
{
  "name": "usitc-tariffs",
  "command": "uv",
  "args": ["run", "python", "scripts/mcp_server_launcher.py"]
}
```

## Requirements

- Python 3.8+
- uv (recommended) or pip
- ~2GB disk space for database

## License

MIT