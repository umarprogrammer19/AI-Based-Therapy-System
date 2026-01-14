from typing import Dict, Any, List
import httpx
import asyncio
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


# Global instance
ai_service = AIService()