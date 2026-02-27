from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class VideoView(SQLModel, table=True):
    __tablename__ = "video_views"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    video_id: int = Field(foreign_key="videos.id")
    watch_time: Optional[int] = 0  
    viewed_at: datetime = Field(default_factory=datetime.utcnow)