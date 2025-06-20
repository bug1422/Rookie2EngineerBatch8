from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings
from jose import jwt
from starlette.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = [
        "",
        "/",
        "/docs",
        "/redoc",
        "/health",
        "/openapi.json",
        "/v1/auth/login",
        "/favicon.ico",
    ]

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token") or request.cookies.get("refresh_token") or request.headers.get("Authorization")
        if not token:
            return JSONResponse(status_code=401, content={"message": "Missing authentication token", "error": "no_tokens"})

        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"message": "Token expired", "error": "expired"})
        except jwt.JWTError:
            return JSONResponse(status_code=401, content={"message": "Invalid token", "error": "invalid"})

        response = await call_next(request)
        return response
