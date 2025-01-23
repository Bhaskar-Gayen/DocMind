from datetime import timedelta

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.services.cache_service import RedisCache


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cache = RedisCache()

    async def authenticate_user(self, username: str, password: str)->User:
        result = await  self.db.execute(select(User).where(or_(User.email == username, User.username == username)))
        user=result.scalar()
        print(user)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        return user

    async def create_user(self, email: EmailStr, username: str, password: str):
        result = await self.db.execute(select(User).where(or_(User.email == email, User.username == username)))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or Userid already registered",
            )

        # Create new user
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password)
        )
        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user.",
            )
        return user

    async def login(self, user: User):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            subject=str(user.email),
            expires_delta=access_token_expires
        )

        # # Store token in Redis
        # await self.cache.set_token(
        #     user.id,
        #     access_token,
        #     settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        # )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def logout(self, user_id: str, token: str):
        # Delete token from Redis
        # await self.cache.delete_token(user_id)
        # Blacklist the token
        # await self.cache.blacklist_token(token)
        pass

    async def change_user_password(self, user:User, new_password: str):
        user.hashed_password=get_password_hash(new_password)
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise

