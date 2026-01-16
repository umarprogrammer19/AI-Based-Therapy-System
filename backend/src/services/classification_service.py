from huggingface_hub import InferenceClient
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClassificationService:
    """
    Service for classifying documents using HuggingFace inference API
    Determines if a document is related to ketamine therapy
    """

    def __init__(self):
        # Get HuggingFace token from environment
        hf_token = os.getenv("HF_API_TOKEN")
        if not hf_token:
            raise ValueError("HF_API_TOKEN environment variable is required")

        self.client = InferenceClient(token=hf_token)
        # Use a suitable model for text classification
        self.model = "mistralai/Mistral-7B-Instruct-v0.1"  # or another appropriate model

    async def classify_document(self, text_sample: str) -> bool:
        """
        Classify if the provided text sample is about ketamine therapy

        Args:
            text_sample: Sample text to classify (e.g., first page of document)

        Returns:
            bool: True if document is ketamine-related, False otherwise
        """
        prompt = f"Is this text about Ketamine Therapy? Answer YES/NO\n\n{text_sample}\n\nAnswer:"

        try:
            response = self.client.text_generation(
                prompt=prompt,
                model=self.model,
                max_new_tokens=10,
                temperature=0.1,
                stop_sequences=["\n"]
            )

            # Extract the answer from the response
            result_text = response.strip().upper()

            # Check if the response contains YES
            if "YES" in result_text:
                return True
            elif "NO" in result_text:
                return False
            else:
                # If the model didn't clearly say YES or NO, default to False for safety
                return False

        except Exception as e:
            print(f"Error during classification: {e}")
            # Default to False in case of error for safety
            return False