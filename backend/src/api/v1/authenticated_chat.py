from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Dict, Any, Optional
from uuid import UUID
import logging

from ..config.database import get_session
from ..services.chat import chat_service
from ..models.chat_query import ChatQueryCreate
from ..models.user import User
from ..services.auth import auth_service

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
async def authenticated_chat_endpoint(
    query_data: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Authenticated chat endpoint that accepts user queries and returns AI-generated responses
    based on the ketamine therapy knowledge base.

    Implements guardrails to detect off-topic queries and retrieves relevant
    context from vector database before generating responses.
    """
    try:
        # Validate required fields
        if "query" not in query_data or not query_data["query"].strip():
            raise HTTPException(status_code=400, detail="Query is required and cannot be empty")

        query_text = query_data["query"]

        # Limit query length
        if len(query_text) > 1000:
            raise HTTPException(status_code=400, detail="Query must be less than 1000 characters")

        # Extract optional fields
        user_id = str(current_user.id)  # Use authenticated user ID
        session_id = query_data.get("session_id")
        chat_session_id = query_data.get("chat_session_id")  # May be a UUID

        # Convert chat_session_id to UUID if provided as string
        if chat_session_id and isinstance(chat_session_id, str):
            try:
                chat_session_id = UUID(chat_session_id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid chat_session_id format")

        # Process the chat query through the RAG pipeline
        result = await chat_service.process_chat_query(
            session=session,
            query_text=query_text,
            user_id=user_id,
            session_id=session_id,
            chat_session_id=chat_session_id
        )

        # Log successful query processing
        logger.info(f"Processed chat query for user {user_id}. Query ID: {result['query_id']}")

        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error processing chat query: {str(e)}", exc_info=True)

        # Raise a generic internal server error
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your query"
        )


@router.get("/history", response_model=list)
async def get_user_chat_history(
    current_user: User = Depends(auth_service.get_current_user),
    session_id: Optional[str] = None,
    limit: int = 10,
    session: Session = Depends(get_session)
) -> list:
    """
    Retrieve chat history for the authenticated user.
    """
    try:
        # Limit the number of items that can be retrieved
        if limit > 100:
            limit = 100

        # Get chat history from the service
        # Note: This would need to be implemented in the chat_service
        # For now, we'll use the existing get_chat_history method
        history = await chat_service.get_chat_history(
            session=session,
            user_id=str(current_user.id),
            session_id=session_id,
            limit=limit
        )

        return history

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving chat history for user {current_user.id}: {str(e)}", exc_info=True)

        # Raise a generic internal server error
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while retrieving chat history"
        )