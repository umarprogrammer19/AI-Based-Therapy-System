from fastapi import APIRouter
from . import knowledge_docs, vector_chunks, audit_logs, chat, admin, auth, user_docs


# Create the main API router
router = APIRouter()

# Include individual API routers
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
router.include_router(knowledge_docs.router, prefix="/knowledge-docs", tags=["knowledge-docs"])
router.include_router(vector_chunks.router, prefix="/vector-chunks", tags=["vector-chunks"])
router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(user_docs.router, prefix="/user-docs", tags=["user-docs"])