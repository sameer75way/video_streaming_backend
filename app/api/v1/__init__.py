from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .videos import router as videos_router
from .payments import router as payments_router
from .streaming import router as streaming_router
from .analytics import router as analytics_router
from .subscriptions import router as subscription_router
from .revenue import router as revenue_router
from .audit import router as audit_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(videos_router)
api_router.include_router(payments_router)
api_router.include_router(streaming_router)
api_router.include_router(analytics_router)
api_router.include_router(subscription_router)
api_router.include_router(revenue_router)
api_router.include_router(audit_router)

__all__ = ["api_router"]