from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session
from uuid import UUID
from pydantic import BaseModel
from ...models.vector_chunk import (
    VectorChunk,
    VectorChunkCreate,
    VectorChunkRead,
    VectorChunkUpdate
)
from ...services.vector_service import vector_chunk_service
from ...api.deps import get_db_session


router = APIRouter()


class VectorSearchRequest(BaseModel):
    """
    Request model for vector similarity search.
    """
    query_embedding: List[float]
    limit: int = 10
    knowledge_doc_ids: Optional[List[str]] = None  # Using str to accommodate UUID parsing


class VectorChunkWithSimilarity(VectorChunkRead):
    """
    VectorChunk with similarity score for search results.
    """
    similarity_score: float


@router.post("/", response_model=VectorChunkRead)
def create_vector_chunk(
    *,
    session: Session = Depends(get_db_session),
    vector_chunk: VectorChunkCreate
):
    """
    Create a new vector chunk.
    """
    try:
        return vector_chunk_service.create_vector_chunk(session, vector_chunk)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{vector_chunk_id}", response_model=VectorChunkRead)
def get_vector_chunk(
    *,
    session: Session = Depends(get_db_session),
    vector_chunk_id: str  # Using str to accommodate UUID parsing
):
    """
    Get a vector chunk by ID.
    """
    try:
        uuid_obj = UUID(vector_chunk_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    vector_chunk = vector_chunk_service.get_vector_chunk(session, uuid_obj)
    if not vector_chunk:
        raise HTTPException(status_code=404, detail="Vector chunk not found")
    return vector_chunk


@router.get("/", response_model=List[VectorChunkRead])
def get_vector_chunks(
    *,
    session: Session = Depends(get_db_session),
    knowledge_doc_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Get a list of vector chunks.
    """
    knowledge_doc_uuid = None
    if knowledge_doc_id:
        try:
            knowledge_doc_uuid = UUID(knowledge_doc_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid knowledge_doc_id UUID format")

    return vector_chunk_service.get_vector_chunks(
        session=session,
        knowledge_doc_id=knowledge_doc_uuid,
        offset=offset,
        limit=limit
    )


@router.put("/{vector_chunk_id}", response_model=VectorChunkRead)
def update_vector_chunk(
    *,
    session: Session = Depends(get_db_session),
    vector_chunk_id: str,  # Using str to accommodate UUID parsing
    vector_chunk_update: VectorChunkUpdate
):
    """
    Update a vector chunk.
    """
    try:
        uuid_obj = UUID(vector_chunk_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_vector_chunk = vector_chunk_service.update_vector_chunk(
        session, uuid_obj, vector_chunk_update
    )
    if not updated_vector_chunk:
        raise HTTPException(status_code=404, detail="Vector chunk not found")
    return updated_vector_chunk


@router.delete("/{vector_chunk_id}")
def delete_vector_chunk(
    *,
    session: Session = Depends(get_db_session),
    vector_chunk_id: str  # Using str to accommodate UUID parsing
):
    """
    Delete a vector chunk.
    """
    try:
        uuid_obj = UUID(vector_chunk_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = vector_chunk_service.delete_vector_chunk(session, uuid_obj)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vector chunk not found")
    return {"message": "Vector chunk deleted successfully"}


@router.post("/search", response_model=List[VectorChunkWithSimilarity])
def search_vector_chunks(
    *,
    session: Session = Depends(get_db_session),
    search_request: VectorSearchRequest
):
    """
    Search for similar vector chunks using cosine similarity.
    """
    # Validate the query embedding dimensions
    if len(search_request.query_embedding) != 384:
        raise HTTPException(
            status_code=400,
            detail=f"Query embedding must have exactly 384 dimensions, got {len(search_request.query_embedding)}"
        )

    # Convert knowledge_doc_ids from string to UUID if provided
    knowledge_doc_uuids = None
    if search_request.knowledge_doc_ids:
        knowledge_doc_uuids = []
        for doc_id_str in search_request.knowledge_doc_ids:
            try:
                knowledge_doc_uuids.append(UUID(doc_id_str))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid knowledge_doc_id UUID format: {doc_id_str}")

    # Perform the search
    similar_chunks = vector_chunk_service.search_similar_vectors(
        session=session,
        query_embedding=search_request.query_embedding,
        limit=search_request.limit,
        knowledge_doc_ids=knowledge_doc_uuids
    )

    # For now, we'll return the chunks with a dummy similarity score
    # In a real implementation, the service would return actual similarity scores
    result = []
    for chunk in similar_chunks:
        chunk_with_similarity = chunk.dict()
        chunk_with_similarity["similarity_score"] = 0.0  # Placeholder - actual similarity would be computed in the service
        result.append(VectorChunkWithSimilarity(**chunk_with_similarity))

    return result