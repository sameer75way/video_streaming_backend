from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.services import AuthService
from app.core.dependencies import get_db, get_current_user
from app.models import User
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService.register(data, db)
    return {"message": "User registered", "user_id": user.id}


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    data = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )
    return await AuthService.login(data, db)


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role.name,
    }