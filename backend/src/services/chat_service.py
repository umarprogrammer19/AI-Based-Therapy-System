from huggingface_hub import InferenceClient
from typing import List
import os
from dotenv import load_dotenv
from ..models.vector_chunk import VectorChunk


class ChatService:
    """
    Service for handling chat conversations, including generation
    """

    def __init__(self):
        load_dotenv()

        # Get HuggingFace token from environment
        hf_token = os.getenv("HF_API_TOKEN")
        if not hf_token:
            raise ValueError("HF_API_TOKEN environment variable is required")

        self.client = InferenceClient(token=hf_token)
        # Use a suitable model for text generation
        self.model = "mistralai/Mistral-7B-Instruct-v0.1"  # or another appropriate model

    async def generate_response(self, full_prompt: str) -> str:
        """
        Generate a response using Mistral

        Args:
            full_prompt: Complete prompt with system message, context, and user query

        Returns:
            Generated response text
        """
        try:
            response = self.client.text_generation(
                prompt=full_prompt,
                model=self.model,
                max_new_tokens=200,
                temperature=0.7,
                stop_sequences=["\nUser:", "\nAssistant:", "</s>"]
            )

            # Extract the response part (remove the prompt)
            response_text = response.strip()

            # Ensure we return only the assistant's response
            if "Assistant:" in response_text:
                response_text = response_text.split("Assistant:")[-1].strip()

            return response_text

        except Exception as e:
            print(f"Error during response generation: {e}")
            return "I'm sorry, but I encountered an error while processing your request. Please try again later."