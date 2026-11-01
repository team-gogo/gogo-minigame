import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


no_logging_path = ['/minigame/health', '/minigame/health/readiness', '/favicon.ico', '/actuator/prometheus']
logger = logging.getLogger('GOGO-MiniGame Logger')


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in no_logging_path:
            return await call_next(request)

        log_id = uuid.uuid4()
        start_time = time.perf_counter()
        response = await call_next(request)
        logger.info(
            'Log-ID: %s, Method: %s, Path: %s, Status-Code: %s, Response Time: %.2fms',
            log_id, request.method, request.url.path, response.status_code,
            (time.perf_counter() - start_time) * 1000,
        )
        return response