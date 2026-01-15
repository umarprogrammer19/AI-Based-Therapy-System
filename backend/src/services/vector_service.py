from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..models.vector_chunk import VectorChunk, VectorChunkCreate, VectorChunkUpdate, VectorChunkRead
from ..models.knowledge_doc import KnowledgeDoc


class VectorChunkService:
    """
    Service class for managing VectorChunk entities.
    """

    async def create_vector_chunk(self, session: AsyncSession, vector_chunk: VectorChunkCreate) -> VectorChunkRead:
        """
        Create a new VectorChunk.
        """
        # Verify that the associated knowledge_doc_id exists
        statement = select(KnowledgeDoc).where(KnowledgeDoc.id == vector_chunk.knowledge_doc_id)
        result = await session.execute(statement)
        knowledge_doc = result.first()
        if not knowledge_doc:
            raise ValueError(f"KnowledgeDoc with id {vector_chunk.knowledge_doc_id} does not exist")

        # Validate that the embedding has exactly 384 dimensions
        if len(vector_chunk.embedding) != 384:
            raise ValueError(f"Embedding must have exactly 384 dimensions, got {len(vector_chunk.embedding)}")

        db_vector_chunk = VectorChunk.model_validate(vector_chunk)
        session.add(db_vector_chunk)
        await session.commit()
        await session.refresh(db_vector_chunk)
        return VectorChunkRead.model_validate(db_vector_chunk)

    async def get_vector_chunk(self, session: AsyncSession, vector_chunk_id: UUID) -> Optional[VectorChunkRead]:
        """
        Get a VectorChunk by ID.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        result = await session.execute(statement)
        vector_chunk = result.first()
        if vector_chunk:
            return VectorChunkRead.model_validate(vector_chunk)
        return None

    async def get_vector_chunks(
        self,
        session: AsyncSession,
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

        result = await session.execute(statement)
        vector_chunks = result.all()
        return [VectorChunkRead.model_validate(vc) for vc in vector_chunks]

    async def update_vector_chunk(
        self,
        session: AsyncSession,
        vector_chunk_id: UUID,
        vector_chunk_update: VectorChunkUpdate
    ) -> Optional[VectorChunkRead]:
        """
        Update a VectorChunk.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        result = await session.execute(statement)
        db_vector_chunk = result.first()
        if not db_vector_chunk:
            return None

        # Update the fields
        update_data = vector_chunk_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vector_chunk, field, value)

        session.add(db_vector_chunk)
        await session.commit()
        await session.refresh(db_vector_chunk)
        return VectorChunkRead.model_validate(db_vector_chunk)

    async def delete_vector_chunk(self, session: AsyncSession, vector_chunk_id: UUID) -> bool:
        """
        Delete a VectorChunk by ID.
        """
        statement = select(VectorChunk).where(VectorChunk.id == vector_chunk_id)
        result = await session.execute(statement)
        vector_chunk = result.first()
        if not vector_chunk:
            return False

        session.delete(vector_chunk)
        await session.commit()
        return True

    async def search_similar_vectors(
        self,
        session: AsyncSession,
        query_embedding: List[float],
        limit: int = 10,
        knowledge_doc_ids: Optional[List[UUID]] = None
    ) -> List[tuple]:
        """
        Search for similar vector chunks using pgvector cosine similarity operator.

        Args:
            session: Database session
            query_embedding: The embedding vector to search for similar vectors
            limit: Maximum number of results to return
            knowledge_doc_ids: Optional list of document IDs to filter by

        Returns:
            List of tuples containing (VectorChunk, similarity_score)
        """
        from sqlalchemy import text

        # Use raw SQL with pgvector operators since SQLModel doesn't directly support them
        # Using the cosine distance operator (<=>) which calculates 1 - cosine_similarity
        base_query = """
            SELECT *, (embedding <=> :query_embedding) AS distance
            FROM vector_chunks
            WHERE TRUE
        """

        params = {"query_embedding": query_embedding}

        # Add filter for specific knowledge documents if provided
        if knowledge_doc_ids:
            # Create placeholders for the IN clause
            doc_placeholders = ", ".join([f":doc_id_{i}" for i in range(len(knowledge_doc_ids))])
            base_query += f" AND knowledge_doc_id IN ({doc_placeholders})"

            # Add the document IDs to the params
            for i, doc_id in enumerate(knowledge_doc_ids):
                params[f"doc_id_{i}"] = doc_id

        # Order by distance (ascending, so closest matches first) and limit
        base_query += " ORDER BY distance ASC LIMIT :limit"
        params["limit"] = limit

        # Convert the embedding list to the proper format for pgvector
        # PostgreSQL's vector extension expects arrays in a specific format
        formatted_params = params.copy()
        formatted_params["query_embedding"] = "[" + ",".join(map(str, params["query_embedding"])) + "]"

        # Execute the raw SQL query
        result = await session.execute(text(base_query), formatted_params)

        # Fetch all results
        rows = result.fetchall()

        # Process the results
        formatted_results = []
        for row in rows:
            # Convert row to dict to access all columns
            row_dict = dict(row._mapping)

            # Extract the distance and remove it from the chunk data
            distance = row_dict.pop('distance')

            # Convert distance to similarity score (cosine similarity = 1 - cosine distance)
            similarity_score = max(0.0, 1.0 - distance)  # Ensure non-negative

            # Remove the extra columns that are not part of VectorChunk
            # Only keep the fields that are part of the VectorChunk model
            allowed_fields = {
                'id', 'knowledge_doc_id', 'text_content', 'embedding', 'chunk_index',
                'chunk_metadata', 'similarity_score', 'created_at', 'updated_at'
            }
            chunk_data = {k: v for k, v in row_dict.items() if k in allowed_fields}

            # Create VectorChunk object from the data
            try:
                chunk = VectorChunk(**chunk_data)
                formatted_results.append((VectorChunkRead.model_validate(chunk), similarity_score))
            except Exception:
                # If there's an issue creating the object, skip this result
                continue

        return formatted_results


# Global instance of the service
vector_chunk_service = VectorChunkService()