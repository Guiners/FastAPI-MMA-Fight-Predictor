from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.database_manager_updater import \
    DatabaseManagerUpdater
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.tools.tools import handle_empty_response

extended_multiple_router = APIRouter(prefix="/multiple")

IS_EXTENDED = True


@extended_multiple_router.post("")
async def create_multiple_extended_fighter(
    fighters_data: List[ExtendedFighterFilter], db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, IS_EXTENDED).add_multiple_fighters(
        fighters_data
    )


@extended_multiple_router.delete("")
@handle_empty_response
async def delete_multiple_extended_fighter(
    list_of_ids: List[int] = Query, db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, IS_EXTENDED).remove_multiple_records(
        list_of_ids
    )
