from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Dict, Any, Optional
from uuid import UUID
import logging

from ...database.session import get_session
from ...services.chat import chat_service
from ...models.chat_query import ChatQueryCreate

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=Dict[str, Any])
async def chat_endpoint(
    query_data: Dict[str, Any],
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Chat endpoint that accepts user queries and returns AI-generated responses
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
        user_id = query_data.get("user_id", "anonymous")
        session_id = query_data.get("session_id")

        # Process the chat query through the RAG pipeline
        result = await chat_service.process_chat_query(
            session=session,
            query_text=query_text,
            user_id=str(user_id),
            session_id=session_id
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


@router.get("/history/{user_id}", response_model=list)
async def get_chat_history(
    user_id: str,
    session_id: Optional[str] = None,
    limit: int = 10,
    session: Session = Depends(get_session)
) -> list:
    """
    Retrieve chat history for a specific user.

    Args:
        user_id: ID of the user to retrieve history for
        session_id: Optional session ID to filter by specific session
        limit: Maximum number of conversations to return (default: 10)
        session: Database session

    Returns:
        List of chat interactions with query and response
    """
    try:
        # Validate user_id
        if not user_id or not user_id.strip():
            raise HTTPException(status_code=400, detail="User ID is required")

        # Limit the number of items that can be retrieved
        if limit > 100:
            limit = 100

        # Get chat history from the service
        history = await chat_service.get_chat_history(
            session=session,
            user_id=user_id,
            session_id=session_id,
            limit=limit
        )

        return history

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving chat history for user {user_id}: {str(e)}", exc_info=True)

        # Raise a generic internal server error
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while retrieving chat history"
        )