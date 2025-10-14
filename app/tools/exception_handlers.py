from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.tools import logger
from app.tools.exceptions.custom_api_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    InternalServerError,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        logger.warning(f"Unauthorized: {exc.detail} | {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "unauthorized",
                "detail": exc.detail,
                "path": str(request.url),
            },
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        logger.warning(f"Forbidden: {exc.detail} | {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "forbidden",
                "detail": exc.detail,
                "path": str(request.url),
            },
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "not_found",
                "detail": exc.detail,
                "path": str(request.url),
            },
        )

    @app.exception_handler(InternalServerError)
    async def internal_error_handler(request: Request, exc: InternalServerError):
        logger.error(f"Internal error: {exc.detail} | {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "internal_server_error",
                "detail": exc.detail,
                "path": str(request.url),
            },
        )

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        logger.exception(f"Unexpected error: {exc} | {request.url}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "unexpected_error",
                "detail": str(exc),
                "path": str(request.url),
            },
        )
