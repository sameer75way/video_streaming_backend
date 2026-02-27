import asyncio
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Video


class EncodingService:

    @staticmethod
    async def simulate_encoding(video_id: int, db: AsyncSession):

        result = await db.execute(
            select(Video).where(Video.id == video_id)
        )
        video = result.scalar_one_or_none()

        if not video:
            return

        video.status = "PROCESSING"
        await db.commit()

        await asyncio.sleep(5)

        video.status = "READY"
        await db.commit()