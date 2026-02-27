from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Engagement(SQLModel, table=True):
    __tablename__ = "engagements"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    video_id: int = Field(foreign_key="videos.id")
    type: str  
    created_at: datetime = Field(default_factory=datetime.utcnow)