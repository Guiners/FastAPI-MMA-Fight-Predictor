from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import (
    FighterGetter,
)
from app.services.fighters.fighter_updater import (
    FighterUpdater,
)
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.tools.utils import handle_empty_response

extended_id_router = APIRouter(prefix="/id")

IS_EXTENDED = True


@extended_id_router.get("/{fighter_id}")
@handle_empty_response
async def get_extended_fighter_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> ExtendedFighterSchema:
    return await FighterGetter(db, True).get_fighter_by_id(fighter_id)


@extended_id_router.put("/{fighter_id}")
@handle_empty_response
async def update_extended_fighter_by_id(
    fighter_id: int,
    fighter_data: ExtendedFighterFilter,
    db: AsyncSession = Depends(get_db),
):
    return await FighterUpdater(db, True).update_fighter_by_id(fighter_id, fighter_data)


@extended_id_router.delete("/{fighter_id}")
@handle_empty_response
async def delete_extended_fighter(fighter_id: int, db: AsyncSession = Depends(get_db)):
    return await FighterUpdater(db, True).remove_record_by_fighter_id(fighter_id)
