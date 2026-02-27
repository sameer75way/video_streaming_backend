from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User
from app.models.video import Video


class Purchase(SQLModel, table=True):
    __tablename__ = "purchases"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    video_id: int = Field(foreign_key="videos.id")
    purchased_at: datetime = Field(default_factory=datetime.utcnow)
    amount: float
    user: Optional[User] = Relationship()
    video: Optional[Video] = Relationship()