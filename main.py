from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
import os

app = FastAPI(title="AI Therapy System Orchestrator")

# Initialize Hugging Face Client for Mistral Large
# Ensure you have your HF_TOKEN set in your environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(model="mistralai/Mistral-Large-Instruct-2407", token=HF_TOKEN)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str
    persona: str = "Calm and empathetic therapist" # Default persona

class ChatResponse(BaseModel):
    routed_to: str
    response: str

# --- Core Logic Functions ---

def detect_intent(message: str) -> str:
    """
    Orchestrator Agent: Determines which model should handle the request.
    """
    system_prompt = (
        "You are an intent detection classifier for a therapy routing system. "
        "Analyze the user's message. If the message explicitly mentions or is "
        "about ketamine therapy, experiences, or protocols, output EXACTLY the word 'KETAMINE'. "
        "If it is about general mental health (depression, anxiety, etc.), output EXACTLY the word 'GENERAL'."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat_completion(messages=messages, max_tokens=10, temperature=0.1)
    decision = response.choices[0].message.content.strip().upper()
    
    return "KETAMINE" if "KETAMINE" in decision else "GENERAL"

def ketamine_therapy_agent(message: str, persona: str) -> str:
    """
    Ketamine Therapy Model: Handles ketamine-specific queries using RAG (Placeholder).
    """
    # TODO: Implement RAG pipeline here (Neon DB pgVector similarity search)
    # For now, we mock the context retrieval.
    retrieved_context = "Ketamine therapy can cause temporary dissociation, which is a known and expected effect."
    
    system_prompt = (
        f"You are a specialized AI focused ONLY on ketamine-related therapy. "
        f"You must adopt the following persona: {persona}. "
        f"Answer the user's query using ONLY the provided context. If the context "
        f"does not contain the answer, state that you do not know."
        f"\n\nContext: {retrieved_context}"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat_completion(messages=messages, max_tokens=500, temperature=0.5)
    return response.choices[0].message.content.strip()

def general_therapy_agent(message: str, persona: str) -> str:
    """
    General Therapy Model: Handles broad mental health topics.
    """
    system_prompt = (
        f"You are a general AI therapist. You handle general mental health topics "
        f"such as depression, anxiety, and stress. "
        f"You must adopt the following persona: {persona}. "
        f"Do NOT provide advice specifically about ketamine."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat_completion(messages=messages, max_tokens=500, temperature=0.7)
    return response.choices[0].message.content.strip()

# --- API Endpoints ---

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main Conversation Endpoint.
    """
    try:
        # 1. Orchestrator detects intent
        route = detect_intent(request.message)
        
        # 2. Route to the appropriate agent and apply the Identity/Persona
        if route == "KETAMINE":
            reply = ketamine_therapy_agent(request.message, request.persona)
            model_used = "Ketamine Therapy Model"
        else:
            reply = general_therapy_agent(request.message, request.persona)
            model_used = "General Therapy Model"
            
        # 3. TODO: Save conversation to Neon DB (including pending training flags)
            
        return ChatResponse(routed_to=model_used, response=reply)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)