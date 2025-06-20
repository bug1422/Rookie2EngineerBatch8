import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logging_config import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        status_code = response.status_code
        
        if status_code >= 500:
            log_level = logger.error
        elif status_code >= 400:
            log_level = logger.warning
        else:
            log_level = logger.info
            
        log_level(
            f"Response: {request.method} {request.url} "
            f"Status: {status_code} "
            f"Duration: {process_time:.3f}s"
        )

        return response
