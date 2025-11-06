import typing
from functools import wraps

from pydantic import BaseModel, create_model

from app.tools.exceptions.custom_api_exceptions import NotFoundException
from app.tools.logger import logger


def handle_empty_response(
    func: typing.Callable[..., typing.Awaitable[typing.Any]]
) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
    """
    Decorator that ensures async DB/service functions don't return empty responses.

    If the wrapped function returns an empty iterable, `None`, or an unexpected value,
    this decorator logs the issue and raises a `NotFoundException`.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> typing.Any:
        try:
            response = await func(*args, **kwargs)

            # Allow integers/bools (e.g., affected row counts, success flags)
            if isinstance(response, (int, bool)):
                return response

            # Detect empty/invalid results
            if (
                response is None
                or response == []
                or (isinstance(response, (list, tuple, set, dict)) and not response)
                or (
                    isinstance(response, (list, tuple))
                    and any(item is None for item in response)
                )
            ):
                logger.error("Fighter/Fighters not found or response empty")
                raise NotFoundException

            return response

        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise NotFoundException from e

    return wrapper


def create_filter_schema(schema: typing.Type[BaseModel]) -> typing.Type[BaseModel]:
    """
    Dynamically creates a Pydantic filter model from another model class.

    All fields except 'fighter_id' and 'last_updated' become optional,
    allowing flexible query filters for search endpoints.
    """
    return create_model(
        f"{schema.__name__}Filter",
        **{
            field: (typing.Optional[field_info.annotation], None)
            for field, field_info in schema.model_fields.items()
            if field not in ("fighter_id", "last_updated")
        },
    )
