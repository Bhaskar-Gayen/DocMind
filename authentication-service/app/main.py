from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import engine, Base
from app.logger_config import setup_logger
from app.routes import auth
from app.utils.auth_service_exception import AuthServiceException

# Setup logging
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting Authentication Service...")

    try:
        # Create database tables asynchronously
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

        # Initialize any other required services here
        # Example: CacheService, ExternalAuthProviders, etc.

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise

    yield  # Server is running and ready to accept requests

    # Shutdown logic
    logger.info("Shutting down Authentication Service...")
    try:
        # Close database connections
        await engine.dispose()
        logger.info("Database connections closed")

        # Cleanup any other resources

    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}", exc_info=True)
        raise

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Authentication Service API for user management and authentication",
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

    duration = (end_time - start_time).total_seconds()
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {duration:.3f}s "
        f"Client: {request.client.host if request.client else 'Unknown'}"
    )

    return response

@app.exception_handler(AuthServiceException)
async def auth_service_exception_handler(request: Request, exc: AuthServiceException):
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
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["authentication"]
)

class Test(BaseModel):
    title:str ="Test title"
    content:str="Test content"


@app.get("/")
def root():
    logger.info("This is a log message for the root API call...")
    # return JSONResponse("Everything running and working fine", status_code=200)
    return {"data":settings}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )
