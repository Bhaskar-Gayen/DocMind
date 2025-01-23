from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Base class for ORM models
Base = declarative_base()

# Create an async engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Create an async session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,   # Use AsyncSession for async operations
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

