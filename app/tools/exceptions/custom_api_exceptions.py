from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    """Exception raised when authentication fails or a token is invalid."""

    def __init__(self, detail: str = "Invalid or expired token") -> None:
        """
        Initialize an UnauthorizedException.

        Args:
            detail (str, optional): Custom error message. Defaults to "Invalid or expired token".
        """
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    """Exception raised when the user lacks permission for an action."""

    def __init__(
        self,
        detail: str = "You don't have permission to perform this action",
    ) -> None:
        """
        Initialize a ForbiddenException.

        Args:
            detail (str, optional): Custom error message. Defaults to "You don't have permission to perform this action".
        """
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(HTTPException):
    """Exception raised when a requested resource cannot be found."""

    def __init__(self, detail: str = "Resource not found") -> None:
        """
        Initialize a NotFoundException.

        Args:
            detail (str, optional): Custom error message. Defaults to "Resource not found".
        """
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InternalServerError(HTTPException):
    """Exception raised when an unexpected server error occurs."""

    def __init__(self, detail: str = "Unexpected server error") -> None:
        """
        Initialize an InternalServerError.

        Args:
            detail (str, optional): Custom error message. Defaults to "Unexpected server error".
        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
