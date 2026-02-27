from huggingface_hub import InferenceClient
from src.core.config import settings

client = InferenceClient(model="mistralai/Mistral-Large-Instruct-2407", token=settings.HF_TOKEN)

def detect_intent(message: str) -> str:
    """
    Determines if the conversation content is explicitly about ketamine therapy [cite: 18]
    or general mental health[cite: 21].
    """
    system_prompt = (
        "Analyze the user's message. If it explicitly mentions ketamine therapy, "
        "experiences, or protocols, output EXACTLY 'KETAMINE'. "
        "If it is about general mental health, output EXACTLY 'GENERAL'."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat_completion(messages=messages, max_tokens=10, temperature=0.1)
    decision = response.choices[0].message.content.strip().upper()
    
    return "KETAMINE" if "KETAMINE" in decision else "GENERAL"