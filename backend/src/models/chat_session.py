from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy import Column, DateTime
from ..models.user import User


class ChatSessionBase(SQLModel):
    """
    Base class for ChatSession with shared attributes.
    """
    title: str = Field(..., description="Title of the chat session", max_length=255)
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who owns this session")
    is_active: bool = Field(default=True, description="Whether this session is currently active")


class ChatSession(ChatSessionBase, table=True):
    """
    ChatSession model representing a conversation session.
    """
    __tablename__ = "chat_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))


class ChatSessionCreate(ChatSessionBase):
    """
    Schema for creating a ChatSession.
    """
    pass


class ChatSessionRead(ChatSessionBase):
    """
    Schema for reading a ChatSession.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime


class ChatSessionUpdate(SQLModel):
    """
    Schema for updating a ChatSession.
    """
    title: Optional[str] = None
    is_active: Optional[bool] = None