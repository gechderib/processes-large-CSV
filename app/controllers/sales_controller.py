from fastapi import BackgroundTasks, UploadFile
from typing import Dict, Tuple
from app.utils.file_processor import process_csv_chunks, generate_output_csv, generate_file_id
from app.utils.storage import LocalFileStorage
from app.models.schemas import ProcessFileResponse
import io

storage = LocalFileStorage()

async def get_processed_file(file_id: str):
    """Retrieve processed file by ID."""
    return await storage.get_file(file_id)



async def process_sales_file(file: UploadFile, background_tasks: BackgroundTasks = None) -> ProcessFileResponse:
    """
    Process uploaded sales CSV file and return response with download link.
    """
    file_id = generate_file_id()
    
    # Read the file content first (this keeps the file content in memory)
    content = await file.read()
    
    if background_tasks:
        # For background processing, we need to create a new file-like object
        background_tasks.add_task(background_process_and_store, content, file_id)
        return ProcessFileResponse(
            message="File is being processed in the background",
            file_id=file_id,
            download_link=storage.get_download_link(file_id),
            metrics=None
        )
    else:
        # For immediate processing
        file_obj = io.BytesIO(content)
        department_sales, metrics = process_csv_chunks(file_obj)
        output_csv = generate_output_csv(department_sales)
        await storage.save_file(file_id, output_csv)
        return ProcessFileResponse(
            message="File processed successfully",
            file_id=file_id,
            download_link=storage.get_download_link(file_id),
            metrics=metrics
        )

async def background_process_and_store(content: bytes, file_id: str):
    """Background task that processes and stores the file."""
    file_obj = io.BytesIO(content)
    department_sales, metrics = process_csv_chunks(file_obj)
    output_csv = generate_output_csv(department_sales)
    await storage.save_file(file_id, output_csv)


