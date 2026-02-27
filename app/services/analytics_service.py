from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from fastapi import HTTPException

from app.models import VideoView, Engagement, Video, User


class AnalyticsService:

    @staticmethod
    async def record_view(video_id: int, user: User, db: AsyncSession):
        view = VideoView(
            user_id=user.id,
            video_id=video_id,
            watch_time=0
        )
        db.add(view)
        await db.commit()

    @staticmethod
    async def add_engagement(video_id: int, user: User, type: str, db: AsyncSession):

        if type not in ["LIKE", "DISLIKE"]:
            raise HTTPException(status_code=400, detail="Invalid engagement type")

        engagement = Engagement(
            user_id=user.id,
            video_id=video_id,
            type=type
        )

        db.add(engagement)
        await db.commit()

        return {"message": f"{type} recorded"}

    @staticmethod
    async def get_video_analytics(video_id: int, user: User, db: AsyncSession):

        video_result = await db.execute(
            select(Video).where(Video.id == video_id)
        )
        video = video_result.scalar_one_or_none()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        # check perms
        if user.role.name != "ADMIN" and video.creator_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        total_views = await db.execute(
            select(func.count(VideoView.id)).where(VideoView.video_id == video_id)
        )

        unique_views = await db.execute(
            select(func.count(func.distinct(VideoView.user_id)))
            .where(VideoView.video_id == video_id)
        )

        likes = await db.execute(
            select(func.count(Engagement.id))
            .where(
                (Engagement.video_id == video_id) &
                (Engagement.type == "LIKE")
            )
        )

        dislikes = await db.execute(
            select(func.count(Engagement.id))
            .where(
                (Engagement.video_id == video_id) &
                (Engagement.type == "DISLIKE")
            )
        )

        return {
            "total_views": total_views.scalar(),
            "unique_viewers": unique_views.scalar(),
            "likes": likes.scalar(),
            "dislikes": dislikes.scalar(),
        }