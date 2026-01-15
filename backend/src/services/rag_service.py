from sqlmodel import Session, select
from sqlalchemy import func, text
from typing import List
import uuid
from ..models.vector_chunk import VectorChunk
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
            SELECT * FROM vector_chunks
            ORDER BY embedding <-> :embedding
            LIMIT :limit
        """)

        result = session.exec(
            sql,
            params={"embedding": embedding_str, "limit": top_k}
        )

        chunks = result.all()

        # Convert the raw results to VectorChunk objects
        # Since SQLModel doesn't directly support the vector operations in queries yet,
        # we'll fetch the IDs and query again using SQLModel for proper object mapping
        chunk_ids = [chunk[0] for chunk in chunks]  # Assuming first column is id

        # Better approach: use a more direct SQLModel-compatible query
        # Since we need to use the vector similarity, we'll execute raw SQL but return proper objects
        sql_with_objects = text("""
            SELECT id, knowledge_doc_id, text_content, chunk_index, created_at, updated_at
            FROM vector_chunks
            ORDER BY embedding <-> :embedding
            LIMIT :limit
        """)

        result = session.exec(
            sql_with_objects,
            params={"embedding": embedding_str, "limit": top_k}
        )

        # For now, we'll implement a hybrid approach that works with SQLModel
        # Get all chunks and calculate similarity in Python (inefficient but works)
        all_chunks = session.exec(select(VectorChunk)).all()

        # Calculate similarity scores (cosine similarity)
        chunk_similarities = []
        query_vec = np.array(query_embedding)

        for chunk in all_chunks:
            if chunk.embedding:
                chunk_vec = np.array(chunk.embedding)

                # Calculate cosine similarity
                # For pgvector, we can use the negative L2 distance as a proxy for cosine similarity
                # Or calculate it directly:
                dot_product = np.dot(query_vec, chunk_vec)
                norms = np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec)

                if norms == 0:
                    similarity = 0
                else:
                    similarity = dot_product / norms

                chunk_similarities.append((chunk, similarity))

        # Sort by similarity score in descending order and return top_k
        chunk_similarities.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [chunk_similarity[0] for chunk_similarity in chunk_similarities[:top_k]]

        return top_chunks

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