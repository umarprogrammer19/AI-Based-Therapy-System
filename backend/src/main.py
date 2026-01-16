from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import create_tables
from .api.v1.router import router as v1_router
from .config.settings import settings
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI.
    Runs startup and shutdown events.
    """
    logger.info("Starting up...")
    # Create database tables on startup
    await create_tables()
    logger.info("Database tables initialized.")
    yield
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Ketamine Therapy AI & Learning System",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    @app.get("/health")
    async def health_check():
        """
        Health check endpoint to verify the application is running.
        """
        return {
            "status": "healthy",
            "message": "Ketamine Therapy AI & Learning System is running",
            "version": settings.version,
        }

    return app


# Create the main application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
