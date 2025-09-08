"""
Tests for tariffs plugin functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server.plugins.tariffs import TariffsPlugin


@pytest.mark.asyncio
async def test_tariffs_plugin_initialization():
    """Test tariffs plugin initializes correctly"""
    plugin = TariffsPlugin()
    assert plugin.name == 'tariffs'
    assert plugin.description is not None
    assert len(plugin.description) > 0


@pytest.mark.asyncio
async def test_tariffs_plugin_tools():
    """Test tariffs plugin provides expected tools"""
    plugin = TariffsPlugin()
    tools = plugin.get_specialized_tools()
    
    tool_names = [tool.name for tool in tools]
    expected_tools = ['get_tariff_rates', 'compare_tariff_rates']
    
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Missing tool: {expected_tool}"
    
    print(f"Tariffs plugin tools: {tool_names}")


@pytest.mark.asyncio
async def test_tariffs_plugin_prompts():
    """Test tariffs plugin provides analysis prompts"""
    plugin = TariffsPlugin()
    prompts = plugin.get_prompts()
    
    assert len(prompts) > 0
    prompt_names = [prompt.name for prompt in prompts]
    
    # Should have analysis guidance prompts
    expected_prompts = ['tariff-analysis-guide', 'hts-code-lookup']
    for expected_prompt in expected_prompts:
        assert expected_prompt in prompt_names, f"Missing prompt: {expected_prompt}"
    
    print(f"Tariffs plugin prompts: {prompt_names}")


@pytest.mark.asyncio
async def test_get_tariff_rates_tool(db_client):
    """Test get_tariff_rates tool functionality"""
    plugin = TariffsPlugin()
    
    # Test with product search
    arguments = {
        "product_search": "beef",
        "year": 2024
    }
    
    result = await plugin._handle_get_tariff_rates(arguments, db_client)
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Should return content with tariff information
    content_text = result[0].text
    assert isinstance(content_text, str)
    assert len(content_text) > 0
    print(f"Tariff rates result (first 200 chars): {content_text[:200]}...")


@pytest.mark.asyncio
async def test_get_tariff_rates_with_hts_code(db_client):
    """Test get_tariff_rates with HTS code"""
    plugin = TariffsPlugin()
    
    # Test with HTS code - use one that exists (from our sample above)
    arguments = {
        "product_code": "1012",  # Should match codes starting with 1012
        "year": 2024
    }
    
    result = await plugin._handle_get_tariff_rates(arguments, db_client)
    assert isinstance(result, list)
    assert len(result) > 0
    
    content_text = result[0].text
    # Should either find the code or show it ran the query successfully  
    assert "1012" in content_text or "query executed successfully" in content_text.lower()
    print(f"HTS code search result: {content_text[:200]}...")


@pytest.mark.asyncio
async def test_compare_tariff_rates_tool(db_client):
    """Test compare_tariff_rates tool functionality"""
    plugin = TariffsPlugin()
    
    # Test comparing rates across years - use existing HTS code
    arguments = {
        "product_code": "1012",
        "years": [2023, 2024]
    }
    
    result = await plugin._handle_compare_tariff_rates(arguments, db_client)
    assert isinstance(result, list)
    assert len(result) > 0
    
    content_text = result[0].text
    assert isinstance(content_text, str)
    assert len(content_text) > 0
    
    # Should mention the years or run successfully
    years_mentioned = "2023" in content_text and "2024" in content_text
    query_successful = "query executed successfully" in content_text.lower()
    assert years_mentioned or query_successful, f"Expected years or success message, got: {content_text[:100]}"
    print(f"Compare rates result: {content_text[:200]}...")


@pytest.mark.asyncio 
async def test_tariffs_plugin_error_handling(db_client):
    """Test tariffs plugin handles errors gracefully"""
    plugin = TariffsPlugin()
    
    # Test with invalid arguments
    arguments = {
        "product_search": "",  # Empty search
        "year": 2024
    }
    
    result = await plugin._handle_get_tariff_rates(arguments, db_client)
    assert isinstance(result, list)
    
    # Should handle gracefully, not crash
    if len(result) > 0:
        content_text = result[0].text
        # Either returns data or explains the issue
        assert isinstance(content_text, str)
        print(f"Error handling result: {content_text[:100]}...")
    
    # Test with non-existent year
    arguments = {
        "product_search": "beef", 
        "year": 1999  # Should not exist
    }
    
    result = await plugin._handle_get_tariff_rates(arguments, db_client)
    assert isinstance(result, list)
    print("Error handling test completed successfully")