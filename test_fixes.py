#!/usr/bin/env python3
"""
Test the fixed MCP tariff tools
"""

import asyncio
import sys
import json
sys.path.append('src')

from mcp_server.core.database_client import UniversalDatabaseClient
from mcp_server.plugins.tariffs import TariffsPlugin

async def test_fixed_tools():
    """Test the fixed MCP tools"""
    
    # Initialize database client
    db_client = UniversalDatabaseClient(
        db_path='data/usitc_data/usitc_trade_data.db', 
        read_only=True
    )
    await db_client.connect()
    
    # Initialize tariffs plugin
    plugin = TariffsPlugin()
    
    print("=" * 80)
    print("TESTING FIXED MCP TOOLS")
    print("=" * 80)
    
    # Test 1: Original pork sausage query (should still work)
    print("\n1. Original Query - Pork Sausage 2024")
    print("-" * 50)
    try:
        result = await plugin._handle_get_tariff_rates({
            "product_search": "pork sausage",
            "year": 2024
        }, db_client)
        print("✅ SUCCESS:")
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 2: HTS Code search (previously broken)
    print("\n\n2. HTS Code Search - Live Horses (Previously Broken)")
    print("-" * 50)
    try:
        result = await plugin._handle_get_tariff_rates({
            "product_code": "0101.21",
            "year": 2024
        }, db_client)
        print("✅ SUCCESS:")
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 3: Compare rates (previously broken)
    print("\n\n3. Compare Tariff Rates (Previously Broken)")
    print("-" * 50)
    try:
        result = await plugin._handle_compare_tariff_rates({
            "product_code": "16010020",  # Pork sausage HTS code
            "years": [2022, 2023, 2024]
        }, db_client)
        print("✅ SUCCESS:")
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 4: Country filtering (should be ignored for now)
    print("\n\n4. Country Filtering (Should Be Ignored)")
    print("-" * 50)
    try:
        result = await plugin._handle_get_tariff_rates({
            "product_search": "beef",
            "country": "Canada",  # This should be ignored
            "year": 2024
        }, db_client)
        print("✅ SUCCESS (country filtering ignored):")
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Close connection
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    
    if hasattr(db_client, 'close') and callable(db_client.close):
        try:
            await db_client.close()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_fixed_tools())
