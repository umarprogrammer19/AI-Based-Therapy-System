from fastapi import APIRouter, HTTPException
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.orchestrator import detect_intent
from src.services.agents import generate_ketamine_response, generate_general_response

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handles live chat requests and routes them."""
    try:
        route = detect_intent(request.message)

        if route == "KETAMINE":
            # In the future, call app.services.rag to get context from Neon DB
            mock_context = "Ketamine therapy can cause dissociation."
            reply = generate_ketamine_response(
                request.message, request.persona, mock_context
            )
            model_used = "Ketamine Therapy Model"
        else:
            reply = generate_general_response(request.message, request.persona)
            model_used = "General Therapy Model"

        # The logic to flag relevant conversation segments as potential training data and store them in the pending dataset [cite: 31] will be added here.

        return ChatResponse(
            routed_to=model_used,
            response=reply,
            flagged_for_training=True,  # Mocking the flagging logic
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
