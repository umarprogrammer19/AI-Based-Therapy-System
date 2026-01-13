from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..config.database import get_session


async def get_db_session() -> AsyncSession:
    """
    Get database session dependency for API endpoints.
    """
    async for session in get_session():
        yield session