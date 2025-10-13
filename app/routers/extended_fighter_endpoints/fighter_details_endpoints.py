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
from app.tools.tools import handle_empty_response

extended_fighter_details_router = APIRouter(prefix="/fighter_details")

IS_EXTENDED = True


@extended_fighter_details_router.get(
    "/name/{name}/nickname/{nickname}/surname/{surname}"
)
@handle_empty_response
async def get_extended_fighter_by_name_nickname_surname(
    name: str, nickname: str, surname: str, db: AsyncSession = Depends(get_db)
) -> ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighter_by_name_nickname_surname(
        name, nickname, surname
    )


@extended_fighter_details_router.put(
    "/name/{name}/nickname/{nickname}/surname/{surname}"
)
@handle_empty_response
async def update_extended_fighter_by_name(
    name: str,
    nickname: str,
    surname: str,
    fighter_data: ExtendedFighterFilter,
    db: AsyncSession = Depends(get_db),
):
    return await FighterUpdater(
        db, IS_EXTENDED
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)
