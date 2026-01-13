from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.knowledge_doc import (
    KnowledgeDoc,
    KnowledgeDocCreate,
    KnowledgeDocUpdate,
    KnowledgeDocRead
)


class KnowledgeDocService:
    """
    Service class for managing KnowledgeDoc entities.
    """

    def create_knowledge_doc(self, session: Session, knowledge_doc: KnowledgeDocCreate) -> KnowledgeDocRead:
        """
        Create a new KnowledgeDoc.
        """
        db_knowledge_doc = KnowledgeDoc.model_validate(knowledge_doc)
        session.add(db_knowledge_doc)
        session.commit()
        session.refresh(db_knowledge_doc)
        return KnowledgeDocRead.model_validate(db_knowledge_doc)

    def get_knowledge_doc(self, session: Session, knowledge_doc_id: UUID) -> Optional[KnowledgeDocRead]:
        """
        Get a KnowledgeDoc by ID.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        knowledge_doc = session.exec(statement).first()
        if knowledge_doc:
            return KnowledgeDocRead.model_validate(knowledge_doc)
        return None

    def get_knowledge_docs(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_direction: str = "asc"
    ) -> List[KnowledgeDocRead]:
        """
        Get a list of KnowledgeDocs with pagination and optional sorting.
        """
        statement = select(KnowledgeDoc).offset(offset).limit(limit)

        # Add sorting if specified
        if sort_field:
            if hasattr(KnowledgeDoc, sort_field):
                if sort_direction.lower() == "desc":
                    statement = statement.order_by(getattr(KnowledgeDoc, sort_field).desc())
                else:
                    statement = statement.order_by(getattr(KnowledgeDoc, sort_field))

        knowledge_docs = session.exec(statement).all()
        return [KnowledgeDocRead.model_validate(kd) for kd in knowledge_docs]

    def update_knowledge_doc(
        self,
        session: Session,
        knowledge_doc_id: UUID,
        knowledge_doc_update: KnowledgeDocUpdate
    ) -> Optional[KnowledgeDocRead]:
        """
        Update a KnowledgeDoc.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        db_knowledge_doc = session.exec(statement).first()
        if not db_knowledge_doc:
            return None

        # Update the fields
        update_data = knowledge_doc_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_knowledge_doc, field, value)

        session.add(db_knowledge_doc)
        session.commit()
        session.refresh(db_knowledge_doc)
        return KnowledgeDocRead.model_validate(db_knowledge_doc)

    def delete_knowledge_doc(self, session: Session, knowledge_doc_id: UUID) -> bool:
        """
        Delete a KnowledgeDoc by ID.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        knowledge_doc = session.exec(statement).first()
        if not knowledge_doc:
            return False

        session.delete(knowledge_doc)
        session.commit()
        return True


# Global instance of the service
knowledge_doc_service = KnowledgeDocService()