from fastapi import APIRouter
from . import knowledge_docs, vector_chunks, audit_logs, chat


# Create the main API router
router = APIRouter()

# Include individual API routers
router.include_router(knowledge_docs.router, prefix="/knowledge-docs", tags=["knowledge-docs"])
router.include_router(vector_chunks.router, prefix="/vector-chunks", tags=["vector-chunks"])
router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])