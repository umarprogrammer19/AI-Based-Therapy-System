from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
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

    async def create_knowledge_doc(self, session: AsyncSession, knowledge_doc: KnowledgeDocCreate) -> KnowledgeDocRead:
        """
        Create a new KnowledgeDoc.
        """
        db_knowledge_doc = KnowledgeDoc.model_validate(knowledge_doc)
        session.add(db_knowledge_doc)
        await session.commit()
        await session.refresh(db_knowledge_doc)
        return KnowledgeDocRead.model_validate(db_knowledge_doc)

    async def get_knowledge_doc(self, session: AsyncSession, knowledge_doc_id: UUID) -> Optional[KnowledgeDocRead]:
        """
        Get a KnowledgeDoc by ID.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        result = await session.execute(statement)
        knowledge_doc = result.scalar_one_or_none()
        if knowledge_doc:
            return KnowledgeDocRead.model_validate(knowledge_doc)
        return None

    async def get_knowledge_docs(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_direction: str = "asc",
        user_id: Optional[UUID] = None,
        relevant: Optional[bool] = None
    ) -> List[KnowledgeDocRead]:
        """
        Get a list of KnowledgeDocs with pagination, optional sorting, and filters.
        """
        statement = select(KnowledgeDoc)

        # Apply filters
        if user_id:
            statement = statement.where(KnowledgeDoc.user_id == user_id)
        if relevant is not None:
            statement = statement.where(KnowledgeDoc.relevant == relevant)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        # Add sorting if specified
        if sort_field:
            if hasattr(KnowledgeDoc, sort_field):
                if sort_direction.lower() == "desc":
                    statement = statement.order_by(getattr(KnowledgeDoc, sort_field).desc())
                else:
                    statement = statement.order_by(getattr(KnowledgeDoc, sort_field))

        result = await session.execute(statement)
        knowledge_docs = result.scalars().all()
        return [KnowledgeDocRead.model_validate(kd) for kd in knowledge_docs]

    async def update_knowledge_doc(
        self,
        session: AsyncSession,
        knowledge_doc_id: UUID,
        knowledge_doc_update: KnowledgeDocUpdate
    ) -> Optional[KnowledgeDocRead]:
        """
        Update a KnowledgeDoc.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        result = await session.execute(statement)
        db_knowledge_doc = result.scalar_one_or_none()
        if not db_knowledge_doc:
            return None

        # Update the fields using model_copy or direct assignment
        update_data = knowledge_doc_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_knowledge_doc, field) and field not in ['id', 'created_at', 'updated_at', 'upload_date']:
                setattr(db_knowledge_doc, field, value)

        session.add(db_knowledge_doc)
        await session.commit()
        await session.refresh(db_knowledge_doc)
        return KnowledgeDocRead.model_validate(db_knowledge_doc)

    async def delete_knowledge_doc(self, session: AsyncSession, knowledge_doc_id: UUID) -> bool:
        """
        Delete a KnowledgeDoc by ID.
        """
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == knowledge_doc_id)
        result = await session.execute(statement)
        knowledge_doc = result.scalar_one_or_none()
        if not knowledge_doc:
            return False

        session.delete(knowledge_doc)
        await session.commit()
        return True


# Global instance of the service
knowledge_doc_service = KnowledgeDocService()