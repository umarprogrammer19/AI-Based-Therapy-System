from sqlmodel.ext.asyncio.session import AsyncSession
from ..config.database import AsyncSessionLocal
from fastapi import Depends
from typing import AsyncGenerator


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    """
    async with AsyncSessionLocal() as session:
        yield session