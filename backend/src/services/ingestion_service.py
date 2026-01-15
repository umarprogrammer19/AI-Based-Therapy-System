from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import UploadFile, HTTPException
from typing import List
import uuid
from datetime import datetime
import hashlib

from .classification_service import ClassificationService
from ..utils.text_extractor import TextExtractor
from ..utils.embeddings import EmbeddingGenerator
from ..models.knowledge_doc import KnowledgeDoc


class IngestionService:
    """
    Service for handling the complete document ingestion pipeline:
    1. Upload and extract text
    2. Classify document as ketamine-related or not
    3. If related: chunk, embed, and store in vector database
    4. If not related: store metadata only
    """

    def __init__(self):
        self.classification_service = ClassificationService()
        self.text_extractor = TextExtractor()
        self.embedding_generator = EmbeddingGenerator()

    async def process_upload(self, file: UploadFile, uploader_id: str, session: AsyncSession) -> dict:
        """
        Process an uploaded document through the complete ingestion pipeline

        Args:
            file: Uploaded file
            uploader_id: ID of the user who uploaded the file
            session: Database session

        Returns:
            dict: Result of the processing with document ID and status
        """
        # Read the file content
        file_content = await file.read()

        # Generate content hash for deduplication
        checksum = hashlib.sha256(file_content).hexdigest()

        # Check if document with same content already exists
        result = await session.execute(
            select(KnowledgeDoc).where(KnowledgeDoc.checksum == checksum)
        )
        existing_doc = result.scalar_one_or_none()

        if existing_doc:
            return {
                "id": str(existing_doc.id),
                "filename": existing_doc.filename,
                "status": "duplicate",
                "isKetamineRelevant": existing_doc.relevant,
                "message": f"Document with same content already exists as {existing_doc.id}"
            }

        # Extract file extension
        file_extension = '.' + file.filename.split('.')[-1].lower()

        # Extract text from the document
        extracted_text = self.text_extractor.extract_text(file_content, file_extension)

        # Get first page/chunk for classification
        first_page_text = extracted_text[:1000]  # First 1000 characters for classification

        # Classify the document
        is_ketamine_related = await self.classification_service.classify_document(first_page_text)

        # Create KnowledgeDoc record
        knowledge_doc = KnowledgeDoc(
            filename=file.filename,
            file_size=len(file_content),
            source=uploader_id,
            checksum=checksum,
            relevant=is_ketamine_related,
            processing_status="classified" if is_ketamine_related else "skipped"
        )

        session.add(knowledge_doc)
        await session.commit()
        await session.refresh(knowledge_doc)

        # If the document is ketamine-related, process it for RAG
        if is_ketamine_related:
            # Update processing status
            knowledge_doc.processing_status = "processing"
            session.add(knowledge_doc)

            # Chunk the full text
            text_chunks = self.embedding_generator.chunk_text(extracted_text, chunk_size=500)

            # Process each chunk
            for idx in range(len(text_chunks)):
                chunk_text = text_chunks[idx]
                # Generate embedding for the chunk
                embedding = self.embedding_generator.generate_embedding(chunk_text)

                # Import VectorChunk here to avoid circular imports
                from ..models.vector_chunk import VectorChunk

                # Create VectorChunk record
                vector_chunk = VectorChunk(
                    knowledge_doc_id=knowledge_doc.id,
                    text_content=chunk_text,
                    embedding=embedding,
                    chunk_index=idx
                )

                session.add(vector_chunk)

            # Update final status
            knowledge_doc.processing_status = "completed"
            session.add(knowledge_doc)
            await session.commit()

        return {
            "id": str(knowledge_doc.id),
            "filename": knowledge_doc.filename,
            "status": "processed",
            "isKetamineRelevant": is_ketamine_related,
            "message": f"Document processed successfully. Ketamine-related: {is_ketamine_related}"
        }