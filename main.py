from fastapi import FastAPI, Request
from app.api import api_router
from app.db import AsyncSessionLocal
from app.db.seeders.role_seeder import seed_roles_and_admin
from app.core.rate_limiter import rate_limit_middleware
from app.services import AuditService
from jose import jwt, JWTError
from app.core import settings

app = FastAPI(title="Video Streaming Backend")

@app.middleware("http")
async def apply_rate_limiting(request: Request, call_next):

    rate_limit_response = await rate_limit_middleware(request)

    if rate_limit_response:
        return rate_limit_response

    response = await call_next(request)
    return response


@app.middleware("http")
async def audit_middleware(request: Request, call_next):

    response = await call_next(request)

    # ignore health check logs
    if "/health" in request.url.path:
        return response

    user_id = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = int(payload.get("sub"))
        except JWTError:
            pass

    async with AsyncSessionLocal() as db:
        await AuditService.log_action(
            db=db,
            user_id=user_id,
            action="API_CALL",
            method=request.method,
            endpoint=request.url.path,
            ip=request.client.host if request.client else None,
        )

    return response


app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    async with AsyncSessionLocal() as session:
        await seed_roles_and_admin(session)


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}