from functools import wraps

from fastapi import HTTPException, Request
from pydantic import ValidationError

from app.tools.logger import logger


def handle_empty_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            if not response or None in response or response == []:
                logger.error("Fighter/Fighters not found")
                raise HTTPException(
                    status_code=404, detail="Fighter/Fighters not found"
                )
            return response

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=404, detail="Fighter/Fighters not found")

    return wrapper
