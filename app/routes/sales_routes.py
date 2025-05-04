from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from app.controllers.sales_controller import process_sales_file, get_processed_file
from app.models.schemas import ProcessFileResponse
from app.utils.storage import LocalFileStorage, LOCAL_STORAGE_PATH
import os


router = APIRouter()
storage = LocalFileStorage()

@router.post("/process", response_model=ProcessFileResponse)
async def process_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    async_processing: bool = False
):
    """
    Process a CSV file containing sales data.
    
    Parameters:
    - file: CSV file to process
    - async_processing: If True, process in background (for large files)
    
    Returns:
    - Message and download link for processed file
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    if async_processing:
        return await process_sales_file(file, background_tasks)
    else:
        return await process_sales_file(file)

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download a processed file by its ID.
    
    Parameters:
    - file_id: The ID of the processed file
    
    Returns:
    - The processed CSV file
    """
    if not storage.file_exists(file_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = os.path.join(LOCAL_STORAGE_PATH, file_id)
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=f"sales_results_{file_id}"
    )

