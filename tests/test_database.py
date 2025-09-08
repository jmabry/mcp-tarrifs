"""
Tests for database connectivity and operations
"""

import pytest
import asyncio


@pytest.mark.asyncio
async def test_database_connection(db_client):
    """Test basic database connectivity"""
    # Should be able to list tables
    tables = await db_client.list_tables()
    assert isinstance(tables, list)
    assert len(tables) > 0
    print(f"Found {len(tables)} tables in database")


@pytest.mark.asyncio
async def test_database_schema(db_client):
    """Test database schema operations"""
    tables = await db_client.list_tables()
    
    # Test getting schema for first table
    if tables:
        first_table = tables[0]
        schema = await db_client.get_schema(first_table)
        assert isinstance(schema, str)
        assert len(schema) > 0
        print(f"Schema for {first_table}: {schema[:100]}...")


@pytest.mark.asyncio
async def test_database_sample_data(db_client):
    """Test getting sample data from tables"""
    tables = await db_client.list_tables()
    
    if tables:
        # Test sample data from first table
        first_table = tables[0]
        sample = await db_client.get_sample_data(first_table, limit=3)
        assert isinstance(sample, str)
        assert len(sample) > 0
        print(f"Sample data from {first_table} (first 100 chars): {sample[:100]}")


@pytest.mark.asyncio
async def test_database_query_execution(db_client):
    """Test executing queries on the database"""
    # Test basic query
    result = await db_client.execute_query("SELECT COUNT(*) as table_count FROM information_schema.tables")
    assert isinstance(result, str)
    assert "table_count" in result
    print(f"Query result: {result}")


@pytest.mark.asyncio
async def test_tariff_data_structure(db_client):
    """Test that tariff data has expected structure"""
    tables = await db_client.list_tables()
    
    # Should have yearly tariff tables (they start with 'tariff_' not 'tariffs_')
    tariff_tables = [t for t in tables if t.startswith('tariff_')]
    assert len(tariff_tables) > 0, f"Should have at least one tariff table, found tables: {tables}"
    
    # Test that we have data from multiple years
    years = []
    for table in tariff_tables:
        # Extract year from table names like 'tariff_2024_tariff_database_202405'
        parts = table.split('_')
        for part in parts:
            if part.isdigit() and len(part) == 4 and part.startswith('20'):
                years.append(int(part))
                break
    
    assert len(years) > 5, f"Should have data from multiple years, found: {sorted(set(years))}"
    print(f"Found tariff data for years: {sorted(set(years))}")


@pytest.mark.asyncio
async def test_hts_codes_exist(db_client):
    """Test that HTS codes exist in the data"""
    tables = await db_client.list_tables()
    tariff_tables = [t for t in tables if t.startswith('tariff_')]
    
    if tariff_tables:
        # Test first tariff table has HTS codes
        table = tariff_tables[0]
        result = await db_client.execute_query(f"SELECT hts8 FROM {table} LIMIT 5")
        assert "hts8" in result
        print(f"Sample HTS codes from {table}: {result}")