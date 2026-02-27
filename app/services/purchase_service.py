from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import Purchase, Video, User


class PurchaseService:

    @staticmethod
    async def purchase_video(
        video_id: int,
        current_user: User,
        db: AsyncSession,
    ):

        video_result = await db.execute(
            select(Video).where(Video.id == video_id)
        )
        video = video_result.scalar_one_or_none()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        if not video.is_paid:
            raise HTTPException(status_code=400, detail="Video is free")

        if video.creator_id == current_user.id:
            raise HTTPException(status_code=400, detail="Creator cannot purchase own video")

        existing = await db.execute(
            select(Purchase).where(
                (Purchase.user_id == current_user.id) &
                (Purchase.video_id == video_id)
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Already purchased")

        purchase = Purchase(
            user_id=current_user.id,
            video_id=video_id,
            amount=video.price,
        )

        db.add(purchase)
        await db.commit()

        return {"message": "Video purchased successfully"}