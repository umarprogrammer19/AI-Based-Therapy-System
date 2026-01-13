import httpx
from typing import List, Optional
from ..config.settings import settings
import logging


logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service class for handling vector embeddings and HuggingFace API interactions.
    """

    def __init__(self):
        self.api_key = settings.hugging_face_api_key
        self.api_url = settings.hugging_face_api_url

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the given texts using HuggingFace API.
        """
        if not self.api_key:
            raise ValueError("HUGGING_FACE_API_KEY is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare the payload for the HuggingFace API
        # This is a simplified example - you may need to adjust based on the specific model
        payload = {
            "inputs": texts,
            "options": {
                "wait_for_model": True
            }
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    embeddings = response.json()
                    # Validate that embeddings have the correct dimensions (384)
                    for embedding in embeddings:
                        if len(embedding) != 384:
                            raise ValueError(f"Expected embedding dimension 384, got {len(embedding)}")
                    return embeddings
                elif response.status_code == 401:
                    raise ValueError("Unauthorized: Invalid HuggingFace API key")
                elif response.status_code == 429:
                    raise ValueError("Rate limited: Too many requests to HuggingFace API")
                else:
                    raise ValueError(f"HuggingFace API error: {response.status_code} - {response.text}")

        except httpx.RequestError as e:
            logger.error(f"Request error while generating embeddings: {e}")
            raise ValueError(f"Failed to connect to HuggingFace API: {str(e)}")

    async def get_embedding_for_text(self, text: str) -> List[float]:
        """
        Get a single embedding for a given text.
        """
        embeddings = await self.generate_embeddings([text])
        return embeddings[0] if embeddings else []

    def validate_embedding_dimensions(self, embedding: List[float], expected_dim: int = 384) -> bool:
        """
        Validate that an embedding has the expected dimensions.
        """
        return len(embedding) == expected_dim

    def handle_invalid_api_key(self, error_msg: str):
        """
        Handle invalid/expired API key errors.
        """
        logger.error(f"API key error: {error_msg}")
        # In a real implementation, you might want to trigger a notification or alert
        # to the system administrator that the API key needs to be renewed
        return {"error": "API key is invalid or expired", "message": error_msg}


# Global instance of the service
embedding_service = EmbeddingService()