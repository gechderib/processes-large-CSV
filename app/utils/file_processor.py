import csv
from io import StringIO, BytesIO
from typing import Dict, Tuple
import time
import uuid
from datetime import datetime
import io


def process_row(row: dict, department_sales: Dict[str, int]):
    """Process a single row of CSV data and update department_sales dict."""
    try:
        dept = row['Department Name']
        sales = int(row['Number of Sales'])
        department_sales[dept] = department_sales.get(dept, 0) + sales
    except (ValueError, KeyError) as e:
        # Skip malformed rows
        pass

def generate_output_csv(department_sales: Dict[str, int]) -> StringIO:
    """Generate the output CSV file from aggregated sales data."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Department Name', 'Total Number of Sales'])
    
    for dept, total in department_sales.items():
        writer.writerow([dept, total])
    
    output.seek(0)
    return output

def generate_file_id() -> str:
    """Generate a unique file ID using time-based UUID."""
    return f"result_{uuid.uuid1()}.csv"

def process_csv_chunks(file_obj: BytesIO) -> Tuple[Dict[str, int], dict]:
    """
    Process CSV file in chunks to aggregate sales by department.
    """
    start_time = time.time()
    total_rows = 0
    department_sales = {}
    
    # Reset file pointer to beginning
    file_obj.seek(0)
    
    # Create text wrapper
    text_wrapper = io.TextIOWrapper(file_obj, encoding='utf-8')
    
    csv_reader = csv.DictReader(text_wrapper, fieldnames=['Department Name', 'Date', 'Number of Sales'])
    
    # Skip header if present
    try:
        first_row = next(csv_reader)
        if first_row['Department Name'] == 'Department Name' and first_row['Date'] == 'Date':
            pass  # Skip header
        else:
            # Process first row if it's not a header
            process_row(first_row, department_sales)
            total_rows += 1
    except StopIteration:
        pass
    
    # Process remaining rows
    for row in csv_reader:
        process_row(row, department_sales)
        total_rows += 1
    
    # Detach the text wrapper to prevent closing the underlying BytesIO
    text_wrapper.detach()
    
    metrics = {
        'processing_time_seconds': time.time() - start_time,
        'total_rows_processed': total_rows,
        'total_departments': len(department_sales),
        'completed_at': datetime.utcnow().isoformat()
    }
    
    return department_sales, metrics



