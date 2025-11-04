import time
import typing

from fastapi import Request
from starlette.responses import Response

from app.tools.logger import logger


async def log_requests(
    request: Request, call_next: typing.Callable[[Request], typing.Awaitable[Response]]
) -> Response:
    """Middleware function for logging HTTP requests and their response times.

    Args:
        request (Request): Incoming FastAPI request object.
        call_next (Callable[[Request], Awaitable[Response]]): Next request handler in the middleware chain.

    Returns:
        Response: Processed HTTP response from the next handler.
    """
    start = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    duration = time.time() - start
    logger.info(
        f"Response status: {response.status_code} for {request.url} completed in {duration:.2f}s"
    )

    return response
