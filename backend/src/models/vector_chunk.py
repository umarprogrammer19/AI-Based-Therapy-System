from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
import json
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from .knowledge_doc import KnowledgeDoc


class VectorChunkBase(SQLModel):
    """
    Base class for VectorChunk with shared attributes.
    """
    knowledge_doc_id: UUID = Field(..., foreign_key="knowledge_docs.id", description="Foreign key to KnowledgeDoc")
    text_content: str = Field(..., description="The actual text content of the chunk", min_length=1)
    embedding: List[float] = Field(..., sa_column=Column(Vector(384)), description="384-dimensional vector embedding")
    chunk_index: int = Field(..., description="Order of the chunk within the original document")
    chunk_metadata: Optional[dict] = Field(None, description="Metadata about the specific chunk", sa_column_kwargs={"server_default": "NULL"})
    similarity_score: Optional[float] = Field(None, description="Cached similarity scores when applicable")


class VectorChunk(VectorChunkBase, table=True):
    """
    VectorChunk model storing text content with vector embeddings for similarity search.
    """
    __tablename__ = "vector_chunks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")

    # Update the updated_at field automatically
    def __setattr__(self, name, value):
        if name == 'updated_at':
            super().__setattr__('updated_at', datetime.utcnow())
        super().__setattr__(name, value)


class VectorChunkCreate(VectorChunkBase):
    """
    Schema for creating a VectorChunk.
    """
    pass


class VectorChunkRead(VectorChunkBase):
    """
    Schema for reading a VectorChunk.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime


class VectorChunkUpdate(SQLModel):
    """
    Schema for updating a VectorChunk.
    """
    text_content: Optional[str] = None
    embedding: Optional[List[float]] = None
    chunk_index: Optional[int] = None
    chunk_metadata: Optional[dict] = None
    similarity_score: Optional[float] = None