import typing

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.endpoints.base_fighter_endpoints.country_endpoints import (
    base_country_router,
)
from app.routers.endpoints.base_fighter_endpoints.fighter_details_endpoints import (
    base_fighter_details_router,
)
from app.routers.endpoints.base_fighter_endpoints.id_endpoints import base_id_router
from app.routers.endpoints.base_fighter_endpoints.multiple_endpoint import (
    base_multiple_router,
)
from app.routers.endpoints.base_fighter_endpoints.top_fighter_endpoints import (
    base_top_router,
)
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.services.fighters.fighter_updater import FighterUpdater
from app.templates import templates

base_fighter_router = APIRouter(prefix="/base_fighter", tags=["Base Fighter"])

base_fighter_router.include_router(base_id_router)
base_fighter_router.include_router(base_country_router)
base_fighter_router.include_router(base_fighter_details_router)
base_fighter_router.include_router(base_multiple_router)
base_fighter_router.include_router(base_top_router)

IS_EXTENDED = False


@base_fighter_router.get(
    "", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_all_base_fighters_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """
    Retrieve a list of all base fighters.

    Args:
        request (Request): The incoming HTTP request.
        db (AsyncSession): Asynchronous database session.

    Returns:
        HTMLResponse: Rendered HTML page displaying the list of fighters.
    """
    fighters = await FighterGetter(db, IS_EXTENDED).get_all_fighters_records()
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@base_fighter_router.post("", status_code=status.HTTP_201_CREATED)
async def create_base_fighter(
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    """
    Create a new base fighter record.

    Args:
        fighter_data (FighterFilter): Data used to create a new fighter.
        db (AsyncSession): Asynchronous database session.

    Returns:
        typing.Dict[str, typing.Any]: Information about the newly created fighter.
    """
    return await FighterUpdater(db, IS_EXTENDED).add_fighter(fighter_data)
