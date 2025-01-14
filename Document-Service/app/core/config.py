from functools import lru_cache

from cryptography.hazmat.primitives.hashes import SHA512
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    PROJECT_NAME: str = "DocMind Document Service"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: Optional[List[str]] = None
    DEBUG: bool= True
    VERSION:str="v1"

    # Database
    DATABASE_URL: Optional[str] = "postgresql+asyncpg://postgres:123@localhost:5432/docmind"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    # ALGORITHM:str=SHA512

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = "fake_access_key"
    AWS_SECRET_ACCESS_KEY: Optional[str] = "fake_secret_key"
    AWS_BUCKET_NAME: Optional[str] = "fake_bucket"
    AWS_REGION: Optional[str] = "us-west-2"

    # Elasticsearch
    ELASTICSEARCH_HOST: Optional[str] = "localhost"
    ELASTICSEARCH_PORT: Optional[int] = 9200

    # Redis
    REDIS_HOST: Optional[str] = "localhost"
    REDIS_PORT: Optional[int] = 6379

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
