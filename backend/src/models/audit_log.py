from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy import JSON, Column


class AuditLogBase(SQLModel):
    """
    Base class for AuditLog with shared attributes.
    """
    user_id: str = Field(..., description="ID of the user performing the action")
    action: str = Field(..., description="Action performed (upload, delete, update, etc.)")
    resource_type: str = Field(..., description="Type of resource affected")
    resource_id: str = Field(..., description="ID of the resource affected")
    ip_address: Optional[str] = Field(None, description="IP address of the request")
    user_agent: Optional[str] = Field(None, description="User agent string")
    details: Optional[dict] = Field(None, description="Additional details about the action", sa_column=Column(JSON))


class AuditLog(AuditLogBase, table=True):
    """
    AuditLog model storing audit trail for system actions.
    """
    __tablename__ = "audit_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique identifier for the audit log entry")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the action occurred")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")


class AuditLogCreate(AuditLogBase):
    """
    Schema for creating an AuditLog entry.
    """
    pass


class AuditLogRead(AuditLogBase):
    """
    Schema for reading an AuditLog entry.
    """
    id: UUID
    timestamp: datetime
    created_at: datetime


class AuditLogUpdate(SQLModel):
    """
    Schema for updating an AuditLog entry.
    """
    user_id: Optional[str] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[dict] = None