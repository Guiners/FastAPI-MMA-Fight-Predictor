import typing

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.services.fighters.fighter_updater import FighterUpdater
from app.tools.utils import handle_empty_response

extended_multiple_router = APIRouter(prefix="/multiple")

IS_EXTENDED = True


@extended_multiple_router.post("", status_code=status.HTTP_201_CREATED)
async def create_multiple_extended_fighter(
    fighters_data: typing.List[ExtendedFighterFilter],
    db: AsyncSession = Depends(get_db),
):
    """Create multiple extended fighter records.

    Args:
        fighters_data (List[ExtendedFighterFilter]): List of fighter data objects to insert.
        db (AsyncSession): Active SQLAlchemy database session.

    Returns:
        dict: Confirmation message or list of created fighters.
    """
    return await FighterUpdater(db, IS_EXTENDED).add_multiple_fighters(fighters_data)


@extended_multiple_router.delete("", status_code=status.HTTP_200_OK)
@handle_empty_response
async def delete_multiple_extended_fighter(
    list_of_ids: typing.List[int] = Query, db: AsyncSession = Depends(get_db)
):
    """Delete multiple extended fighter records by ID list.

    Args:
        list_of_ids (List[int]): List of fighter IDs to delete.
        db (AsyncSession): Active SQLAlchemy database session.

    Returns:
        dict: Confirmation message for successful deletion.
    """
    return await FighterUpdater(db, IS_EXTENDED).remove_multiple_records(list_of_ids)
