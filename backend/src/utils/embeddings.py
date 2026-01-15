from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    """
    Utility class to generate embeddings for text chunks using sentence transformers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator with a pre-trained model

        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to generate embedding for

        Returns:
            List[float]: Embedding vector as a list of floats
        """
        embedding = self.model.encode([text])
        # Convert to list of floats for JSON serialization
        return embedding[0].tolist()

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = self.model.encode(texts)
        # Convert to list of lists of floats for JSON serialization
        return [emb.tolist() for emb in embeddings]

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into overlapping chunks of specified size

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters

        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)

        return chunks