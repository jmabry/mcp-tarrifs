#!/usr/bin/env python3
"""
Comprehensive test script for MCP tariff tools
Shows different ways to query tariff data using the MCP server tools
"""

import asyncio
import sys
import json
sys.path.append('src')

from mcp_server.core.database_client import UniversalDatabaseClient
from mcp_server.plugins.tariffs import TariffsPlugin

async def test_multiple_queries():
    """Test various MCP tool queries"""
    
    # Initialize database client
    db_client = UniversalDatabaseClient(
        db_path='data/usitc_data/usitc_trade_data.db', 
        read_only=True
    )
    await db_client.connect()
    
    # Initialize tariffs plugin
    plugin = TariffsPlugin()
    
    # Test cases
    test_cases = [
        {
            "name": "Your Original Query - Pork Sausage 2024",
            "tool": "get_tariff_rates",
            "params": {
                "country": None,
                "product_code": None,
                "product_search": "pork sausage",
                "year": 2024
            }
        },
        {
            "name": "Search by HTS Code - Live Horses",
            "tool": "get_tariff_rates", 
            "params": {
                "product_code": "0101.21",
                "year": 2024
            }
        },
        {
            "name": "Search for Automobiles",
            "tool": "get_tariff_rates",
            "params": {
                "product_search": "automobiles",
                "year": 2024
            }
        },
        {
            "name": "Search with Country Filter - Beef from Canada",
            "tool": "get_tariff_rates",
            "params": {
                "product_search": "beef",
                "country": "Canada",
                "year": 2024
            }
        },
        {
            "name": "Compare Tariff Rates Across Years - HTS 0101.21.00",
            "tool": "compare_tariff_rates",
            "params": {
                "product_code": "0101.21.00",
                "years": [2022, 2023, 2024]
            }
        }
    ]
    
    print("=" * 80)
    print("MCP TARIFF TOOL TESTING")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 60)
        print(f"Tool: {test_case['tool']}")
        print(f"Parameters: {json.dumps(test_case['params'], indent=2)}")
        print("-" * 60)
        
        try:
            if test_case['tool'] == 'get_tariff_rates':
                result = await plugin._handle_get_tariff_rates(test_case['params'], db_client)
            elif test_case['tool'] == 'compare_tariff_rates':
                result = await plugin._handle_compare_tariff_rates(test_case['params'], db_client)
            
            print("RESULT:")
            for content in result:
                print(content.text)
                
        except Exception as e:
            print(f"ERROR: {e}")
        
        print("\n" + "="*80)
    
    # Close connection
    if hasattr(db_client, 'close') and callable(db_client.close):
        try:
            await db_client.close()
        except:
            pass

async def show_available_tools():
    """Show all available MCP tools"""
    plugin = TariffsPlugin()
    tools = plugin.get_specialized_tools()
    
    print("\n📋 AVAILABLE MCP TOOLS:")
    print("=" * 50)
    
    for tool in tools:
        print(f"\n🔧 Tool: {tool.name}")
        print(f"Description: {tool.description}")
        print("Parameters:")
        if 'properties' in tool.inputSchema:
            for param, details in tool.inputSchema['properties'].items():
                required = param in tool.inputSchema.get('required', [])
                req_str = " (required)" if required else " (optional)"
                print(f"  - {param}: {details.get('type', 'unknown')}{req_str}")
                print(f"    {details.get('description', 'No description')}")
        print("-" * 50)

if __name__ == "__main__":
    print("MCP Tariff Tools Test Suite")
    print("This script shows how to make test queries like the one you requested.")
    
    # Show available tools first
    asyncio.run(show_available_tools())
    
    # Run test queries
    asyncio.run(test_multiple_queries())
