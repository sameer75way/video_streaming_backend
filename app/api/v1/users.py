from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db, get_current_user
from app.schemas import RoleUpdate
from app.services import UserService
from app.models import User
from app.core.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/admin-only")
async def admin_only(
    user: User = Depends(require_role("ADMIN"))
):
    return {"message": "Welcome Admin"}

@router.patch("/{user_id}/role")
async def change_user_role(
    user_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await UserService.change_role(
        user_id,
        data.role_name,
        current_user,
        db,
    )

@router.get("/")
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await UserService.list_users(
        current_user=current_user,
        db=db,
        skip=skip,
        limit=limit,
    )