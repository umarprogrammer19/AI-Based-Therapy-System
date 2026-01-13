from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.vector_chunk import VectorChunk, VectorChunkCreate, VectorChunkUpdate, VectorChunkRead
from ..models.knowledge_doc import KnowledgeDoc


class VectorChunkService:
    """
    Service class for managing VectorChunk entities.
    """

    def create_vector_chunk(self, session: Session, vector_chunk: VectorChunkCreate) -> VectorChunkRead:
        """
        Create a new VectorChunk.
        """
        # Verify that the associated knowledge_doc_id exists
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == vector_chunk.knowledge_doc_id)
        knowledge_doc = session.exec(statement).first()
        if not knowledge_doc:
            raise ValueError(f"KnowledgeDoc with id {vector_chunk.knowledge_doc_id} does not exist")

        # Validate that the embedding has exactly 384 dimensions
        if len(vector_chunk.embedding) != 384:
            raise ValueError(f"Embedding must have exactly 384 dimensions, got {len(vector_chunk.embedding)}")

        db_vector_chunk = VectorChunk.model_validate(vector_chunk)
        session.add(db_vector_chunk)
        session.commit()
        session.refresh(db_vector_chunk)
        return VectorChunkRead.model_validate(db_vector_chunk)

    def get_vector_chunk(self, session: Session, vector_chunk_id: UUID) -> Optional[VectorChunkRead]:
        """
        Get a VectorChunk by ID.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        vector_chunk = session.exec(statement).first()
        if vector_chunk:
            return VectorChunkRead.model_validate(vector_chunk)
        return None

    def get_vector_chunks(
        self,
        session: Session,
        knowledge_doc_id: Optional[UUID] = None,
        offset: int = 0,
        limit: int = 100
    ) -> List[VectorChunkRead]:
        """
        Get a list of VectorChunks with optional filtering by knowledge document.
        """
        statement = select(VectorChunk)

        if knowledge_doc_id:
            statement = statement.where(VectorChunk.knowledge_doc_id == knowledge_doc_id)

        statement = statement.offset(offset).limit(limit)

        vector_chunks = session.exec(statement).all()
        return [VectorChunkRead.model_validate(vc) for vc in vector_chunks]

    def update_vector_chunk(
        self,
        session: Session,
        vector_chunk_id: UUID,
        vector_chunk_update: VectorChunkUpdate
    ) -> Optional[VectorChunkRead]:
        """
        Update a VectorChunk.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        db_vector_chunk = session.exec(statement).first()
        if not db_vector_chunk:
            return None

        # Update the fields
        update_data = vector_chunk_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vector_chunk, field, value)

        session.add(db_vector_chunk)
        session.commit()
        session.refresh(db_vector_chunk)
        return VectorChunkRead.model_validate(db_vector_chunk)

    def delete_vector_chunk(self, session: Session, vector_chunk_id: UUID) -> bool:
        """
        Delete a VectorChunk by ID.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        vector_chunk = session.exec(statement).first()
        if not vector_chunk:
            return False

        session.delete(vector_chunk)
        session.commit()
        return True

    def search_similar_vectors(
        self,
        session: Session,
        query_embedding: List[float],
        limit: int = 10,
        knowledge_doc_ids: Optional[List[UUID]] = None
    ) -> List[VectorChunkRead]:
        """
        Search for similar vector chunks using cosine similarity.
        This is a simplified implementation that will need to be enhanced with actual pgvector functions.
        """
        # This is a placeholder implementation
        # In a real implementation, we'd use pgvector functions like:
        # SELECT *, embedding <=> %s AS distance FROM vector_chunks ORDER BY distance LIMIT %s
        # For now, we'll return a basic implementation that finds chunks with closest embedding values

        statement = select(VectorChunk)

        if knowledge_doc_ids:
            statement = statement.where(VectorChunk.knowledge_doc_id.in_(knowledge_doc_ids))

        all_chunks = session.exec(statement).all()

        # Calculate cosine similarity for each chunk
        similarities = []
        for chunk in all_chunks:
            # Simple dot product calculation for demonstration
            # In practice, this should use pgvector's built-in functions
            similarity = sum(a * b for a, b in zip(query_embedding, chunk.embedding))
            similarities.append((chunk, similarity))

        # Sort by similarity (descending) and return top N
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [chunk for chunk, sim in similarities[:limit]]

        return [VectorChunkRead.model_validate(vc) for vc in top_chunks]


# Global instance of the service
vector_chunk_service = VectorChunkService()