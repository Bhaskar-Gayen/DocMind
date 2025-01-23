from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    API_V1_STR: str
    DEBUG:bool

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Database settings
    DATABASE_URL: str

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    # Password hashing
    HASH_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
