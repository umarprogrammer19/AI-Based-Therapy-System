from pydantic_settings import BaseSettings as Settings
import os
from typing import Optional


class Settings(Settings):
    """
    Application settings loaded from environment variables.
    """

    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://neondb_owner:npg_fIvBAb13GOzn@ep-shiny-mud-adwijmjc-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    )

    # API settings
    api_v1_prefix: str = "/api/v1"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    project_name: str = "Backend Foundation API"
    version: str = "0.1.0"
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "*")

    # Hugging Face settings
    hugging_face_api_key: Optional[str] = os.getenv("HUGGING_FACE_API_KEY")

    # API Configuration
    hugging_face_api_url: str = os.getenv(
        "HUGGING_FACE_API_URL", "https://api-inference.huggingface.co"
    )

    # Security settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24


# Create a single instance of settings
settings = Settings()
