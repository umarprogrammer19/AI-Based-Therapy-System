from sqlmodel import SQLModel
from .connection import engine, enable_vector_extension
from ..models.knowledge_doc import KnowledgeDoc
from ..models.vector_chunk import VectorChunk
from ..models.chat_session import ChatSession
from ..models.chat_message import ChatMessage

def init_db():
    """
    Initialize the database with all required tables
    Including enabling the vector extension for pgvector
    """
    print("Enabling vector extension...")
    enable_vector_extension()

    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()