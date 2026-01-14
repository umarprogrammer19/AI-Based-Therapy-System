from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .settings import settings
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

# For asyncpg, SSL parameters need to be handled differently
# We'll remove SSL parameters from the URL and add them as connect_args
import urllib.parse

def create_engine_with_ssl():
    parsed_url = urllib.parse.urlparse(str(settings.database_url))
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Remove SSL-related parameters from URL since asyncpg handles them differently
    ssl_params = {'sslmode', 'sslcert', 'sslkey', 'sslrootcert', 'channel_binding'}
    filtered_params = {k: v for k, v in query_params.items() if k.lower() not in ssl_params}

    # Reconstruct URL without SSL parameters
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    if filtered_params:
        new_query = urllib.parse.urlencode(filtered_params, doseq=True)
        clean_url = f"{base_url}?{new_query}" if new_query else base_url
    else:
        clean_url = base_url

    # Handle SSL configuration for asyncpg
    connect_args = {}
    if 'sslmode' in query_params:
        sslmode = query_params['sslmode'][0]
        # For asyncpg, we might need to handle SSL differently
        # This depends on the specific requirements

    return create_async_engine(
        clean_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        connect_args=connect_args,
    )

# Create the async engine
engine = create_engine_with_ssl()

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
        # Install pgvector extension if it doesn't exist
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
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