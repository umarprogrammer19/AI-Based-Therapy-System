from sqlmodel import create_engine, Session
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - using Neon Serverless PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/ketamine_ai"
)

# Create engine with pgvector support
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def enable_vector_extension():
    """
    Enable the pgvector extension in the database
    This is critical for vector storage and similarity search
    """
    with engine.connect() as conn:
        # Enable the vector extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()