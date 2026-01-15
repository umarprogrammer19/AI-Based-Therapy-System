from typing import Dict, Any, List, Optional
from uuid import UUID
import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.chat_query import ChatQuery, ChatQueryCreate
from ..models.chat_response import ChatResponse, ChatResponseCreate
from ..services.ai import ai_service
from ..services.vector_service import vector_chunk_service
from datetime import datetime


class ChatService:
    """
    Service class for handling chat interactions with RAG (Retrieval Augmented Generation).
    """

    def __init__(self):
        self.ai_service = ai_service
        self.vector_service = vector_chunk_service

    async def process_chat_query(
        self,
        session: AsyncSession,
        query_text: str,
        user_id: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat query through the full RAG pipeline:
        1. Store the query in the database
        2. Check if the query is off-topic using guardrails
        3. Generate query embedding
        4. Retrieve relevant context from vector database
        5. Generate response using AI with context
        6. Store the response in the database

        Args:
            session: Database session
            query_text: The user's query text
            user_id: ID of the user submitting the query
            session_id: Optional session identifier for conversation continuity

        Returns:
            Dictionary containing the response and metadata
        """
        start_time = datetime.utcnow()

        # 1. Store the initial query in the database
        chat_query_create = ChatQueryCreate(
            user_id=user_id,
            query_text=query_text,
            session_id=session_id,
            is_off_topic=None,  # Will be set after guardrail check
            retrieved_context_ids=None,  # Will be set after context retrieval
            query_metadata={"processing_stage": "received"}
        )

        chat_query = ChatQuery.model_validate(chat_query_create)
        session.add(chat_query)
        await session.commit()
        await session.refresh(chat_query)

        # Store the query ID to avoid lazy loading issues later
        query_id = chat_query.id

        try:
            # 2. Check if the query is off-topic using guardrails
            is_off_topic = await self._check_if_off_topic(query_text)

            # Update the query record with off-topic status
            chat_query.is_off_topic = is_off_topic
            chat_query.query_metadata = {"processing_stage": "guardrail_checked", "is_off_topic": is_off_topic}
            session.add(chat_query)
            await session.commit()

            # If the query is off-topic, return a predefined response
            if is_off_topic:
                response_text = (
                    "I'm sorry, but your query appears to be outside the scope of ketamine therapy topics. "
                    "I can only provide information related to ketamine therapy, its applications, "
                    "benefits, risks, and related medical information. "
                    "Please ask a question related to ketamine therapy or consult with a healthcare professional for other matters."
                )

                chat_response_create = ChatResponseCreate(
                    chat_query_id=query_id,
                    response_text=response_text,
                    confidence_score=0.9,  # High confidence in off-topic response
                    used_context_ids=[],
                    generation_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                    metadata={"response_type": "off_topic_guardrail"}
                )

                chat_response = ChatResponse.model_validate(chat_response_create)
                session.add(chat_response)
                await session.commit()
                await session.refresh(chat_response)

                # Store the response ID to avoid lazy loading issues later
                response_id = chat_response.id

                return {
                    "message": response_text,
                    "query_id": str(query_id),
                    "response_id": str(response_id),
                    "confidence": 0.9,
                    "context_used": [],
                    "is_off_topic": True,
                    "timestamp": datetime.utcnow().isoformat()
                }

            # 3. Generate query embedding
            query_embedding = await self.ai_service.generate_query_embedding(query_text)

            # Update the query record with the embedding
            chat_query.query_embedding = query_embedding
            session.add(chat_query)
            await session.commit()

            # 4. Retrieve relevant context from vector database
            context_chunks_with_scores = await self.vector_service.search_similar_vectors(
                session=session,
                query_embedding=query_embedding,
                limit=5  # Retrieve top 5 most similar chunks
            )

            # Extract the context chunks and prepare for response generation
            context_chunks = []
            retrieved_context_ids = []

            for chunk_read, similarity_score in context_chunks_with_scores:
                context_chunks.append({
                    "text": chunk_read.text_content,
                    "chunk_id": str(chunk_read.id),
                    "similarity_score": similarity_score
                })
                retrieved_context_ids.append(chunk_read.id)

            # Update the query record with retrieved context IDs
            chat_query.retrieved_context_ids = retrieved_context_ids
            session.add(chat_query)
            await session.commit()

            # 5. Generate response using AI with context
            response_result = await self.ai_service.generate_response_with_context(
                query=query_text,
                context_chunks=context_chunks
            )

            # 6. Store the response in the database
            chat_response_create = ChatResponseCreate(
                chat_query_id=query_id,
                response_text=response_result["response_text"],
                confidence_score=response_result["confidence_score"],
                used_context_ids=retrieved_context_ids,
                generation_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                response_metadata=response_result["metadata"]
            )

            chat_response = ChatResponse.model_validate(chat_response_create)
            session.add(chat_response)
            await session.commit()
            await session.refresh(chat_response)

            # Store the response ID to avoid lazy loading issues later
            response_id = chat_response.id

            # Prepare the response for the API
            context_used = [
                {
                    "chunk_id": str(chunk["chunk_id"]),
                    "text_preview": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                    "similarity_score": chunk["similarity_score"]
                }
                for chunk in context_chunks
            ]

            return {
                "message": response_result["response_text"],
                "query_id": str(query_id),
                "response_id": str(response_id),
                "confidence": response_result["confidence_score"],
                "context_used": context_used,
                "is_off_topic": False,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            # Handle any errors during processing
            error_message = f"An error occurred while processing your query: {str(e)}"

            # Store error response in the database - use the query_id if available
            try:
                chat_query_id_to_use = query_id
            except NameError:
                # If query_id wasn't set (error happened before initial commit), we need to save the query first
                # This shouldn't happen since query_id is set right after the first commit, but just in case
                chat_query_id_to_use = chat_query.id if hasattr(chat_query, 'id') and chat_query.id else None

            if chat_query_id_to_use:
                chat_response_create = ChatResponseCreate(
                    chat_query_id=chat_query_id_to_use,
                    response_text=error_message,
                    confidence_score=0.0,
                    used_context_ids=[],
                    generation_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                    response_metadata={"error": str(e)}
                )

                chat_response = ChatResponse.model_validate(chat_response_create)
                session.add(chat_response)
                await session.commit()
                await session.refresh(chat_response)

            raise e

    async def _check_if_off_topic(self, query_text: str) -> bool:
        """
        Check if the query is off-topic using AI classification.

        Args:
            query_text: The query text to check

        Returns:
            Boolean indicating if the query is off-topic
        """
        # Define topics related to ketamine therapy for classification
        relevant_topics = [
            "ketamine therapy", "ketamine treatment", "depression treatment",
            "mental health", "treatment-resistant depression", "TRD",
            "infusion therapy", "psychiatric treatment", "anxiety",
            "PTSD", "suicidal ideation", "mood disorders", "NMDA receptor"
        ]

        # Create a prompt for the AI to classify the query
        prompt = f"""
        Is the following query related to ketamine therapy or mental health treatment?
        Relevant topics include: {', '.join(relevant_topics)}

        Query: "{query_text}"

        Respond with ONLY "YES" if it's related or "NO" if it's not related.
        """

        try:
            # Use the AI service to classify the query
            # For now, we'll use a simple keyword-based approach as a fallback
            query_lower = query_text.lower()

            # Check for relevant keywords
            has_relevant_keyword = any(topic.lower() in query_lower for topic in relevant_topics)

            # Also check for common mental health terms
            mental_health_terms = ["depression", "anxiety", "therapy", "treatment", "mental health",
                                 "psychiatry", "psychological", "mood", "suicide", "ptsd", "trauma"]
            has_mental_health_term = any(term in query_lower for term in mental_health_terms)

            # Check for ketamine-specific terms
            ketamine_terms = ["ketamine", "spravato", " esketamine", "nmda"]
            has_ketamine_term = any(term in query_lower for term in ketamine_terms)

            # If any relevant terms are found, it's on-topic
            is_on_topic = has_relevant_keyword or has_mental_health_term or has_ketamine_term

            # Additional check: if it contains many off-topic keywords, mark as off-topic
            off_topic_keywords = [
                "cooking", "sports", "gaming", "movie", "celebrity", "entertainment",
                "finance", "stock", "cryptocurrency", "weather", "news", "politics"
            ]
            has_off_topic_keyword = any(keyword in query_lower for keyword in off_topic_keywords)

            if has_off_topic_keyword and not is_on_topic:
                return True  # Off-topic

            return not is_on_topic  # Return True if off-topic (not on-topic)
        except Exception:
            # If classification fails, assume it's on-topic to be safe
            return False

    async def get_chat_history(
        self,
        session: AsyncSession,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a user or specific session.

        Args:
            session: Database session
            user_id: ID of the user
            session_id: Optional session identifier to filter by session
            limit: Maximum number of conversations to return

        Returns:
            List of chat interactions with query and response
        """
        from sqlmodel import select

        # Build query for chat queries
        query_stmt = select(ChatQuery).where(ChatQuery.user_id == user_id)

        if session_id:
            query_stmt = query_stmt.where(ChatQuery.session_id == session_id)

        query_stmt = query_stmt.order_by(ChatQuery.timestamp.desc()).limit(limit)

        result = await session.execute(query_stmt)
        queries = result.all()

        history = []
        for query in queries:
            # Get the corresponding response if it exists
            response_stmt = select(ChatResponse).where(ChatResponse.chat_query_id == query.id)
            result = await session.execute(response_stmt)
            response = result.first()

            history_item = {
                "query_id": str(query.id),
                "query_text": query.query_text,
                "timestamp": query.timestamp.isoformat(),
                "is_off_topic": query.is_off_topic
            }

            if response:
                history_item["response_text"] = response.response_text
                history_item["response_id"] = str(response.id)
                history_item["confidence"] = response.confidence_score

            history.append(history_item)

        return history


# Global instance of the chat service
chat_service = ChatService()