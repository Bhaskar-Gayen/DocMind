from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import httpx

from .config import settings
from .routes import router

app = FastAPI(
    title="DocMind-Document Processing Platform API Gateway",
    description="API Gateway for document processing and RAG-based Q&A system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Health Check


@app.get("/health")
async def health_check():
    services_health = {}
    async with httpx.AsyncClient() as client:
        for service, url in {
            "auth": settings.AUTH_SERVICE_URL,
            "document": settings.DOCUMENT_SERVICE_URL,
            "rag": settings.RAG_SERVICE_URL
        }.items():
            try:
                response = await client.get(f"{url}/health")
                services_health[service] = "healthy" if response.status_code == 200 else "unhealthy"
            except httpx.RequestError:
                services_health[service] = "unavailable"

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": services_health
    }

# Error Handlers


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "status_code": exc.status_code,
        "detail": exc.detail,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
