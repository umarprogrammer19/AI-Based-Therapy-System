from typing import Dict, Any, List
import httpx
import asyncio
import json
from ..config.settings import settings
from transformers import pipeline
import torch
from huggingface_hub import InferenceApi


class AIService:
    """
    Service for handling AI operations including document classification and embedding generation.
    """

    def __init__(self):
        self.hf_token = settings.hugging_face_api_key
        self.hf_api_url = settings.hugging_face_api_url

    async def classify_document_relevance(self, text_sample: str) -> Dict[str, Any]:
        """
        Classify if the document is related to ketamine therapy using AI.

        Args:
            text_sample: First 500 characters of the document

        Returns:
            Dictionary with classification result and confidence
        """
        if not self.hf_token:
            raise ValueError("Hugging Face API key not configured")

        # Prepare the prompt for classification
        prompt = f"Is this text about Ketamine Therapy? Answer with 'Yes' or 'No' only.\n\n{text_sample}"

        try:
            # Use Hugging Face Inference API with a suitable model
            inference = InferenceApi(
                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                token=self.hf_token
            )

            result = inference(inputs=prompt)

            # Extract the response and determine relevance
            response_text = result[0]['generated_text'] if isinstance(result, list) else str(result)

            # Simple logic to determine if the response indicates relevance
            response_lower = response_text.lower()
            is_relevant = any(word in response_lower for word in ['yes', 'ketamine', 'therapy'])

            return {
                "is_relevant": is_relevant,
                "confidence": 0.8 if is_relevant else 0.2,  # Placeholder confidence
                "reason": response_text[:200],  # First 200 chars as reason
                "raw_response": response_text
            }
        except Exception as e:
            # Fallback classification - if API fails, classify as not relevant for safety
            return {
                "is_relevant": False,
                "confidence": 0.0,
                "reason": f"Classification failed: {str(e)}",
                "raw_response": ""
            }

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks using Hugging Face models.

        Args:
            texts: List of text chunks to embed

        Returns:
            List of embedding vectors
        """
        if not self.hf_token:
            raise ValueError("Hugging Face API key not configured")

        if not texts:
            return []

        try:
            # Use sentence-transformers model for embedding generation
            embedding_pipeline = pipeline(
                "feature-extraction",
                model="sentence-transformers/all-MiniLM-L6-v2",
                device=0 if torch.cuda.is_available() else -1,
                token=self.hf_token,
                batch_size=min(len(texts), 16)  # Process in batches for efficiency
            )

            # Handle empty texts by replacing with placeholder
            processed_texts = [text if text.strip() else "[EMPTY]" for text in texts]

            try:
                # Process all texts in a single batch operation
                embeddings_batch = embedding_pipeline(processed_texts)

                embeddings = []
                for i, embedding in enumerate(embeddings_batch):
                    # Handle the case where individual text might be empty
                    if not texts[i].strip():
                        embeddings.append([0.0] * 384)
                        continue

                    if not embedding or len(embedding) == 0:
                        # Use a zero vector if embedding fails
                        embeddings.append([0.0] * 384)
                        continue

                    # Convert to list of floats and take mean across sequence dimension
                    import numpy as np
                    avg_embedding = np.mean(embedding, axis=0).tolist()
                    embeddings.append(avg_embedding)

                return embeddings
            except Exception as batch_error:
                print(f"Warning: Batch embedding failed, falling back to individual processing: {str(batch_error)}")

                # Fall back to individual processing if batch fails
                embedding_pipeline = pipeline(
                    "feature-extraction",
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    device=0 if torch.cuda.is_available() else -1,
                    token=self.hf_token
                )

                embeddings = []
                for text in texts:
                    # Handle empty text
                    if not text.strip():
                        # Use a zero vector for empty text
                        embeddings.append([0.0] * 384)
                        continue

                    try:
                        # The pipeline returns a 3D array [batch_size, sequence_length, features]
                        # We take the mean to get a single embedding vector per text
                        embedding = embedding_pipeline(text)

                        if not embedding or len(embedding) == 0:
                            # Use a zero vector if embedding fails
                            embeddings.append([0.0] * 384)
                            continue

                        # Convert to list of floats and take mean across sequence dimension
                        import numpy as np
                        avg_embedding = np.mean(embedding[0], axis=0).tolist()
                        embeddings.append(avg_embedding)
                    except Exception as text_error:
                        print(f"Warning: Failed to generate embedding for text chunk: {str(text_error)}")
                        # Use a zero vector as fallback
                        embeddings.append([0.0] * 384)

                return embeddings

        except Exception as e:
            raise ValueError(f"Failed to generate embeddings: {str(e)}")

    async def generate_query_embedding(self, query_text: str) -> List[float]:
        """
        Generate embedding for a query text using Hugging Face models.

        Args:
            query_text: The query text to embed

        Returns:
            Embedding vector as a list of floats
        """
        if not self.hf_token:
            raise ValueError("Hugging Face API key not configured")

        if not query_text or not query_text.strip():
            return [0.0] * 384  # Return zero vector for empty query

        try:
            # Use the same embedding pipeline as for document chunks
            embedding_pipeline = pipeline(
                "feature-extraction",
                model="sentence-transformers/all-MiniLM-L6-v2",
                device=0 if torch.cuda.is_available() else -1,
                token=self.hf_token
            )

            # Generate embedding for the query
            embedding = embedding_pipeline(query_text)

            if not embedding or len(embedding) == 0:
                # Use a zero vector if embedding fails
                return [0.0] * 384

            # Convert to list of floats and take mean across sequence dimension
            import numpy as np
            avg_embedding = np.mean(embedding[0], axis=0).tolist()
            return avg_embedding

        except Exception as e:
            raise ValueError(f"Failed to generate query embedding: {str(e)}")

    async def generate_response_with_context(self, query: str, context_chunks: List[Dict],
                                           system_prompt: str = None) -> Dict[str, Any]:
        """
        Generate a response to a query using provided context chunks.

        Args:
            query: The user's query
            context_chunks: List of context chunks with text and metadata
            system_prompt: Optional system prompt to guide the response

        Returns:
            Dictionary containing the response, confidence score, and metadata
        """
        if not self.hf_token:
            raise ValueError("Hugging Face API key not configured")

        # Build the system prompt if not provided
        if system_prompt is None:
            system_prompt = """You are an AI assistant specialized in ketamine therapy.
            Answer the user's question based on the provided context. If the answer is not in the context,
            politely say you don't know and suggest consulting a healthcare professional."""

        # Build the context from the retrieved chunks
        context_text = "\n\n".join([
            f"Context {i+1}: {chunk.get('text', '')}"
            for i, chunk in enumerate(context_chunks)
        ])

        # Construct the full prompt
        full_prompt = f"""
        <s>[INST] <<SYS>>
        {system_prompt}
        <</SYS>>

        CONTEXT:
        {context_text}

        QUESTION:
        {query}

        Please provide a helpful and accurate response based on the context provided.
        [/INST]
        """

        try:
            # Use Hugging Face Inference API with a suitable model for response generation
            inference = InferenceApi(
                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                token=self.hf_token
            )

            result = inference(
                inputs=full_prompt,
                parameters={
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            )

            # Extract the response text
            if isinstance(result, list) and len(result) > 0:
                response_text = result[0]['generated_text']
            elif isinstance(result, dict) and 'generated_text' in result:
                response_text = result['generated_text']
            else:
                response_text = str(result)

            # Extract just the response part (remove the prompt from the output)
            if "[/INST]" in response_text:
                response_text = response_text.split("[/INST]")[-1].strip()

            # Calculate a basic confidence score based on response characteristics
            confidence = self._calculate_response_confidence(response_text, context_chunks)

            return {
                "response_text": response_text,
                "confidence_score": confidence,
                "metadata": {
                    "model_used": "mistralai/Mistral-7B-Instruct-v0.2",
                    "context_chunks_count": len(context_chunks),
                    "system_prompt_used": system_prompt[:100] + "..." if len(system_prompt) > 100 else system_prompt
                }
            }
        except Exception as e:
            raise ValueError(f"Failed to generate response: {str(e)}")

    def _calculate_response_confidence(self, response_text: str, context_chunks: List[Dict]) -> float:
        """
        Calculate a basic confidence score based on response characteristics.

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
            return 0.2  # Very low confidence if no context was provided

        # Higher confidence with more context chunks (but cap it)
        context_based_confidence = min(0.3 + (len(context_chunks) * 0.15), 0.8)

        # Boost confidence if response seems substantive
        word_count = len(response_text.split())
        length_bonus = min(word_count / 100 * 0.2, 0.2)  # Up to 0.2 bonus for longer responses

        confidence = min(context_based_confidence + length_bonus, 1.0)
        return confidence


# Global instance
ai_service = AIService()