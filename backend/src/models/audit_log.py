from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
import json


class AuditLogBase(SQLModel):
    """
    Base class for AuditLog with shared attributes.
    """
    action: str = Field(..., description="Type of action performed")
    actor_id: str = Field(..., description="Identifier of who performed the action")
    actor_type: str = Field(..., description="Type of actor - user, system, api")
    resource_type: str = Field(..., description="Type of resource affected")
    resource_id: str = Field(..., description="Identifier of the specific resource")
    details: dict = Field(..., description="Additional information about the action", sa_column_kwargs={"server_default": "'{}'"})
    severity: str = Field(default="info", description="Log level: info, warning, error, critical")
    ip_address: Optional[str] = Field(None, description="IP address of the request, if applicable")
    user_agent: Optional[str] = Field(None, description="User agent string, if applicable")


class AuditLog(AuditLogBase, table=True):
    """
    AuditLog model tracking system actions and events for monitoring and debugging.
    """
    __tablename__ = "audit_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the action occurred")

    def __setattr__(self, name, value):
        # Update the timestamp field automatically if needed
        if name == 'timestamp' and value is None:
            super().__setattr__('timestamp', datetime.utcnow())
        super().__setattr__(name, value)


class AuditLogCreate(AuditLogBase):
    """
    Schema for creating an AuditLog.
    """
    pass


class AuditLogRead(AuditLogBase):
    """
    Schema for reading an AuditLog.
    """
    id: UUID
    timestamp: datetime


class AuditLogUpdate(SQLModel):
    """
    Schema for updating an AuditLog.
    """
    action: Optional[str] = None
    actor_id: Optional[str] = None
    actor_type: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[dict] = None
    severity: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None