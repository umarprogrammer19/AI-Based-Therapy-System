from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any
import json
from sqlalchemy import JSON, Column
from pgvector.sqlalchemy import Vector


class ChatQueryBase(SQLModel):
    """
    Base class for ChatQuery with shared attributes.
    """
    user_id: str = Field(..., description="ID of the user who submitted the query", min_length=1)
    query_text: str = Field(..., description="The user's input query", min_length=1, max_length=1000)
    session_id: Optional[str] = Field(None, description="Identifier for conversation session")
    query_embedding: Optional[List[float]] = Field(None, sa_column=Column(Vector(384)), description="Vector embedding of the query")
    is_off_topic: Optional[bool] = Field(None, description="Result of guardrail check")
    retrieved_context_ids: Optional[List[UUID]] = Field(sa_column=Column(JSON), description="IDs of VectorChunks retrieved")
    query_metadata: Optional[Dict[str, Any]] = Field(sa_column=Column(JSON), description="Additional query metadata")


class ChatQuery(ChatQueryBase, table=True):
    """
    ChatQuery model representing a user's query to the chat system.
    """
    __tablename__ = "chat_queries"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the query was submitted")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")


class ChatQueryCreate(ChatQueryBase):
    """
    Schema for creating a ChatQuery.
    """
    pass


class ChatQueryRead(ChatQueryBase):
    """
    Schema for reading a ChatQuery.
    """
    id: UUID
    timestamp: datetime
    created_at: datetime
    updated_at: datetime


class ChatQueryUpdate(SQLModel):
    """
    Schema for updating a ChatQuery.
    """
    user_id: Optional[str] = None
    query_text: Optional[str] = None
    session_id: Optional[str] = None
    query_embedding: Optional[List[float]] = None
    is_off_topic: Optional[bool] = None
    retrieved_context_ids: Optional[List[UUID]] = None
    query_metadata: Optional[dict] = None