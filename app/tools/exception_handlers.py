from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.tools import logger
from app.tools.exceptions.custom_api_exceptions import (
    ForbiddenException,
    InternalServerError,
    NotFoundException,
    UnauthorizedException,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers for the FastAPI application.

    This function attaches global handlers for known exceptions (e.g. `UnauthorizedException`)
    and a fallback handler for unexpected errors.
    Each handler logs the error and returns a structured JSON response.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request, exc: UnauthorizedException
    ) -> JSONResponse:
        """
        Handle `UnauthorizedException` raised during request processing.

        Args:
            request (Request): The incoming HTTP request.
            exc (UnauthorizedException): The raised exception.

        Returns:
            JSONResponse: JSON response with status 401 and error details.
        """
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
    async def forbidden_handler(
        request: Request, exc: ForbiddenException
    ) -> JSONResponse:
        """
        Handle `ForbiddenException`.

        Args:
            request (Request): The incoming HTTP request.
            exc (ForbiddenException): The raised exception.

        Returns:
            JSONResponse: JSON response with status 403 and error details.
        """
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
    async def not_found_handler(
        request: Request, exc: NotFoundException
    ) -> JSONResponse:
        """
        Handle `NotFoundException`.

        Args:
            request (Request): The incoming HTTP request.
            exc (NotFoundException): The raised exception.

        Returns:
            JSONResponse: JSON response with status 404 and error details.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "not_found",
                "detail": exc.detail,
                "path": str(request.url),
            },
        )

    @app.exception_handler(InternalServerError)
    async def internal_error_handler(
        request: Request, exc: InternalServerError
    ) -> JSONResponse:
        """
        Handle `InternalServerError`.

        Args:
            request (Request): The incoming HTTP request.
            exc (InternalServerError): The raised exception.

        Returns:
            JSONResponse: JSON response with status 500 and error details.
        """
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
    async def global_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handle all unexpected exceptions.

        Args:
            request (Request): The incoming HTTP request.
            exc (Exception): The unhandled exception.

        Returns:
            JSONResponse: JSON response with status 500 and generic error details.
        """
        logger.exception(f"Unexpected error: {exc} | {request.url}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "unexpected_error",
                "detail": str(exc),
                "path": str(request.url),
            },
        )
