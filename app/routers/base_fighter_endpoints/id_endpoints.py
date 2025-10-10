from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.fighters_database_managers.fighter_database_manager_getter import \
    DatabaseManagerGetter
from app.db.database_menagers.fighters_database_managers.fighter_database_manager_updater import \
    DatabaseManagerUpdater
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.tools import handle_empty_response

base_id_router = APIRouter(prefix="/id")

IS_EXTENDED = False


@base_id_router.get("/{fighter_id}")
@handle_empty_response
async def get_base_fighter_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManagerGetter(db, IS_EXTENDED).get_fighter_by_id(fighter_id)


@base_id_router.delete("/{fighter_id}")
@handle_empty_response
async def delete_base_fighter(fighter_id: int, db: AsyncSession = Depends(get_db)):
    return await DatabaseManagerUpdater(db, IS_EXTENDED).remove_record_by_fighter_id(
        fighter_id
    )


@base_id_router.put("/{fighter_id}")
@handle_empty_response
async def update_base_fighter_by_id(
    fighter_id: int,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await DatabaseManagerUpdater(db, IS_EXTENDED).update_fighter_by_id(
        fighter_id, fighter_data
    )
