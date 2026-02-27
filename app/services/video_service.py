from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models import Video, User, Purchase
from app.schemas import VideoCreate, VideoUpdate
from app.services.subscription_service import SubscriptionService
from app.services.encoding_service import EncodingService


VALID_TRANSITIONS = {
    "UPLOADED": ["PROCESSING"],
    "PROCESSING": ["READY"],
    "READY": []
}


class VideoService:

    @staticmethod
    async def _get_video(video_id: int, db: AsyncSession):
        result = await db.execute(
            select(Video).where(
                Video.id == video_id,
                Video.is_deleted == False
            )
        )
        video = result.scalar_one_or_none()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

    @staticmethod
    async def create_video(
        data: VideoCreate,
        current_user: User,
        db: AsyncSession,
    ):
        if current_user.role.name not in ["CREATOR", "ADMIN"]:
            raise HTTPException(status_code=403, detail="Not allowed")

        if data.is_paid and (data.price is None or data.price <= 0):
            raise HTTPException(status_code=400, detail="Invalid price")

        video = Video(
            title=data.title,
            description=data.description,
            is_paid=data.is_paid,
            price=data.price,
            creator_id=current_user.id,
        )

        db.add(video)
        await db.commit()
        await db.refresh(video)

        await EncodingService.simulate_encoding(video.id, db)

        return video

    @staticmethod
    async def list_videos(
        current_user: User,
        db: AsyncSession,
    ):
        if current_user.role.name == "ADMIN":
            result = await db.execute(
                select(Video)
                .where(Video.is_deleted == False)
                .options(selectinload(Video.creator))
            )
            return result.scalars().all()

        if current_user.role.name == "CREATOR":
            result = await db.execute(
                select(Video)
                .where(
                    Video.is_deleted == False,
                    (
                        (Video.status == "READY") |
                        (Video.creator_id == current_user.id)
                    )
                )
            )
            return result.scalars().all()

        result = await db.execute(
            select(Video)
            .where(
                Video.is_deleted == False,
                Video.status == "READY"
            )
        )
        return result.scalars().all()

    @staticmethod
    async def update_video(
        video_id: int,
        data: VideoUpdate,
        current_user: User,
        db: AsyncSession,
    ):
        video = await VideoService._get_video(video_id, db)

        if current_user.role.name != "ADMIN" and video.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        if data.title is not None:
            video.title = data.title

        if data.description is not None:
            video.description = data.description

        if data.is_paid is not None:
            video.is_paid = data.is_paid

        if data.price is not None:
            video.price = data.price

        await db.commit()
        await db.refresh(video)

        return video

    @staticmethod
    async def delete_video(
        video_id: int,
        current_user: User,
        db: AsyncSession,
    ):
        video = await VideoService._get_video(video_id, db)

        if current_user.role.name != "ADMIN" and video.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        video.is_deleted = True
        video.deleted_at = datetime.utcnow()

        await db.commit()

        return {"message": "Video soft deleted"}

    @staticmethod
    async def restore_video(
        video_id: int,
        current_user: User,
        db: AsyncSession,
    ):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not allowed")

        result = await db.execute(
            select(Video).where(Video.id == video_id)
        )
        video = result.scalar_one_or_none()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        video.is_deleted = False
        video.deleted_at = None

        await db.commit()

        return {"message": "Video restored"}

    @staticmethod
    async def hard_delete(
        video_id: int,
        current_user: User,
        db: AsyncSession,
    ): 
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not allowed")

        result = await db.execute(
            select(Video).where(Video.id == video_id)
        )
        video = result.scalar_one_or_none()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        await db.delete(video)
        await db.commit()

        return {"message": "Video permanently deleted"}

    @staticmethod
    async def change_status(
        video_id: int,
        status: str,
        current_user: User,
        db: AsyncSession,
    ):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Only admin can change status")

        video = await VideoService._get_video(video_id, db)

        if status not in VALID_TRANSITIONS.get(video.status, []):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from {video.status} to {status}"
            )

        video.status = status
        await db.commit()
        await db.refresh(video)

        return video

    @staticmethod
    async def can_user_access_video(
        video_id: int,
        current_user: User,
        db: AsyncSession,
    ):
        video = await VideoService._get_video(video_id, db)

        if video.status != "READY":
            raise HTTPException(status_code=400, detail="Video not ready")

        if not video.is_paid:
            return video

        if current_user.role.name == "ADMIN":
            return video

        if video.creator_id == current_user.id:
            return video

        if await SubscriptionService.has_active_subscription(current_user, db):
            return video

        purchase = await db.execute(
            select(Purchase).where(
                Purchase.user_id == current_user.id,
                Purchase.video_id == video_id
            )
        )

        if not purchase.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Purchase required")

        return video