from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/verify-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )
