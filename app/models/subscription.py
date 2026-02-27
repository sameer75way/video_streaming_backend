from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime
    active: bool = True