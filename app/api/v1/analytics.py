from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import AnalyticsService
from app.core import get_db, get_current_user
from app.models import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/{video_id}")
async def video_analytics(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await AnalyticsService.get_video_analytics(
        video_id,
        current_user,
        db,
    )


@router.post("/{video_id}/engagement/{type}")
async def engagement(
    video_id: int,
    type: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await AnalyticsService.add_engagement(
        video_id,
        current_user,
        type,
        db,
    )