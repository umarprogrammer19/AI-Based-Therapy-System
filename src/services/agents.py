from huggingface_hub import InferenceClient
from src.core.config import settings

client = InferenceClient(
    model="mistralai/Mistral-Large-Instruct-2407", token=settings.HF_TOKEN
)


def generate_ketamine_response(message: str, persona: str, context: str) -> str:
    """
    Specialized Al focused only on ketamine-related therapy conversations.
    """
    system_prompt = (
        f"You are a specialized AI for ketamine therapy. Adopt this persona: {persona}. "
        f"Answer using ONLY the provided context. If the context does not contain the answer, "
        f"state that you do not know. \n\nContext: {context}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    response = client.chat_completion(
        messages=messages, max_tokens=500, temperature=0.5
    )
    return response.choices[0].message.content.strip()


def generate_general_response(message: str, persona: str) -> str:
    """
    A broader Al therapist handling general mental health topics.
    """
    system_prompt = (
        f"You are a general AI therapist. Adopt this persona: {persona}. "
        f"Do not provide advice specifically about ketamine; you should not be "
        f"contaminated with ketamine-specific data."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    response = client.chat_completion(
        messages=messages, max_tokens=500, temperature=0.7
    )
    return response.choices[0].message.content.strip()
