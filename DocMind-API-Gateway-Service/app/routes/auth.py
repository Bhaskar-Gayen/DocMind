from fastapi import APIRouter
from app.config import settings
from app.utils.http import forward_request

router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])


@router.post("/login")
async def login(credentials: dict):
    return await forward_request(
        f"{settings.AUTH_SERVICE_URL}/login",
        method="POST",
        json=credentials
    )


@router.post("/register")
async def register(user_data: dict):
    return await forward_request(
        f"{settings.AUTH_SERVICE_URL}/register",
        method="POST",
        json=user_data
    )
