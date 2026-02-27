import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Therapy Orchestrator"
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    NEON_DB_URL: str = os.getenv("NEON_DB_URL", "")

    class Config:
        env_file = ".env"


settings = Settings()
