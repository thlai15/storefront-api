from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, sourced from environment variables / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./storefront.db"
    cors_allowed_origins: list[str] = ["http://localhost:3000"]
    environment: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
