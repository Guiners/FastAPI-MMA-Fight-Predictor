import typing

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.services.fighters.fighter_updater import FighterUpdater
from app.templates import templates
from app.tools.utils import handle_empty_response

base_fighter_details_router = APIRouter(prefix="/fighter_details")

IS_EXTENDED = False


@base_fighter_details_router.get(
    "/name/{name}/nickname/{nickname}/surname/{surname}",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def get_base_fighter_by_name_nickname_surname(
    request: Request,
    name: str,
    nickname: str,
    surname: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve and render fighter data by full name and nickname.

    Args:
        request (Request): FastAPI request object.
        name (str): Fighter's first name.
        nickname (str): Fighter's nickname.
        surname (str): Fighter's last name.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        HTMLResponse: Rendered HTML template with fighter details.
    """
    fighters = await FighterGetter(
        db, IS_EXTENDED
    ).get_fighter_by_name_nickname_surname(name, nickname, surname)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
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
) -> typing.Dict[str, typing.Any]:
    """Update fighter data by name, nickname, and surname.

    Args:
        name (str): Fighter's first name.
        nickname (str): Fighter's nickname.
        surname (str): Fighter's last name.
        fighter_data (FighterFilter): Filter or data payload for updating fighter details.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        dict: Updated fighter record or confirmation of successful update.
    """
    return await FighterUpdater(
        db, IS_EXTENDED
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)
