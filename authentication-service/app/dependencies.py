from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.exc import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



async def get_db() -> AsyncSession:
    """
    Database dependency that creates a new SessionLocal instance for each request
    and closes it when the request is done.
    """
    async with SessionLocal() as session:
        yield session


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> str:
    """
    Dependency that validates the JWT token and returns the current user ID.
    Raises HTTPException if token is invalid or user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Here you might want to verify the user exists in the database
        return user_id
    except InvalidTokenError:
        raise credentials_exception