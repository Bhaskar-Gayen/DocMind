from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.logger_config import setup_logger
from app.routes import document
from app.services.search_service import ElasticsearchService
from app.services.storage_service import S3StorageService
from app.utils.document_service_exception import DocumentServiceException

# Setup logging
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI ):
    # Startup logic
    logger.info("Starting Document Service...")

    try:
        # Create database tables asynchronously
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

        # Initialize S3 connection
        # s3_service = S3StorageService()
        # await s3_service.initialize()
        # logger.info("S3 connection initialized successfully")

        # Initialize Elasticsearch
        # es_service = ElasticsearchService()
        # await es_service.initialize()
        # logger.info("Elasticsearch connection initialized successfully")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise

    yield  # Server is running and ready to accept requests

    # Shutdown logic
    logger.info("Shutting down Document Service...")
    try:
        # Close database connections
        await engine.dispose()
        logger.info("Database connections closed")

        # Cleanup any other resources
        # Add cleanup code for other services if needed

    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}", exc_info=True)
        raise


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Document Service API for managing documents with RAG capabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()

    # Calculate request duration
    duration = (end_time - start_time).total_seconds()

    # Log request details
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {duration:.3f}s "
        f"Client: {request.client.host if request.client else 'Unknown'}"
    )

    return response



@app.exception_handler(DocumentServiceException)
async def document_service_exception_handler(request: Request, exc: DocumentServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "details": str(exc) if settings.DEBUG else None
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": settings.VERSION
    }


# Include routers
app.include_router(
    document.router,
    prefix=f"{settings.API_V1_STR}/documents",
    tags=["documents"]
)

@app.get("/")
def root():
    logger.info("This a log message for root API call...")
    return JSONResponse("Everything is working..", status_code=200)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )

