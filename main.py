from fastapi import FastAPI
from src.api import chat
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Include Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
def read_root():
    return {"status": "AI Therapy Backend is running"}
