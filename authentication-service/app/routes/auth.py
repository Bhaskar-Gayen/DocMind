from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.services.auth_service import AuthService
from app.models.schemas import UserCreate, Token, User, NewPassword
from app.dependencies import get_db, get_current_user, oauth2_scheme

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    db: AsyncSession  = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password
    )
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(
        form_data.username,
        form_data.password
    )
    return await auth_service.login(user)

@router.post("/logout")
async def logout(
    current_user_id: str = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    await auth_service.logout(current_user_id, token)
    return {"message": "Successfully logged out"}

@router.put("/update-password")
async def update_user_password(newpassword:NewPassword, username: str = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user=await auth_service.authenticate_user(username, newpassword.current_password)
    try:
        await auth_service.change_user_password(user, newpassword.new_password)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the password.",
        )
    return JSONResponse(content={"detail": "Password updated successfully"}, status_code=status.HTTP_200_OK)

