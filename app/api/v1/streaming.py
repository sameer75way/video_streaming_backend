from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import AnalyticsService
from app.services import VideoService
from app.core import get_db, get_current_user
from app.models import User
from app.core.security import create_stream_token
from jose import jwt, JWTError
from app.core.config import settings

router = APIRouter(prefix="/stream", tags=["Streaming"])


@router.get("/{video_id}")
async def generate_stream_link(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = await VideoService.can_user_access_video(video_id, current_user, db)

    token = create_stream_token(video.id, current_user.id)

    return {
        "stream_url": f"/api/v1/stream/play/{token}",
        "expires_in_seconds": 60
    }


@router.get("/play/{token}")
async def play_stream(token: str):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired stream token")

    if payload.get("type") != "stream":
        raise HTTPException(status_code=401, detail="Invalid token type")

    video_id = payload.get("video_id")

    return {
        "message": f"Streaming secured video {video_id}"
    } 