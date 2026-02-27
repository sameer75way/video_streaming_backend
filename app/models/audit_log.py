from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    action: str
    resource: Optional[str] = None
    method: str
    endpoint: str
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)