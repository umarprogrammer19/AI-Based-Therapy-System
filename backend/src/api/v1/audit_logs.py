from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from uuid import UUID
from ...models.audit_log import (
    AuditLog,
    AuditLogCreate,
    AuditLogRead
)
from ...services.audit_service import audit_service
from ...config.database import get_db_session
from ...api.deps import get_db_session as get_session


router = APIRouter()


@router.get("/", response_model=List[AuditLogRead])
def get_audit_logs(
    *,
    session: Session = Depends(get_session),
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Get a list of audit logs with optional filtering.
    """
    # Parse dates if provided
    start_dt = None
    end_dt = None

    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format")

    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format")

    return audit_service.get_audit_logs(
        session=session,
        offset=offset,
        limit=limit,
        action=action,
        resource_type=resource_type,
        start_date=start_dt,
        end_date=end_dt
    )


@router.get("/{audit_log_id}", response_model=AuditLogRead)
def get_audit_log(
    *,
    session: Session = Depends(get_session),
    audit_log_id: str  # Using str to accommodate UUID parsing
):
    """
    Get an audit log by ID.
    """
    try:
        uuid_obj = UUID(audit_log_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    audit_log = audit_service.get_audit_log(session, uuid_obj)
    if not audit_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return audit_log


@router.get("/actions/{action}", response_model=List[AuditLogRead])
def get_audit_logs_by_action(
    *,
    session: Session = Depends(get_session),
    action: str
):
    """
    Get audit logs filtered by action type.
    """
    return audit_service.get_audit_logs_by_action(session, action)