import typing

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_updater import FighterUpdater
from app.tools.utils import handle_empty_response

base_multiple_router = APIRouter(prefix="/multiple")

IS_EXTENDED = False


@base_multiple_router.post("", status_code=status.HTTP_201_CREATED)
async def create_multiple_base_fighter(
    fighters_data: typing.List[FighterFilter],
    db: AsyncSession = Depends(get_db),
) -> typing.List[typing.Dict[str, typing.Any]]:
    """Create multiple fighter records in the database.

    Args:
        fighters_data (List[FighterFilter]): A list of fighter objects to be added.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        List[Dict[str, Any]]: A list of created fighter records.
    """
    return await FighterUpdater(db, IS_EXTENDED).add_multiple_fighters(fighters_data)


@base_multiple_router.delete("", status_code=status.HTTP_200_OK)
@handle_empty_response
async def delete_multiple_base_fighter(
    list_of_ids: typing.List[int] = Query(...),
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    """Delete multiple fighter records based on their IDs.

    Args:
        list_of_ids (List[int]): A list of fighter IDs to be deleted.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        Dict[str, Any]: Result of the deletion operation.
    """
    return await FighterUpdater(db, IS_EXTENDED).remove_multiple_records(list_of_ids)
