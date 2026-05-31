from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "HealthyCare"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./data/healthy_care.db"
    DATABASE_ECHO: bool = False

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: list[str] = ["*"]

    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""
    LLM_MODEL: str = ""

    EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"
    CHROMA_PERSIST_DIR: str = "data/chroma"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
