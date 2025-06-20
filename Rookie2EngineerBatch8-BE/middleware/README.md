# Middleware

This directory contains FastAPI middleware components that process requests and responses globally.

## Structure

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        # Process request
        response = await call_next(request)
        # Process response
        return response
```

## Common Middleware Types

### Authentication Middleware

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from typing import Optional

security = HTTPBearer()

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        try:
            # Skip auth for public endpoints
            if request.url.path in ["/docs", "/redoc", "/api/v1/auth/login"]:
                return await call_next(request)

            # Get token
            auth = await security(request)
            token = auth.credentials

            # Validate token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            # Add user info to request state
            request.state.user_id = payload.get("sub")
            request.state.is_superuser = payload.get("is_superuser", False)

            return await call_next(request)

        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
```

### CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Request ID Middleware

```python
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response
```

### Logging Middleware

```python
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} "
            f"Processed in {process_time:.3f}s"
        )
        
        return response
```

### Error Handling Middleware

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        try:
            return await call_next(request)
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
```

### Rate Limiting Middleware

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        requests_per_minute: int = 60
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        # Get client IP
        client_ip = request.client.host
        
        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        return await call_next(request)
```

## Using Middleware

Add middleware to your FastAPI application in `main.py`:

```python
from fastapi import FastAPI
from middleware.auth import JWTAuthMiddleware
from middleware.logging import LoggingMiddleware
from middleware.error_handling import ErrorHandlingMiddleware
from middleware.rate_limit import RateLimitMiddleware

app = FastAPI()

# Add middleware in reverse order (last added = first executed)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(JWTAuthMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Best Practices

1. Order matters:
   - Add middleware in reverse order of execution
   - Consider dependencies between middleware

2. Performance:
   - Keep middleware lightweight
   - Only process what's necessary
   - Use caching when appropriate

3. Error handling:
   - Handle errors appropriately in each middleware
   - Don't let errors propagate unnecessarily
   - Log errors for debugging

4. Security:
   - Validate input in security middleware
   - Don't expose sensitive information
   - Use appropriate HTTP headers

5. Configuration:
   - Make middleware configurable
   - Use environment variables for settings
   - Document configuration options

