from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from environment variables (and `.env` in development)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "postgresql+psycopg://autoexam:autoexam@localhost:5432/autoexam"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]

    # LLM provider layer: provider and model names come from config, never from code.
    llm_provider: str = "gemini"
    llm_model: str = ""
    embedding_model: str = ""
    embedding_dimensions: int = 768
    gemini_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
