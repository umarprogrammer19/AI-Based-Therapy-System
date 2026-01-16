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
    # The issue is with SSL parameters in the URL causing problems with asyncpg
    # asyncpg handles SSL automatically when using the postgresql+asyncpg scheme
    # Let's strip out problematic SSL parameters from the URL

    parsed_url = urllib.parse.urlparse(str(settings.database_url))
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Remove SSL-related parameters that cause issues with asyncpg
    # These parameters are often not compatible with asyncpg via SQLAlchemy
    ssl_params_to_remove = {'sslmode', 'channel_binding', 'sslcert', 'sslkey', 'sslrootcert'}
    safe_params = {k: v for k, v in query_params.items() if k.lower() not in ssl_params_to_remove}

    # Reconstruct URL without SSL parameters that cause issues
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    if safe_params:
        new_query = urllib.parse.urlencode(safe_params, doseq=True)
        clean_url = f"{base_url}?{new_query}" if new_query else base_url
    else:
        clean_url = base_url

    # Connect args for asyncpg - minimal settings to avoid conflicts
    connect_args = {}

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
    Create all tables defined in SQLModel models and initialize default admin user.
    """
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        # Install pgvector extension if it doesn't exist
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully.")

    # Create default admin user after tables are created in a separate session
    await create_default_admin_user()


async def create_default_admin_user():
    """
    Create a default admin user if one doesn't exist.
    """
    import asyncio
    from sqlmodel.ext.asyncio.session import AsyncSession
    from ..services.user import user_service
    from ..models.user import UserCreate, UserRole
    from ..services.auth import auth_service
    from sqlalchemy.exc import ProgrammingError, OperationalError

    # Wait a bit to ensure tables are fully available in PostgreSQL
    await asyncio.sleep(1)

    try:
        async with AsyncSession(engine) as session:
            # Check if admin user already exists
            admin_user = await user_service.get_user_by_username(session, "admin")
            if not admin_user:
                logger.info("Creating default admin user...")

                # Create admin user
                admin_create = UserCreate(
                    email="admin@ketamine-therapy.ai",
                    username="admin",
                    full_name="Administrator",
                    role=UserRole.ADMIN,
                    password="admin123"  # Default password - should be changed in production
                )

                await user_service.create_user(session, admin_create)
                logger.info("Default admin user created successfully.")
    except (ProgrammingError, OperationalError) as e:
        # If there's a column/table mismatch, log it but continue
        logger.warning(f"Could not create default admin user due to schema mismatch: {str(e)}")
        logger.info("Continuing startup process...")
    except Exception as e:
        # Log other errors but continue
        logger.warning(f"Could not create default admin user: {str(e)}")
        logger.info("Continuing startup process...")


async def drop_tables():
    """
    Drop all tables (useful for testing).
    """
    logger.warning("Dropping database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    logger.info("Database tables dropped successfully.")