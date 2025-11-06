from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates

extended_country_router = APIRouter(prefix="/country")

IS_EXTENDED = True


@extended_country_router.get(
    "/{country}", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_extended_fighters_by_country(
    request: Request,
    country: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Retrieve extended fighter data for a specific country.

    Args:
        request (Request): FastAPI request object.
        country (str): The country name used to filter fighters.
        db (AsyncSession): Active SQLAlchemy session (dependency-injected).

    Returns:
        HTMLResponse: Rendered template with fighters from the given country.
    """
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_country(country)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_country_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_avg_wins_per_country(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Get the average number of wins per country.

    Args:
        request (Request): FastAPI request object.
        db (AsyncSession): Active SQLAlchemy session (dependency-injected).

    Returns:
        HTMLResponse: Rendered template showing average wins grouped by country.
    """
    results = await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="country",
        param_name2="wins",
        math_func1=func.avg,
        label1="avg_wins",
    )
    title = "Average Wins per Country"
    return templates.TemplateResponse(
        "stats.html", {"request": request, "result": results[0], "title": title}
    )


@extended_country_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_avg_loss_per_country(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    """Get the average number of losses per country.

    Args:
        request (Request): FastAPI request object.
        db (AsyncSession): Active SQLAlchemy session (dependency-injected).

    Returns:
        HTMLResponse: Rendered template showing average losses grouped by country.
    """
    results = await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="country",
        param_name2="loss",
        math_func1=func.avg,
        label1="avg_loss",
    )
    title = "Average Loss per Country"
    return templates.TemplateResponse(
        "stats.html", {"request": request, "result": results[0], "title": title}
    )
