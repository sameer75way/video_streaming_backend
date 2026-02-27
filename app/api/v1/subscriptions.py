from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import SubscriptionService
from app.core import get_db, get_current_user
from app.models import User

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/activate")
async def subscribe(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await SubscriptionService.subscribe(current_user, db)