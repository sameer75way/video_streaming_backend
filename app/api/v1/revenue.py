from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import RevenueService
from app.core import get_db, get_current_user, require_role
from app.models import User

router = APIRouter(prefix="/revenue", tags=["Revenue"])


@router.get("/admin")
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return await RevenueService.admin_revenue_dashboard(db)


@router.get("/creator")
async def creator_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await RevenueService.creator_dashboard(current_user, db)