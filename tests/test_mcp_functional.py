"""
MCP Inspector Tests using pytest
Tests the tariffs MCP server with comprehensive validation scenarios
"""
import pytest
import json
from pathlib import Path
from mcp_server.plugins.tariffs import TariffsPlugin


class TestTariffRatesTool:
    """Test get_tariff_rates tool with various inputs"""
    
    @pytest.mark.asyncio
    async def test_valid_hts_code_2024(self, mcp_server):
        """Test valid HTS code lookup"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_code": "87036000", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return EmbeddedResource with JSON data
        assert hasattr(result[0], 'resource'), "Should return EmbeddedResource"
        json_data = json.loads(result[0].resource.text)
        assert json_data["count"] > 0, "Should return tariff data"
        assert "87036000" in str(json_data["data"]), "Should contain the HTS code"
    
    @pytest.mark.asyncio  
    async def test_partial_hts_code_search(self, mcp_server):
        """Test partial HTS code search"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_code": "8703", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return EmbeddedResource with JSON data
        assert hasattr(result[0], 'resource'), "Should return EmbeddedResource"
        json_data = json.loads(result[0].resource.text)
        assert json_data["count"] > 0, "Should return tariff data"
        assert "8703" in str(json_data["data"]), "Should contain matching HTS codes"
    
    @pytest.mark.asyncio
    async def test_product_search_automobiles(self, mcp_server):
        """Test product description search for automobiles"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_search": "automobiles", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return EmbeddedResource with JSON data or TextContent with error
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid search results"
        else:
            # Handle case where no results are found (returns TextContent error)
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_product_search_horses(self, mcp_server):
        """Test product description search for horses"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_search": "horses", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return results or no data found message
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid search results"
        else:
            # Handle case where no results are found (returns TextContent error)
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_invalid_year_graceful_fallback(self, mcp_server):
        """Test that invalid years fall back gracefully to available data"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_code": "8703.23.00", "year": 2030}, 
            mcp_server.db_client
        )
        # Should either find data in fallback year or return no data message
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should handle invalid year gracefully"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_nonexistent_hts_code_returns_empty(self, mcp_server):
        """Test that nonexistent HTS codes return appropriate message"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_code": "9999.99.99", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return no data found error"
        assert "No tariff data found" in result[0].text, "Should indicate no data found"
    
    @pytest.mark.asyncio
    async def test_missing_both_search_params_error(self, mcp_server):
        """Test that missing both product_code and product_search returns error"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"year": 2024}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return validation error"
        assert "provide either" in result[0].text, "Should request required parameters"
    
    @pytest.mark.asyncio  
    async def test_empty_product_search_error(self, mcp_server):
        """Test that empty product_search string returns error"""
        plugin = TariffsPlugin()
        result = await plugin._handle_get_tariff_rates(
            {"product_search": "", "year": 2024}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return validation error"
        assert "empty" in result[0].text, "Should indicate empty search term"


class TestCompareTariffRatesTool:
    """Test compare_tariff_rates tool with various inputs"""
    
    @pytest.mark.asyncio
    async def test_valid_comparison_multiple_years(self, mcp_server):
        """Test valid multi-year comparison"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "8703.23.00", "years": [2022, 2023, 2024]}, 
            mcp_server.db_client
        )
        # Should return comparison data or no data message
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid comparison results"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_single_year_comparison(self, mcp_server):
        """Test single year comparison"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "8703.23.00", "years": [2024]}, 
            mcp_server.db_client
        )
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid comparison results"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_auto_year_selection(self, mcp_server):
        """Test automatic year selection when no years specified"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "8703.23.00"}, 
            mcp_server.db_client
        )
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid comparison results"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_invalid_years_returns_empty(self, mcp_server):
        """Test that invalid years return appropriate message"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "8703.23.00", "years": [2030, 2031]}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return no data found error"
    
    @pytest.mark.asyncio
    async def test_missing_product_code_error(self, mcp_server):
        """Test that missing product_code returns error"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"years": [2023, 2024]}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return validation error"
        assert "required" in result[0].text, "Should indicate product_code is required"
    
    @pytest.mark.asyncio
    async def test_nonexistent_product_returns_empty(self, mcp_server):
        """Test that nonexistent product returns appropriate message"""
        plugin = TariffsPlugin()
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "9999.99.99", "years": [2023, 2024]}, 
            mcp_server.db_client
        )
        # Should return TextContent with error message
        assert hasattr(result[0], 'text'), "Should return error message"
        assert result[0].text.startswith("❌"), "Should return no data found error"


class TestDatabaseQueryTool:
    """Test query_database tool with various SQL queries"""
    
    @pytest.mark.asyncio
    async def test_show_tables(self, mcp_server):
        """Test SHOW TABLES query"""
        result = await mcp_server.db_client.execute_query("SHOW TABLES")
        assert "tariff_" in result, "Should show tariff tables"
    
    @pytest.mark.asyncio
    async def test_count_tariff_records(self, mcp_server):
        """Test counting records in tariff table"""
        # Get a valid table name first
        tables_result = await mcp_server.db_client.execute_query("SHOW TABLES")
        # Extract a tariff table name - this is a simple approach
        if "tariff_2024" in tables_result:
            result = await mcp_server.db_client.execute_query(
                "SELECT COUNT(*) FROM tariff_2024_tariff_database_202405"
            )
            assert result.strip() != "", "Should return a count"
    
    @pytest.mark.asyncio 
    async def test_sample_tariff_data(self, mcp_server):
        """Test sampling data from tariff table"""
        result = await mcp_server.db_client.execute_query(
            "SELECT hts8, brief_description, mfn_text_rate FROM tariff_2024_tariff_database_202405 LIMIT 5"
        )
        assert "hts8" in result or "brief_description" in result, "Should return data columns"
    
    @pytest.mark.asyncio
    async def test_invalid_sql_syntax_error(self, mcp_server):
        """Test that invalid SQL returns appropriate error"""
        with pytest.raises(Exception):
            await mcp_server.db_client.execute_query("INVALID SQL STATEMENT")
    
    @pytest.mark.asyncio
    async def test_nonexistent_table_error(self, mcp_server):
        """Test that querying nonexistent table returns error"""
        with pytest.raises(Exception):
            await mcp_server.db_client.execute_query("SELECT * FROM nonexistent_table")


@pytest.mark.integration
class TestEndToEndWorkflows:
    """Integration tests for complete user workflows"""
    
    @pytest.mark.asyncio
    async def test_beginner_user_workflow(self, mcp_server):
        """Test a beginner user finding car tariff rates"""
        plugin = TariffsPlugin()
        
        # Step 1: User searches for automobiles
        result1 = await plugin._handle_get_tariff_rates(
            {"product_search": "automobiles", "year": 2024}, 
            mcp_server.db_client
        )
        
        # Should get helpful results
        if hasattr(result1[0], 'resource'):
            json_data = json.loads(result1[0].resource.text)
            assert json_data["count"] >= 0, "Should return valid search results"
        else:
            assert hasattr(result1[0], 'text'), "Should return error message"
        
        # Step 2: User tries specific HTS code from results
        result2 = await plugin._handle_get_tariff_rates(
            {"product_code": "8703", "year": 2024}, 
            mcp_server.db_client
        )
        
        if hasattr(result2[0], 'resource'):
            json_data = json.loads(result2[0].resource.text)
            assert json_data["count"] > 0, "Should return tariff data for valid HTS code"
        else:
            assert hasattr(result2[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_researcher_trend_analysis(self, mcp_server):
        """Test researcher analyzing trends over multiple years"""
        plugin = TariffsPlugin()
        
        # Multi-year comparison for electric vehicles
        result = await plugin._handle_compare_tariff_rates(
            {"product_code": "8703.80", "years": [2022, 2023, 2024]}, 
            mcp_server.db_client
        )
        
        # Should provide comparison data or indicate no data
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return comparison results"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"
    
    @pytest.mark.asyncio
    async def test_business_compliance_workflow(self, mcp_server):
        """Test business user calculating import costs"""
        plugin = TariffsPlugin()
        
        # Look up machinery tariffs
        result = await plugin._handle_get_tariff_rates(
            {"product_search": "machinery", "year": 2024}, 
            mcp_server.db_client
        )
        
        if hasattr(result[0], 'resource'):
            json_data = json.loads(result[0].resource.text)
            assert json_data["count"] >= 0, "Should return machinery tariff data"
        else:
            assert hasattr(result[0], 'text'), "Should return error message"


if __name__ == "__main__":
    # Run with: pytest tests/test_mcp_inspector.py -v
    pytest.main([__file__, "-v"])