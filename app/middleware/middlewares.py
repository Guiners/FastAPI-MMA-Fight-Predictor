import time

from fastapi import Request

from app.utils.logger import logger


async def log_requests(request: Request, call_next):
    start = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        f"Response status: {response.status_code} for {request.url} completed in {duration:.2f}s"
    )
    return response
