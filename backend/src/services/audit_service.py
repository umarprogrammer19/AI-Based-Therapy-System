from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from ..models.audit_log import AuditLog, AuditLogCreate, AuditLogUpdate, AuditLogRead


class AuditService:
    """
    Service class for managing AuditLog entities.
    """

    def create_audit_log(self, session: Session, audit_log: AuditLogCreate) -> AuditLogRead:
        """
        Create a new AuditLog.
        """
        db_audit_log = AuditLog.model_validate(audit_log)
        session.add(db_audit_log)
        session.commit()
        session.refresh(db_audit_log)
        return AuditLogRead.model_validate(db_audit_log)

    def get_audit_log(self, session: Session, audit_log_id: UUID) -> Optional[AuditLogRead]:
        """
        Get an AuditLog by ID.
        """
        statement = select(AuditLog).where(AuditLog.id == audit_log_id)
        audit_log = session.exec(statement).first()
        if audit_log:
            return AuditLogRead.model_validate(audit_log)
        return None

    def get_audit_logs(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 100,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AuditLogRead]:
        """
        Get a list of AuditLogs with pagination and optional filters.
        """
        statement = select(AuditLog)

        # Apply filters if provided
        if action:
            statement = statement.where(AuditLog.action == action)
        if resource_type:
            statement = statement.where(AuditLog.resource_type == resource_type)
        if start_date:
            statement = statement.where(AuditLog.timestamp >= start_date)
        if end_date:
            statement = statement.where(AuditLog.timestamp <= end_date)

        statement = statement.offset(offset).limit(limit)

        audit_logs = session.exec(statement).all()
        return [AuditLogRead.model_validate(al) for al in audit_logs]

    def get_audit_logs_by_action(self, session: Session, action: str) -> List[AuditLogRead]:
        """
        Get AuditLogs filtered by action type.
        """
        statement = select(AuditLog).where(AuditLog.action == action).limit(100)
        audit_logs = session.exec(statement).all()
        return [AuditLogRead.model_validate(al) for al in audit_logs]

    def create_knowledge_doc_audit(self, session: Session, actor_id: str, actor_type: str,
                                   resource_id: str, details: dict, ip_address: str = None,
                                   user_agent: str = None) -> AuditLogRead:
        """
        Create an audit log for a KnowledgeDoc operation.
        """
        audit_log_create = AuditLogCreate(
            action="knowledge_doc_created",
            actor_id=actor_id,
            actor_type=actor_type,
            resource_type="KnowledgeDoc",
            resource_id=resource_id,
            details=details,
            severity="info",
            ip_address=ip_address,
            user_agent=user_agent
        )
        return self.create_audit_log(session, audit_log_create)


# Global instance of the service
audit_service = AuditService()