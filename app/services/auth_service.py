from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models import User, Role
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.core import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


class AuthService:

    @staticmethod
    async def register(data: RegisterRequest, db: AsyncSession):

        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        role_result = await db.execute(
            select(Role).where(Role.name == "VIEWER")
        )
        viewer_role = role_result.scalar_one()

        new_user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            role_id=viewer_role.id
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def login(data: LoginRequest, db: AsyncSession):

        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )

        payload = {"sub": str(user.id)}

        return TokenResponse(
            access_token=create_access_token(payload), 
            refresh_token=create_refresh_token(payload),
        )