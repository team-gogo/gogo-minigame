import uuid
import time
import logging

from fastapi import Request, Response
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger('GOGO-MiniGame Logger')


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log_id = str(uuid.uuid4())
        start_time = time.time()

        request_body = await request.body()

        logger.info(
            f"Log-ID: {log_id}, "
            f"IP: {request.client.host}, "
            f"URI: {request.url.path}, "
            f"Http-Method: {request.method}, "
            f"Params: {dict(request.query_params)}, "
            f"Content-Type: {request.headers.get('content-type')}, "
            f"User-Agent: {request.headers.get('user-agent')}, "
            f"Request-Body: {request_body.decode('utf-8')}"
        )

        response = await call_next(request)

        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))

        process_time = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"Log-ID: {log_id}, "
            f"Status-Code: {response.status_code}, "
            f"Content-Type: {response.headers.get('content-type')}, "
            f"Response Time: {process_time}ms, "
            f"Response-Body: {response_body[0].decode('utf-8')}"
        )

        return response