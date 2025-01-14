from pydantic import BaseModel
from typing import List
import os


class Settings(BaseModel):
    AUTH_SERVICE_URL: str = os.getenv(
        "AUTH_SERVICE_URL", "http://auth-service:8001")
    DOCUMENT_SERVICE_URL: str = os.getenv(
        "DOCUMENT_SERVICE_URL", "http://document-service:8002")
    RAG_SERVICE_URL: str = os.getenv(
        "RAG_SERVICE_URL", "http://rag-service:8003")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    API_V1_PREFIX: str = "/api/v1"


settings = Settings()
