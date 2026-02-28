from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str
    message: str
    persona: str = "Calm therapist"


class ChatResponse(BaseModel):
    routed_to: str
    response: str
    flagged_for_training: bool = False  # Storing training candidates
