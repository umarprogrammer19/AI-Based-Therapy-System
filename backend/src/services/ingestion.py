from fastapi import UploadFile
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import hashlib
import tempfile
import os
from pathlib import Path
from ..models.knowledge_doc import KnowledgeDoc, KnowledgeDocCreate, KnowledgeDocUpdate
from ..models.vector_chunk import VectorChunk, VectorChunkCreate
from ..services.ai import ai_service
from ..services.knowledge_service import knowledge_doc_service
from ..services.vector_service import vector_chunk_service


async def process_uploaded_file(file: UploadFile, session: AsyncSession, user_id: Optional[UUID] = None) -> KnowledgeDoc:
    """
    Process an uploaded file through the ingestion pipeline:
    1. Extract text from file
    2. Classify relevance using AI
    3. If relevant, extract full text, chunk, and embed
    4. If not relevant, save with relevant=False and stop processing
    """
    # Read the file content
    file_content = await file.read()

    # Calculate checksum
    checksum = hashlib.md5(file_content).hexdigest()

    # Get file size
    file_size = len(file_content)

    # Set source based on whether it's a user upload or admin upload
    source = "user_upload" if user_id else "admin_upload"

    # Create a temporary file to handle the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        # Extract first 500 characters for classification
        first_500_chars = await extract_first_n_characters(temp_file_path, file.content_type or "", 500)

        # Classify document relevance
        classification_result = await ai_service.classify_document_relevance(first_500_chars)

        # Create initial KnowledgeDoc with classification results
        knowledge_doc_data = KnowledgeDocCreate(
            filename=file.filename,
            file_size=file_size,
            source=source,
            user_id=user_id,  # Include user_id if provided
            content_type=file.content_type,
            checksum=checksum,
            relevant=classification_result["is_relevant"],
            classification_reason=classification_result["reason"],
            processing_status="classified" if classification_result["is_relevant"] else "skipped"
        )

        knowledge_doc = await knowledge_doc_service.create_knowledge_doc(session, knowledge_doc_data)

        # If document is not relevant, stop processing
        if not classification_result["is_relevant"]:
            knowledge_doc_update = KnowledgeDocUpdate(processing_status="skipped")
            knowledge_doc = await knowledge_doc_service.update_knowledge_doc(
                session,
                knowledge_doc.id,
                knowledge_doc_update
            )
            return knowledge_doc

        # If document is relevant, continue with full processing
        knowledge_doc_update_processing = KnowledgeDocUpdate(processing_status="processing")
        knowledge_doc = await knowledge_doc_service.update_knowledge_doc(
            session,
            knowledge_doc.id,
            knowledge_doc_update_processing
        )

        # Extract full text content
        full_text = await extract_full_text(temp_file_path, file.content_type or "")

        # Split text into chunks of ~500 characters
        text_chunks = chunk_text(full_text, max_chunk_size=500)

        # Generate embeddings for each chunk
        embeddings = ai_service.generate_embeddings(text_chunks)

        # Create VectorChunk records
        for idx in range(min(len(text_chunks), len(embeddings))):
            chunk_text_content = text_chunks[idx]
            embedding = embeddings[idx]

            vector_chunk = VectorChunkCreate(
                knowledge_doc_id=knowledge_doc.id,
                text_content=chunk_text_content,
                embedding=embedding,
                chunk_index=idx
            )
            await vector_chunk_service.create_vector_chunk(session, vector_chunk)

        # Update processing status to completed
        knowledge_doc_update_completed = KnowledgeDocUpdate(processing_status="completed")
        knowledge_doc = await knowledge_doc_service.update_knowledge_doc(
            session,
            knowledge_doc.id,
            knowledge_doc_update_completed
        )

        return knowledge_doc

    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


async def extract_first_n_characters(file_path: str, content_type: str, n: int = 500) -> str:
    """
    Extract the first n characters from a file based on its type.
    """
    full_text = await extract_full_text(file_path, content_type)
    return full_text[:n]


async def extract_full_text(file_path: str, content_type: str) -> str:
    """
    Extract full text content from a file based on its type.
    """
    if content_type == "text/plain" or content_type == "text/txt" or file_path.endswith(('.txt', '.text')):
        # Handle plain text files
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        # For other file types (PDF, DOCX), return a mock content
        # In a real implementation, we would process these files properly
        if file_path.endswith('.pdf'):
            return f"Mock content extracted from PDF file: {os.path.basename(file_path)}. This is a placeholder for actual PDF content extraction."
        elif file_path.endswith('.docx'):
            return f"Mock content extracted from DOCX file: {os.path.basename(file_path)}. This is a placeholder for actual DOCX content extraction."
        else:
            # Default to text file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, try with latin-1
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()


def chunk_text(text: str, max_chunk_size: int = 500) -> list:
    """
    Split text into chunks of approximately max_chunk_size characters,
    trying to respect sentence boundaries when possible.
    """
    if not text or len(text.strip()) == 0:
        return []

    chunks = []
    current_pos = 0

    while current_pos < len(text):
        # Determine the end position for this chunk
        end_pos = current_pos + max_chunk_size

        # If we're at the end of the text, take whatever is left
        if end_pos >= len(text):
            chunk = text[current_pos:].strip()
            if chunk:
                chunks.append(chunk)
            break

        # Try to find a sentence boundary near the end of our chunk
        chunk_end = text.rfind('.', current_pos, end_pos)

        # If no sentence boundary found, try for a paragraph break
        if chunk_end <= current_pos:
            chunk_end = text.rfind('\n', current_pos, end_pos)

        # If no paragraph break, try for a space
        if chunk_end <= current_pos:
            chunk_end = text.rfind(' ', current_pos, end_pos)

        # If still nothing found, just cut at max_chunk_size
        if chunk_end <= current_pos:
            chunk_end = end_pos

        # Extract the chunk and add if not empty
        chunk = text[current_pos:chunk_end].strip()
        if chunk:
            chunks.append(chunk)

        # Move to the next position
        current_pos = chunk_end

        # Skip past any whitespace
        while current_pos < len(text) and text[current_pos].isspace():
            current_pos += 1

    return chunks