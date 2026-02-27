from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    role_id: int = Field(foreign_key="roles.id")
    role: Optional[Role] = Relationship()