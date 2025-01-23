import redis
from app.core.config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    async def set_token(self, user_id: int, token: str, expires_in: int):
        """Store token in Redis with expiration"""
        key = f"user_session:{user_id}"
        await self.redis_client.setex(key, expires_in, token)

    async def get_token(self, user_id: int) -> str:
        """Get token from Redis"""
        key = f"user_session:{user_id}"
        return await self.redis_client.get(key)

    async def delete_token(self, user_id: int):
        """Delete token from Redis"""
        key = f"user_session:{user_id}"
        await self.redis_client.delete(key)

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        return await self.redis_client.sismember("blacklisted_tokens", token)

    async def blacklist_token(self, token: str):
        """Add token to blacklist"""
        await self.redis_client.sadd("blacklisted_tokens", token)