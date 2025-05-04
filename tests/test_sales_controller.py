import io
import pytest
from fastapi import UploadFile, BackgroundTasks
from app.controllers.sales_controller import process_sales_file

@pytest.mark.asyncio
async def test_process_sales_file():
    # Create test file
    csv_data = b"""Department Name,Date,Number of Sales
Electronics,2023-08-01,100
Clothing,2023-08-01,200
Electronics,2023-08-02,150
"""
    file = io.BytesIO(csv_data)
    upload_file = UploadFile(filename="test.csv", file=file)
    
    response = await process_sales_file(upload_file)
    
    assert "download" in response.download_link
    assert response.metrics['total_rows_processed'] == 3