from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import PurchaseService
from app.core import get_db, get_current_user
from app.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/purchase/{video_id}")
async def purchase_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await PurchaseService.purchase_video(video_id, current_user, db)