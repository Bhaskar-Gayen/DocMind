from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
import jwt
from datetime import datetime
import httpx
from ..config import settings


class JWTAuthMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.public_paths = {
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh-token",
            "/health",
            "/docs",
            "/openapi.json"
        }

    async def __call__(self, request: Request) -> Optional[Dict]:
        if request.url.path in self.public_paths:
            return None

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization credentials"
            )

        try:
            # Verify token with auth service
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.AUTH_SERVICE_URL}/verify-token",
                    headers={"Authorization": f"Bearer {
                        credentials.credentials}"}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token"
                    )

                user_data = response.json()
                # Add user data to request state
                request.state.user = user_data
                return user_data

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )


class RateLimitMiddleware:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = {}

    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Check if client has exceeded rate limit
        current_time = datetime.utcnow().timestamp()
        client_requests = self._requests.get(client_ip, [])

        # Remove old requests
        client_requests = [req_time for req_time in client_requests
                           if current_time - req_time < self.window_seconds]

        if len(client_requests) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        # Add current request
        client_requests.append(current_time)
        self._requests[client_ip] = client_requests

        return await call_next(request)
