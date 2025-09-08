"""JSON formatting utilities for tariff data"""
import json
import re
from typing import List, Dict, Any

def format_tariff_data_as_json(query_result: str, columns: List[str] = None) -> str:
    """
    Convert SQL query result text to structured JSON.
    
    Args:
        query_result: Raw text result from database query
        columns: Optional list of column names
        
    Returns:
        JSON string with structured data
    """
    if not query_result or query_result.strip() == "":
        return json.dumps({"data": [], "count": 0})
    
    # Default columns for tariff queries
    if columns is None:
        columns = ["hts8", "brief_description", "mfn_text_rate"]
    
    try:
        # Split into lines and filter out empty lines
        lines = [line.strip() for line in query_result.split('\n') if line.strip()]
        
        # Skip header line if present (usually contains column names)
        data_lines = lines
        if lines and any(col.lower() in lines[0].lower() for col in columns):
            data_lines = lines[1:]
        
        # Parse each data line
        records = []
        for line in data_lines:
            # Split by tab or multiple spaces (common database output formats)
            fields = re.split(r'\t+|\s{2,}', line)
            
            if len(fields) >= len(columns):
                record = {}
                for i, col in enumerate(columns):
                    if i < len(fields):
                        record[col] = fields[i].strip()
                records.append(record)
        
        return json.dumps({
            "data": records,
            "count": len(records),
            "columns": columns
        }, indent=2)
        
    except Exception as e:
        # Fallback: return raw data with error info
        return json.dumps({
            "error": f"Failed to parse result: {str(e)}",
            "raw_data": query_result,
            "count": 0
        })

def format_comparison_data_as_json(query_result: str) -> str:
    """Format year-over-year comparison data as JSON"""
    columns = ["year", "hts8", "brief_description", "mfn_text_rate"]
    return format_tariff_data_as_json(query_result, columns)
