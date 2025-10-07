from functools import wraps
from typing import Optional

from fastapi import HTTPException, Request
from pydantic import ValidationError, create_model

from app.tools.logger import logger


def handle_empty_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)

            if type(response) in (int, bool):
                pass

            elif not response or None in response or response == []:
                logger.error("Fighter/Fighters not found")
                raise HTTPException(
                    status_code=404, detail="Fighter/Fighters not found"
                )
            return response

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=404, detail="Fighter/Fighters not found")

    return wrapper


def create_filter_schema(schema):
    return create_model(
        f"{schema.__name__}Filter",
        **{
            field: (Optional[typ.annotation], None)
            for field, typ in schema.model_fields.items()
            if field not in ("fighter_id", "last_updated")
        },
    )
