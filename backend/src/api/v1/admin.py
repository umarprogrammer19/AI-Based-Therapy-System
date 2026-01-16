from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ...models.knowledge_doc import (
    KnowledgeDoc,
    KnowledgeDocCreate,
    KnowledgeDocRead,
    KnowledgeDocUpdate
)
from ...models.user import User, UserRole
from ...services.knowledge_service import knowledge_doc_service
from ...api.async_deps import get_async_db_session
from ...services.auth import auth_service
from ...services.ingestion import process_uploaded_file


router = APIRouter()


@router.get("/documents", response_model=List[KnowledgeDocRead])
async def get_documents(
    *,
    session: AsyncSession = Depends(get_async_db_session),
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

    return await knowledge_doc_service.get_knowledge_docs(
        session=session,
        offset=offset,
        limit=limit,
        sort_field=sort_field,
        sort_direction=sort_direction
    )


@router.post("/upload", response_model=KnowledgeDocRead)
async def admin_upload_document(
    *,
    current_user: User = Depends(auth_service.get_current_user_dependency()),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_db_session)
):
    """
    Upload a document (PDF/TXT) for processing and classification by an admin.
    The document will be classified as relevant to ketamine therapy or not using AI.
    Only accessible by admin users.
    """
    # Check if user is admin
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin users can upload documents through this endpoint"
        )

    # Validate file type
    allowed_types = {
        "application/pdf",
        "text/plain",
        "text/txt",
        "application/msword",  # .doc
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # .docx
    }
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
        knowledge_doc = await process_uploaded_file(file, session)

        # Update the document to include the user_id (admin uploading)
        knowledge_doc.user_id = current_user.id
        session.add(knowledge_doc)
        await session.commit()
        await session.refresh(knowledge_doc)

        return knowledge_doc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")