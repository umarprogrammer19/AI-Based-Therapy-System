from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
import json
from sqlalchemy import JSON, Column


class KnowledgeDocBase(SQLModel):
    """
    Base class for KnowledgeDoc with shared attributes.
    """
    filename: str = Field(..., description="Name of the uploaded file", min_length=1)
    file_size: int = Field(..., description="Size of the file in bytes", ge=0)
    source: str = Field(..., description="Where the document originated from")
    content_type: Optional[str] = Field(None, description="MIME type of the document")
    checksum: Optional[str] = Field(None, description="Hash of the file for integrity checking")
    doc_metadata: Optional[dict] = Field(None, description="Additional document-specific metadata", sa_column=Column(JSON))
    # Ingestion-specific fields
    relevant: bool = Field(..., description="Whether document is relevant to ketamine therapy (classification result)")
    classification_reason: Optional[str] = Field(None, description="Reason for classification decision")
    processing_status: str = Field(default="uploaded", description="Current status (uploaded, classified, processing, completed, failed, skipped)")
    error_message: Optional[str] = Field(None, description="Error details if processing failed")


class KnowledgeDoc(KnowledgeDocBase, table=True):
    """
    KnowledgeDoc model representing a knowledge document with metadata.
    """
    __tablename__ = "knowledge_docs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    upload_date: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when document was uploaded")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")



class KnowledgeDocCreate(KnowledgeDocBase):
    """
    Schema for creating a KnowledgeDoc.
    """
    pass


class KnowledgeDocRead(KnowledgeDocBase):
    """
    Schema for reading a KnowledgeDoc.
    """
    id: UUID
    upload_date: datetime
    created_at: datetime
    updated_at: datetime


class KnowledgeDocUpdate(SQLModel):
    """
    Schema for updating a KnowledgeDoc.
    """
    filename: Optional[str] = None
    file_size: Optional[int] = None
    source: Optional[str] = None
    content_type: Optional[str] = None
    checksum: Optional[str] = None
    doc_metadata: Optional[dict] = None
    # Ingestion-specific fields
    relevant: Optional[bool] = None
    classification_reason: Optional[str] = None
    processing_status: Optional[str] = None
    error_message: Optional[str] = None