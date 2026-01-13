from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .settings import settings
import logging

logger = logging.getLogger(__name__)

# Create the async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True to see SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Number of connection pools
    max_overflow=10,  # Additional connections beyond pool_size
    pool_recycle=300,  # Recycle connections after 5 minutes
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    """
    Create all tables defined in SQLModel models.
    """
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully.")


async def drop_tables():
    """
    Drop all tables (useful for testing).
    """
    logger.warning("Dropping database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    logger.info("Database tables dropped successfully.")