from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database.connection import get_session
from typing import Optional
import uuid
from datetime import datetime
import os

from ..models.chat_session import ChatSession
from ..models.chat_message import ChatMessage
from ..models.vector_chunk import VectorChunk
from ..services.chat_service import ChatService
from ..services.rag_service import RAGService
from ..utils.embeddings import EmbeddingGenerator


router = APIRouter()

@router.post("/chat")
async def chat(
    message: str,
    session_id: Optional[str] = None,
    db_session: Session = Depends(get_session)
):
    """
    Submit a chat query and receive a response using RAG (Retrieval Augmented Generation)
    """
    # Get or create chat session
    chat_session = None
    if session_id:
        # Try to find existing session
        chat_session = db_session.exec(
            select(ChatSession).where(ChatSession.id == session_id)
        ).first()

    if not chat_session:
        # Create new session
        new_session_id = str(uuid.uuid4())
        chat_session = ChatSession(
            id=new_session_id,
            user_identifier="anonymous"
        )
        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)

    # Create user message record
    user_message = ChatMessage(
        session_id=chat_session.id,
        role="user",
        content=message
    )
    db_session.add(user_message)
    db_session.commit()

    # Use RAG service to retrieve relevant chunks
    rag_service = RAGService()
    relevant_chunks = rag_service.retrieve_relevant_chunks(message, db_session, top_k=3)

    # Check if query is off-topic or if no relevant chunks are found
    if not relevant_chunks:
        # Return a polite refusal as per safety requirements
        response_message = "I'm sorry, but I don't have sufficient information in my knowledge base to answer your question about ketamine therapy. My knowledge is limited to information specifically related to ketamine therapy. Please consult with a qualified healthcare professional for personalized medical advice."

        # Create assistant message record
        assistant_message = ChatMessage(
            session_id=chat_session.id,
            role="assistant",
            content=response_message
        )
        db_session.add(assistant_message)
        db_session.commit()

        return {
            "id": str(assistant_message.id),
            "message": response_message,
            "sessionId": chat_session.id,
            "sources": []
        }

    # Use chat service to generate response with context
    chat_service = ChatService()

    # Construct the full prompt with context
    full_prompt = rag_service.construct_prompt_with_context(message, relevant_chunks)

    # Generate response
    response_text = await chat_service.generate_response(message, relevant_chunks)

    # Create assistant message record
    assistant_message = ChatMessage(
        session_id=chat_session.id,
        role="assistant",
        content=response_text
    )
    db_session.add(assistant_message)
    db_session.commit()

    return {
        "id": str(assistant_message.id),
        "message": response_text,
        "sessionId": chat_session.id,
        "sources": [str(chunk.id) for chunk in relevant_chunks]
    }