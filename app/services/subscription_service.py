from datetime import datetime, timedelta
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import Subscription, User


class SubscriptionService:

    @staticmethod
    async def subscribe(current_user: User, db: AsyncSession):

        existing = await db.execute(
            select(Subscription)
            .where(
                (Subscription.user_id == current_user.id) &
                (Subscription.active == True)
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Already subscribed")

        subscription = Subscription(
            user_id=current_user.id,
            end_date=datetime.utcnow() + timedelta(days=30),
            active=True
        )

        db.add(subscription)
        await db.commit()

        return {"message": "Subscription activated"}

    @staticmethod
    async def has_active_subscription(user: User, db: AsyncSession):

        result = await db.execute(
            select(Subscription)
            .where(
                (Subscription.user_id == user.id) &
                (Subscription.active == True)
            )
        )

        subscription = result.scalar_one_or_none()

        if not subscription:
            return False

        if subscription.end_date < datetime.utcnow():
            subscription.active = False
            await db.commit()
            return False

        return True