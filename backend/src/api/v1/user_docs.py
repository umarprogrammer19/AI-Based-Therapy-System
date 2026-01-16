from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ...models.knowledge_doc import KnowledgeDoc, KnowledgeDocRead
from ...models.user import User
from ...services.knowledge_service import knowledge_doc_service
from ...api.async_deps import get_async_db_session
from ...services.ingestion import process_uploaded_file
from ...services.auth import auth_service


router = APIRouter(prefix="/user-docs", tags=["user-docs"])


@router.post("/upload", response_model=KnowledgeDocRead)
async def upload_user_document(
    *,
    current_user: User = Depends(auth_service.get_current_user_dependency()),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_db_session)
):
    """
    Upload a document (PDF/TXT) for processing and classification by a user.
    The document will be classified as relevant to ketamine therapy or not using AI.
    """
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
        # Process the uploaded file with user_id
        knowledge_doc = await process_uploaded_file(file, session)

        # Update the document to include the user_id
        knowledge_doc.user_id = current_user.id
        session.add(knowledge_doc)
        await session.commit()
        await session.refresh(knowledge_doc)

        return knowledge_doc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/my-documents", response_model=List[KnowledgeDocRead])
async def get_my_documents(
    *,
    current_user: User = Depends(auth_service.get_current_user_dependency()),
    session: AsyncSession = Depends(get_async_db_session),
    limit: int = 100,
    offset: int = 0,
    sort: str = None
):
    """
    Get documents uploaded by the current user.
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
        sort_direction=sort_direction,
        user_id=current_user.id
    )


@router.get("/all-documents", response_model=List[KnowledgeDocRead])
async def get_all_documents(
    *,
    current_user: User = Depends(auth_service.get_current_user_dependency()),
    session: AsyncSession = Depends(get_async_db_session),
    limit: int = 100,
    offset: int = 0,
    sort: str = None,
    relevant: Optional[bool] = None  # Filter by relevance
):
    """
    Get all documents with optional filters. Regular users can only see their own documents,
    admins can see all documents.
    """
    # Parse sort parameter (e.g., "upload_date:desc")
    sort_field = None
    sort_direction = "asc"
    if sort:
        parts = sort.split(":")
        sort_field = parts[0]
        if len(parts) > 1:
            sort_direction = parts[1]

    # If user is admin, they can see all documents
    # Otherwise, only their own documents
    user_id_filter = None if current_user.role == "admin" else current_user.id

    return await knowledge_doc_service.get_knowledge_docs(
        session=session,
        offset=offset,
        limit=limit,
        sort_field=sort_field,
        sort_direction=sort_direction,
        user_id=user_id_filter,
        relevant=relevant
    )