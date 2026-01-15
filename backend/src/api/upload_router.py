from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from typing import Optional
import uuid
from datetime import datetime
import os

from ..database.connection import get_session
from ..services.ingestion_service import IngestionService

router = APIRouter()

def verify_api_key(x_api_key: str = None):
    """Verify admin API key for upload access"""
    required_api_key = os.getenv("ADMIN_API_KEY", "placeholder_api_key")
    if x_api_key != required_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.post("/admin/upload")
async def upload_document(
    file: UploadFile = File(...),
    x_api_key: str = Depends(verify_api_key),
    session: Session = Depends(get_session)
):
    """
    Upload a document for classification and processing
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt', '.md']
    file_extension = '.' + file.filename.split('.')[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: .pdf, .docx, .txt, .md")

    # Validate file size (optional: limit to 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()

    # Check file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")

    # Reset file pointer for further processing
    await file.seek(0)

    # Process the upload using the ingestion service
    ingestion_service = IngestionService()

    try:
        result = await ingestion_service.process_upload(file, "admin_user", session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")