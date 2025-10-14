from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import (
    FighterGetter,
)
from app.services.fighters.fighter_updater import (
    FighterUpdater,
)
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.utils import handle_empty_response

base_fighter_details_router = APIRouter(prefix="/fighter_details")

IS_EXTENDED = False


@base_fighter_details_router.get(
    "/name/{name}/nickname/{nickname}/surname/{surname}", status_code=status.HTTP_200_OK
)
@handle_empty_response
async def get_base_fighter_by_name_nickname_surname(
    name: str, nickname: str, surname: str, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighter_by_name_nickname_surname(
        name, nickname, surname
    )


@base_fighter_details_router.put(
    "/name/{name}/nickname/{nickname}/surname/{surname}",
    status_code=status.HTTP_202_ACCEPTED,
)
@handle_empty_response
async def update_base_fighter_by_name(
    name: str,
    nickname: str,
    surname: str,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await FighterUpdater(
        db, IS_EXTENDED
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)
