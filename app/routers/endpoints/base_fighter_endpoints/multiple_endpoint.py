from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_updater import (
    FighterUpdater,
)
from app.schemas.fighter import FighterFilter
from app.tools.utils import handle_empty_response

base_multiple_router = APIRouter(prefix="/multiple")

IS_EXTENDED = False


@base_multiple_router.post("", status_code=status.HTTP_201_CREATED)
async def create_multiple_base_fighter(
    fighters_data: List[FighterFilter], db: AsyncSession = Depends(get_db)
):
    return await FighterUpdater(db, False).add_multiple_fighters(fighters_data)


@base_multiple_router.delete("", status_code=status.HTTP_200_OK)
@handle_empty_response
async def delete_multiple_base_fighter(
    list_of_ids: List[int] = Query, db: AsyncSession = Depends(get_db)
):
    return await FighterUpdater(db, False).remove_multiple_records(list_of_ids)
