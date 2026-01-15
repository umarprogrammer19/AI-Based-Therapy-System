from sqlmodel import Session, select
from sqlalchemy import func, text
from typing import List
import uuid
from ..models.vector_chunk import VectorChunk, VectorChunkRead
from ..utils.embeddings import EmbeddingGenerator
import numpy as np


class RAGService:
    """
    Retrieval-Augmented Generation service for finding relevant document chunks
    based on user queries and returning them for context in responses
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    def retrieve_relevant_chunks(self, query: str, session: Session, top_k: int = 3) -> List[VectorChunk]:
        """
        Retrieve the top-k most relevant chunks to the query using vector similarity

        Args:
            query: User's query to find relevant context for
            session: Database session for querying
            top_k: Number of top results to return (default 3)

        Returns:
            List of VectorChunk objects that are most relevant to the query
        """
        # Generate embedding for the query
        query_embedding = self.embedding_generator.generate_embedding(query)

        # Create the embedding vector string for SQL query
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        # Use raw SQL to leverage pgvector's cosine distance operator '<->'
        # This performs the similarity search at the database level which is much more efficient
        sql = text("""
            SELECT id
            FROM vector_chunks
            ORDER BY embedding <-> :embedding::vector
            LIMIT :limit
        """)

        result = session.exec(
            sql,
            params={"embedding": embedding_str, "limit": top_k}
        )

        # Fetch the IDs from the similarity search
        chunk_ids = [row[0] for row in result.all()]

        if not chunk_ids:
            return []

        # Query for the actual VectorChunk objects using the IDs in the correct order
        # First get all chunks
        all_matching_chunks = session.exec(
            select(VectorChunk).where(VectorChunk.id.in_(chunk_ids))
        ).all()

        # Then reorder them to match the similarity ranking
        chunks_by_id = {str(chunk.id): chunk for chunk in all_matching_chunks}
        ordered_chunks = [chunks_by_id[str(chunk_id)] for chunk_id in chunk_ids if str(chunk_id) in chunks_by_id]

        return ordered_chunks

    def construct_prompt_with_context(self, query: str, relevant_chunks: List[VectorChunk]) -> str:
        """
        Construct a prompt that includes the system prompt, relevant context, and user query

        Args:
            query: Original user query
            relevant_chunks: List of relevant VectorChunk objects

        Returns:
            Formatted prompt string with context
        """
        system_prompt = "You are a medical information assistant specializing ONLY in ketamine therapy. You must provide educational information based on the provided context. Do not diagnose conditions, prescribe treatments, or provide medical advice beyond the scope of ketamine therapy. If the context doesn't contain relevant information, politely explain that you don't have sufficient information to answer the question."

        # Build context from relevant chunks
        context = ""
        if relevant_chunks:
            context = "Relevant Context:\n"
            for i, chunk in enumerate(relevant_chunks, 1):
                context += f"{i}. {chunk.text_content}\n\n"
        else:
            context = "No relevant context found in the knowledge base.\n"

        # Construct the full prompt
        full_prompt = f"{system_prompt}\n\n{context}\nUser Question: {query}\n\nAssistant:"

        return full_prompt