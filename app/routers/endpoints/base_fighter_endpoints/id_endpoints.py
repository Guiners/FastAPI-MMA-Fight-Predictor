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

base_id_router = APIRouter(prefix="/id")

IS_EXTENDED = False


@base_id_router.get(
    "/{fighter_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_base_fighter_by_id(
    request: Request,
    fighter_id: int,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve a fighter's details by their ID and render them as HTML.

    Args:
        request (Request): FastAPI request object.
        fighter_id (int): Unique fighter identifier.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        HTMLResponse: Rendered template with fighter data.
    """
    fighter = await FighterGetter(db, IS_EXTENDED).get_fighter_by_id(fighter_id)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighter}
    )


@base_id_router.delete("/{fighter_id}", status_code=status.HTTP_200_OK)
@handle_empty_response
async def delete_base_fighter(
    fighter_id: int,
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    """Delete a fighter record by its ID.

    Args:
        fighter_id (int): Unique fighter identifier.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        dict: Confirmation or result of the deletion.
    """
    return await FighterUpdater(db, IS_EXTENDED).remove_record_by_fighter_id(fighter_id)


@base_id_router.put("/{fighter_id}", status_code=status.HTTP_202_ACCEPTED)
@handle_empty_response
async def update_base_fighter_by_id(
    fighter_id: int,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    """Update fighter details by their ID.

    Args:
        fighter_id (int): Unique fighter identifier.
        fighter_data (FighterFilter): Updated fighter information.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        dict: Updated fighter record.
    """
    return await FighterUpdater(db, IS_EXTENDED).update_fighter_by_id(
        fighter_id, fighter_data
    )
