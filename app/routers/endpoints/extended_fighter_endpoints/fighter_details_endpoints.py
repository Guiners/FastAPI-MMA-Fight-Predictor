from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.services.fighters.fighter_updater import FighterUpdater
from app.templates import templates
from app.tools.utils import handle_empty_response

extended_fighter_details_router = APIRouter(prefix="/fighter_details")

IS_EXTENDED = True


@extended_fighter_details_router.get(
    "/name/{name}/nickname/{nickname}/surname/{surname}", status_code=status.HTTP_200_OK
)
async def get_extended_fighter_by_name_nickname_surname(
    request: Request,
    name: str,
    nickname: str,
    surname: str,
    db: AsyncSession = Depends(get_db),
):
    fighters = await FighterGetter(
        db, IS_EXTENDED
    ).get_fighter_by_name_nickname_surname(name, nickname, surname)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_fighter_details_router.put(
    "/name/{name}/nickname/{nickname}/surname/{surname}",
    status_code=status.HTTP_202_ACCEPTED,
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
