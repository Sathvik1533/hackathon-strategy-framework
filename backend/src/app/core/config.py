import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hackathon Strategy Framework API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # JWT Security
    SECRET_KEY: str = "super-secret-hackathon-jwt-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres_secret@localhost:5432/hackathon_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MCP
    MCP_SERVER_URL: str = "http://localhost:8001/sse"

    # AI Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
