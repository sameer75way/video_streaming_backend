from sqlmodel import select
from fastapi import HTTPException
from app.models import User, Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class UserService:

    @staticmethod
    async def change_role(
        user_id: int,
        role_name: str,
        current_user: User,
        db: AsyncSession,
    ):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not allowed")

        role_result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = role_result.scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.role_id = role.id
        await db.commit()
        await db.refresh(user)

        return {"message": f"User role updated to {role_name}"}

    @staticmethod
    async def list_users(
        current_user: User,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
    ):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not allowed")

        result = await db.execute(
            select(User)
            .options(selectinload(User.role))
            .offset(skip)
            .limit(limit)
        )

        users = result.scalars().all()

        return [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role.name,
                "created_at": user.created_at,
            }
            for user in users
        ]