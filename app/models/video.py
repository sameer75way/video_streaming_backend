from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User


class Video(SQLModel, table=True):
    __tablename__ = "videos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_paid: bool = False
    price: Optional[float] = None
    status: str = Field(default="UPLOADED")  # UPLOADED, PROCESSING, READY
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None   
    creator_id: int = Field(foreign_key="users.id")
    creator: Optional[User] = Relationship()