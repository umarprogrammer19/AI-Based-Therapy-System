from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy import JSON, Column
from .knowledge_doc import KnowledgeDoc


class UploadSessionBase(SQLModel):
    """
    Base class for UploadSession with shared attributes.
    """
    user_id: str = Field(..., description="ID of the user who initiated the upload")
    knowledge_doc_id: Optional[UUID] = Field(None, foreign_key="knowledge_docs.id", description="Reference to associated KnowledgeDoc")
    original_filename: str = Field(..., description="Original name of uploaded file", min_length=1)
    file_path: Optional[str] = Field(None, description="Temporary storage path")
    file_size: int = Field(..., description="Size of uploaded file", ge=0)
    status: str = Field(..., description="Current status (uploading, uploaded, processing, completed, failed)")
    progress: Optional[float] = Field(None, description="Processing progress percentage (0.0 to 1.0)", ge=0.0, le=1.0)
    error_details: Optional[str] = Field(None, description="Error details if upload failed")


class UploadSession(UploadSessionBase, table=True):
    """
    UploadSession model for tracking upload processing sessions.
    """
    __tablename__ = "upload_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, description="When upload started")
    completed_at: Optional[datetime] = Field(None, description="When processing completed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")


class UploadSessionCreate(UploadSessionBase):
    """
    Schema for creating an UploadSession.
    """
    pass


class UploadSessionRead(UploadSessionBase):
    """
    Schema for reading an UploadSession.
    """
    id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class UploadSessionUpdate(SQLModel):
    """
    Schema for updating an UploadSession.
    """
    user_id: Optional[str] = None
    knowledge_doc_id: Optional[UUID] = None
    original_filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    error_details: Optional[str] = None
    completed_at: Optional[datetime] = None