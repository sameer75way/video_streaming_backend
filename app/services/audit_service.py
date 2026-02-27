from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AuditLog


class AuditService:

    @staticmethod
    async def log_action(
        db: AsyncSession,
        user_id: int,
        action: str,
        method: str,
        endpoint: str,
        ip: str,
        resource: str = None,
    ):
        log = AuditLog(
            user_id=user_id,
            action=action,
            method=method,
            endpoint=endpoint,
            ip_address=ip,
            resource=resource,
        )

        db.add(log)
        await db.commit()