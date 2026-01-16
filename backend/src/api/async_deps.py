from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from ..config.database import get_session


async def get_async_db_session() -> AsyncSession:
    """
    Dependency to get an async database session.
    """
    async for session in get_session():
        yield session