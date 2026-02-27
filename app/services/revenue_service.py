from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from fastapi import HTTPException

from app.models import Purchase, Video, User

PLATFORM_SHARE = 0.20
CREATOR_SHARE = 0.80


class RevenueService:

    @staticmethod
    async def admin_revenue_dashboard(db: AsyncSession):

        total_revenue = await db.execute(
            select(func.sum(Purchase.amount))
        )

        total_revenue = total_revenue.scalar() or 0

        platform_earnings = total_revenue * PLATFORM_SHARE
        creator_earnings = total_revenue * CREATOR_SHARE

        return {
            "total_revenue": total_revenue,
            "platform_earnings": platform_earnings,
            "creator_earnings": creator_earnings,
        }

    @staticmethod
    async def creator_dashboard(user: User, db: AsyncSession):

        if user.role.name != "CREATOR":
            raise HTTPException(status_code=403, detail="Not allowed")

        result = await db.execute(
            select(func.sum(Purchase.amount))
            .join(Video, Video.id == Purchase.video_id)
            .where(Video.creator_id == user.id)
        )

        total = result.scalar() or 0

        return {
            "total_sales": total,
            "your_earnings": total * CREATOR_SHARE,
            "platform_cut": total * PLATFORM_SHARE,
        }