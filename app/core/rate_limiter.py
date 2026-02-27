import time
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.config import settings
RATE_LIMITS = {
    "auth": (settings.RATE_LIMIT_AUTH, 60),
    "stream": (settings.RATE_LIMIT_STREAM, 60),
    "default": (settings.RATE_LIMIT_DEFAULT, 60),
}

request_logs = defaultdict(list)


def get_route_type(path: str):
    if "/auth/login" in path:
        return "auth"
    if "/stream" in path:
        return "stream"
    return "default"


async def rate_limit_middleware(request: Request):

    path = request.url.path
    client_ip = request.client.host

    route_type = get_route_type(path)
    max_requests, window = RATE_LIMITS[route_type]

    now = time.time()
    window_start = now - window

    logs = request_logs[client_ip]

    # Remove expired timestamps
    request_logs[client_ip] = [
        timestamp for timestamp in logs if timestamp > window_start
    ]

    if len(request_logs[client_ip]) >= max_requests:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please slow down."}
        )

    request_logs[client_ip].append(now)