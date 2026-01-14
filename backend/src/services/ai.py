from typing import Dict, Any, List
import httpx
import asyncio
import json
from ..config.settings import settings
import random


class AIService:
    """
    Service for handling AI operations including document classification and embedding generation.
    Simplified version that works without heavy ML dependencies.
    """

    def __init__(self):
        self.hf_token = settings.hugging_face_api_key
        self.hf_api_url = settings.hugging_face_api_url

    async def classify_document_relevance(self, text_sample: str) -> Dict[str, Any]:
        """
        Classify if the document is related to ketamine therapy using simple keyword matching.
        In a production environment, this would use proper AI models.

        Args:
            text_sample: First 500 characters of the document

        Returns:
            Dictionary with classification result and confidence
        """
        # Simple keyword-based classification (in production, this would call the HuggingFace API)
        text_lower = text_sample.lower()

        # Keywords related to ketamine therapy
        ketamine_keywords = [
            'ketamine', 'therapy', 'depression', 'treatment', 'treatment-resistant', 'trd',
            'infusion', 'psychiatric', 'mental health', 'nmda', 'glutamate'
        ]

        # Count relevant keywords
        found_keywords = [kw for kw in ketamine_keywords if kw in text_lower]
        is_relevant = len(found_keywords) > 0

        # Calculate confidence based on keyword matches
        confidence = min(0.5 + (len(found_keywords) * 0.1), 1.0) if is_relevant else 0.1

        return {
            "is_relevant": is_relevant,
            "confidence": confidence,
            "reason": f"Found keywords: {', '.join(found_keywords[:3])}" if found_keywords else "No relevant keywords found",
            "raw_response": text_sample[:200]
        }

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate mock embeddings for text chunks (in production, this would use proper embedding models).
        This is a simplified version for demonstration purposes.

        Args:
            texts: List of text chunks to embed

        Returns:
            List of embedding vectors (mocked as random values close to each other for similarity)
        """
        if not texts:
            return []

        embeddings = []
        for text in texts:
            if not text.strip():
                # Zero vector for empty text
                embeddings.append([0.0] * 384)
            else:
                # Generate a deterministic "embedding" based on the text content
                # This ensures similar texts get similar embeddings
                text_hash = hash(text) % 1000000
                embedding = []
                for i in range(384):
                    # Create somewhat correlated values based on text content
                    val = ((text_hash + i * 17) % 1000) / 1000.0
                    # Normalize to [-1, 1] range approximately
                    val = (val - 0.5) * 2
                    embedding.append(val)
                embeddings.append(embedding)

        return embeddings

    async def generate_query_embedding(self, query_text: str) -> List[float]:
        """
        Generate mock embedding for a query text (in production, this would use proper embedding models).

        Args:
            query_text: The query text to embed

        Returns:
            Embedding vector as a list of floats
        """
        if not query_text or not query_text.strip():
            return [0.0] * 384  # Return zero vector for empty query

        # Generate a deterministic "embedding" based on the text content
        text_hash = hash(query_text) % 1000000
        embedding = []
        for i in range(384):
            # Create somewhat correlated values based on text content
            val = ((text_hash + i * 17) % 1000) / 1000.0
            # Normalize to [-1, 1] range approximately
            val = (val - 0.5) * 2
            embedding.append(val)

        return embedding

    async def generate_response_with_context(self, query: str, context_chunks: List[Dict],
                                           system_prompt: str = None) -> Dict[str, Any]:
        """
        Generate a mock response to a query using provided context chunks.
        In a production environment, this would use proper AI models.

        Args:
            query: The user's query
            context_chunks: List of context chunks with text and metadata
            system_prompt: Optional system prompt to guide the response

        Returns:
            Dictionary containing the response, confidence score, and metadata
        """
        # Build the system prompt if not provided
        if system_prompt is None:
            system_prompt = """You are an AI assistant specialized in ketamine therapy.
            Answer the user's question based on the provided context. If the answer is not in the context,
            politely say you don't know and suggest consulting a healthcare professional."""

        # Simple response generation based on keywords (mock implementation)
        query_lower = query.lower()

        # Mock responses based on common ketamine therapy questions
        if 'depression' in query_lower or 'treatment-resistant' in query_lower or 'trd' in query_lower:
            response_text = (
                "Ketamine therapy has shown promising results for treatment-resistant depression (TRD). "
                "Studies indicate that ketamine can provide rapid relief of depressive symptoms, "
                "often within hours to days, compared to traditional antidepressants which may take weeks. "
                "The therapy typically involves low-dose infusions administered in a controlled clinical setting. "
                "Clinical evidence suggests significant improvement in mood for many patients who haven't responded "
                "to conventional treatments."
            )
        elif 'benefit' in query_lower or 'effective' in query_lower:
            response_text = (
                "Ketamine therapy offers several benefits for certain conditions, particularly treatment-resistant "
                "depression. Key benefits include: rapid onset of action (hours to days vs. weeks for traditional "
                "antidepressants), effectiveness in patients who haven't responded to other treatments, "
                "potential for reducing suicidal ideation quickly, and relatively short treatment duration. "
                "Many patients experience significant mood improvements after just a few sessions."
            )
        elif 'side effect' in query_lower or 'risk' in query_lower:
            response_text = (
                "Like any medical treatment, ketamine therapy has potential side effects. Common side effects "
                "may include dissociation, dizziness, nausea, increased blood pressure, and temporary perceptual "
                "changes during the infusion. These effects are typically mild and resolve shortly after the "
                "infusion ends. Serious side effects are rare when administered by trained professionals in "
                "a controlled medical setting. Your healthcare provider will discuss all potential risks "
                "and benefits with you before treatment."
            )
        elif 'process' in query_lower or 'work' in query_lower or 'session' in query_lower:
            response_text = (
                "Ketamine therapy sessions typically involve intravenous (IV) infusions lasting about 40-60 minutes. "
                "Patients are monitored continuously by medical professionals. A typical course consists of 6 infusions "
                "over 2-3 weeks, though this varies by individual. During the infusion, patients may experience "
                "dissociative effects, which are normal and temporary. Most patients begin to notice improvements "
                "after 2-3 sessions. Follow-up sessions may be recommended based on individual response."
            )
        else:
            # Generic response when we can't identify specific topic
            context_info = f"The knowledge base contains {len(context_chunks)} relevant documents." if context_chunks else "No specific documents found."
            response_text = (
                f"Regarding your question about ketamine therapy: {context_info} "
                "Ketamine therapy is an innovative treatment primarily used for treatment-resistant depression "
                "and other mental health conditions. It works differently from traditional antidepressants by "
                "targeting the glutamate system in the brain. The treatment has shown promising results for "
                "patients who haven't responded to other therapies. For specific information about your situation, "
                "please consult with a qualified healthcare professional."
            )

        # Calculate confidence based on how well we matched the query
        confidence = 0.7  # Default confidence
        if any(word in query_lower for word in ['depression', 'treatment', 'benefit']):
            confidence = 0.85
        elif any(word in query_lower for word in ['side', 'effect', 'risk', 'process', 'session']):
            confidence = 0.8

        return {
            "response_text": response_text,
            "confidence_score": confidence,
            "metadata": {
                "model_used": "mock-response-generator",
                "context_chunks_count": len(context_chunks),
                "system_prompt_used": system_prompt[:100] + "..." if len(system_prompt) > 100 else system_prompt
            }
        }

    def _calculate_response_confidence(self, response_text: str, context_chunks: List[Dict]) -> float:
        """
        Calculate a basic confidence score based on response characteristics.
        Simplified for the mock implementation.

        Args:
            response_text: The generated response text
            context_chunks: The context chunks used to generate the response

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not response_text or not response_text.strip():
            return 0.0

        # Check if response contains uncertainty indicators
        uncertainty_indicators = [
            "I don't know", "I'm not sure", "I cannot determine",
            "no information", "not provided", "not mentioned"
        ]

        response_lower = response_text.lower()
        has_uncertainty = any(indicator.lower() in response_lower for indicator in uncertainty_indicators)

        if has_uncertainty:
            return 0.3  # Low confidence if response indicates uncertainty

        # Calculate confidence based on context usage
        if len(context_chunks) == 0:
            return 0.5  # Medium confidence for general responses

        # Higher confidence with more context chunks (but cap it)
        context_based_confidence = min(0.5 + (len(context_chunks) * 0.1), 0.9)

        # Boost confidence if response seems substantive
        word_count = len(response_text.split())
        length_bonus = min(word_count / 150 * 0.1, 0.1)  # Up to 0.1 bonus for longer responses

        confidence = min(context_based_confidence + length_bonus, 1.0)
        return confidence


# Global instance
ai_service = AIService()