from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import AuditLog
from app.core import get_db, require_role

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/")
async def get_logs(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("ADMIN")),
):
    result = await db.execute(select(AuditLog))
    logs = result.scalars().all()
    return logs