from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates

base_top_router = APIRouter(prefix="/top")

IS_EXTENDED = False


@base_top_router.get(
    "/wins",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def get_top_fighters_by_wins(
    request: Request,
    limit: int,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve the top fighters ranked by number of wins.

    Args:
        request (Request): The FastAPI request object.
        limit (int): The maximum number of fighters to retrieve.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        HTMLResponse: Rendered HTML page displaying top fighters by wins.
    """
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "wins", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@base_top_router.get(
    "/loss",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def get_top_fighters_by_loss(
    request: Request,
    limit: int,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve the top fighters ranked by number of losses.

    Args:
        request (Request): The FastAPI request object.
        limit (int): The maximum number of fighters to retrieve.
        db (AsyncSession): Active database session (dependency-injected).

    Returns:
        HTMLResponse: Rendered HTML page displaying top fighters by losses.
    """
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )
