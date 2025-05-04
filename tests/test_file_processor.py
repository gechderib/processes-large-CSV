import io
import pytest
from app.utils.file_processor import process_csv_chunks, generate_output_csv

def test_process_csv_chunks():
    # Create test CSV data
    csv_data = b"""Department Name,Date,Number of Sales
Electronics,2023-08-01,100
Clothing,2023-08-01,200
Electronics,2023-08-02,150
"""
    file = io.BytesIO(csv_data)
    
    result, metrics = process_csv_chunks(file)
    
    assert result == {
        "Electronics": 250,
        "Clothing": 200
    }
    assert metrics['total_rows_processed'] == 3
    assert metrics['total_departments'] == 2

def test_generate_output_csv():
    department_sales = {
        "Electronics": 250,
        "Clothing": 200
    }
    output = generate_output_csv(department_sales)
    content = output.getvalue().splitlines()
    
    assert content[0] == "Department Name,Total Number of Sales"
    assert "Electronics,250" in content
    assert "Clothing,200" in content