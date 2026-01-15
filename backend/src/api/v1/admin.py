from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlmodel import Session
from uuid import UUID
from ...models.knowledge_doc import (
    KnowledgeDoc,
    KnowledgeDocCreate,
    KnowledgeDocRead,
    KnowledgeDocUpdate
)
from ...services.knowledge_service import knowledge_doc_service
from ...api.deps import get_db_session
from ...services.ingestion import process_uploaded_file


router = APIRouter()


@router.post("/upload", response_model=KnowledgeDocRead)
def upload_document(
    *,
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session)
):
    """
    Upload a document (PDF/TXT) for processing and classification.
    The document will be classified as relevant to ketamine therapy or not using AI.
    """
    from uuid import UUID

    # Validate file type
    allowed_types = {"application/pdf", "text/plain", "text/txt"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        )

    # Validate file size (max 50MB)
    max_size = 50 * 1024 * 1024  # 50MB in bytes
    if hasattr(file, 'size') and file.size and file.size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {max_size} bytes"
        )

    try:
        # Process the uploaded file
        knowledge_doc = process_uploaded_file(file, session)
        return knowledge_doc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/documents", response_model=List[KnowledgeDocRead])
def get_documents(
    *,
    session: Session = Depends(get_db_session),
    limit: int = 100,
    offset: int = 0,
    sort: str = None
):
    """
    Get a list of knowledge documents.
    """
    # Parse sort parameter (e.g., "upload_date:desc")
    sort_field = None
    sort_direction = "asc"
    if sort:
        parts = sort.split(":")
        sort_field = parts[0]
        if len(parts) > 1:
            sort_direction = parts[1]

    return knowledge_doc_service.get_knowledge_docs(
        session=session,
        offset=offset,
        limit=limit,
        sort_field=sort_field,
        sort_direction=sort_direction
    )