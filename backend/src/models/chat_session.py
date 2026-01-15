from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional

class ChatSession(SQLModel, table=True):
    """
    Represents a user's chat session with a unique identifier and user information
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_identifier: str = Field(sa_column_kwargs={"nullable": False})  # identifier of the user
    created_at: datetime = Field(default_factory=datetime.utcnow)  # timestamp of session creation
    last_activity_at: datetime = Field(default_factory=datetime.utcnow)  # timestamp of last activity
    is_active: bool = Field(default=True)  # indicates if session is currently active

    class Config:
        json_schema_extra = {
            "example": {
                "user_identifier": "user_123",
                "is_active": True
            }
        }