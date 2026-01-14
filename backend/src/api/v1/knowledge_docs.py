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


@router.post("/", response_model=KnowledgeDocRead)
def create_knowledge_doc(
    *,
    session: Session = Depends(get_db_session),
    knowledge_doc: KnowledgeDocCreate
):
    """
    Create a new knowledge document.
    """
    try:
        return knowledge_doc_service.create_knowledge_doc(session, knowledge_doc)
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Document already exists: {str(e)}")


@router.get("/{knowledge_doc_id}", response_model=KnowledgeDocRead)
def get_knowledge_doc(
    *,
    session: Session = Depends(get_db_session),
    knowledge_doc_id: str  # Using str to accommodate UUID parsing
):
    """
    Get a knowledge document by ID.
    """
    from uuid import UUID

    try:
        uuid_obj = UUID(knowledge_doc_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    knowledge_doc = knowledge_doc_service.get_knowledge_doc(session, uuid_obj)
    if not knowledge_doc:
        raise HTTPException(status_code=404, detail="Knowledge document not found")
    return knowledge_doc


@router.get("/", response_model=List[KnowledgeDocRead])
def get_knowledge_docs(
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


@router.put("/{knowledge_doc_id}", response_model=KnowledgeDocRead)
def update_knowledge_doc(
    *,
    session: Session = Depends(get_db_session),
    knowledge_doc_id: str,  # Using str to accommodate UUID parsing
    knowledge_doc_update: KnowledgeDocUpdate
):
    """
    Update a knowledge document.
    """
    from uuid import UUID

    try:
        uuid_obj = UUID(knowledge_doc_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_knowledge_doc = knowledge_doc_service.update_knowledge_doc(
        session, uuid_obj, knowledge_doc_update
    )
    if not updated_knowledge_doc:
        raise HTTPException(status_code=404, detail="Knowledge document not found")
    return updated_knowledge_doc


@router.post("/admin/upload", response_model=KnowledgeDocRead)
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


@router.delete("/{knowledge_doc_id}")
def delete_knowledge_doc(
    *,
    session: Session = Depends(get_db_session),
    knowledge_doc_id: str  # Using str to accommodate UUID parsing
):
    """
    Delete a knowledge document.
    """
    try:
        uuid_obj = UUID(knowledge_doc_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = knowledge_doc_service.delete_knowledge_doc(session, uuid_obj)
    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge document not found")
    return {"message": "Knowledge document deleted successfully"}