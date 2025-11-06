from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.services.fighters.fighter_updater import FighterUpdater
from app.templates import templates
from app.tools.utils import handle_empty_response

extended_fighter_details_router = APIRouter(prefix="/fighter_details")

IS_EXTENDED = True


@extended_fighter_details_router.get(
    "/name/{name}/nickname/{nickname}/surname/{surname}",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def get_extended_fighter_by_name_nickname_surname(
    request: Request,
    name: str,
    nickname: str,
    surname: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve extended fighter details by name, nickname, and surname.

    Args:
        request (Request): FastAPI request object.
        name (str): Fighter’s first name.
        nickname (str): Fighter’s nickname.
        surname (str): Fighter’s surname.
        db (AsyncSession): Active SQLAlchemy session (dependency-injected).

    Returns:
        HTMLResponse: Rendered HTML template with the fighter’s data.
    """
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
    """Update extended fighter data using name, nickname, and surname.

    Args:
        name (str): Fighter’s first name.
        nickname (str): Fighter’s nickname.
        surname (str): Fighter’s surname.
        fighter_data (ExtendedFighterFilter): New fighter data to update.
        db (AsyncSession): Active SQLAlchemy session (dependency-injected).

    Returns:
        dict: Confirmation of update operation or the updated fighter data.
    """
    return await FighterUpdater(
        db, IS_EXTENDED
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)
