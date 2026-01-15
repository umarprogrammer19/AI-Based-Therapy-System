from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional, List

class ChatMessage(SQLModel, table=True):
    """
    Represents individual messages within a chat session with role (user/system) and content
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="chatsession.id")  # Foreign Key to ChatSession
    role: str = Field(sa_column_kwargs={"nullable": False})  # either "user" or "assistant"
    content: str = Field(sa_column_kwargs={"nullable": False})  # the message content
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # when the message was sent
    source_chunks: Optional[str] = Field(default=None)  # IDs of vector chunks referenced in response (as JSON string)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_12345",
                "role": "assistant",
                "content": "Ketamine therapy has shown promising results...",
                "source_chunks": '["chunk_abc123", "chunk_def456"]'
            }
        }