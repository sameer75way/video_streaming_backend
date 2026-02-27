

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    VideoCreate,
    VideoUpdate,
    VideoStatusUpdate,
)
from app.services import VideoService
from app.core import get_db, get_current_user, require_role
from app.models import User

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/")
async def create_video(
    data: VideoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await VideoService.create_video(data, current_user, db)


@router.get("/")
async def list_videos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await VideoService.list_videos(current_user, db)


@router.put("/{video_id}")
async def update_video(
    video_id: int,
    data: VideoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await VideoService.update_video(video_id, data, current_user, db)

@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await VideoService.delete_video(video_id, current_user, db)

@router.patch("/{video_id}/status")
async def change_status(
    video_id: int,
    data: VideoStatusUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return await VideoService.change_status(
        video_id,
        data.status,
        user,
        db,
    )

@router.patch("/{video_id}/restore")
async def restore_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await VideoService.restore_video(video_id, current_user, db)