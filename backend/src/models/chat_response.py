from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
import json
from sqlalchemy import JSON, Column


class ChatResponseBase(SQLModel):
    """
    Base class for ChatResponse with shared attributes.
    """
    chat_query_id: UUID = Field(..., description="Reference to the associated query")
    response_text: str = Field(..., description="The generated response", min_length=1)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence in the response")
    used_context_ids: Optional[List[UUID]] = Field(sa_column=Column(JSON), description="IDs of VectorChunks used in response")
    generation_time_ms: Optional[int] = Field(None, ge=0, description="Time taken to generate response in milliseconds")
    response_metadata: Optional[dict] = Field(sa_column=Column(JSON), description="Additional response metadata")


class ChatResponse(ChatResponseBase, table=True):
    """
    ChatResponse model representing a generated response to a user's query.
    """
    __tablename__ = "chat_responses"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the response was generated")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")


class ChatResponseCreate(ChatResponseBase):
    """
    Schema for creating a ChatResponse.
    """
    pass


class ChatResponseRead(ChatResponseBase):
    """
    Schema for reading a ChatResponse.
    """
    id: UUID
    timestamp: datetime
    created_at: datetime
    updated_at: datetime


class ChatResponseUpdate(SQLModel):
    """
    Schema for updating a ChatResponse.
    """
    chat_query_id: Optional[UUID] = None
    response_text: Optional[str] = None
    confidence_score: Optional[float] = None
    used_context_ids: Optional[List[UUID]] = None
    generation_time_ms: Optional[int] = None
    response_metadata: Optional[dict] = None