from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates

extended_weightclass_router = APIRouter(prefix="/weightclass")

IS_EXTENDED = True


@extended_weightclass_router.get("/age", status_code=status.HTTP_200_OK)
async def get_avg_age_per_weight_class(
    request: Request, db: AsyncSession = Depends(get_db)
):
    """Retrieve the average fighter age per weight class.

    Args:
        request (Request): FastAPI request object.
        db (AsyncSession): Active SQLAlchemy asynchronous session.

    Returns:
        TemplateResponse: Rendered HTML with the average age grouped by weight class.
    """
    results = await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="age",
        math_func1=func.avg,
        label1="avg_age",
    )
    title = "Average Age per Weight Class"
    return templates.TemplateResponse(
        "stats.html", {"request": request, "result": results[0], "title": title}
    )


@extended_weightclass_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_avg_wins_per_weight_class(
    request: Request, db: AsyncSession = Depends(get_db)
):
    """Retrieve the average number of wins per weight class.

    Args:
        request (Request): FastAPI request object.
        db (AsyncSession): Active SQLAlchemy asynchronous session.

    Returns:
        TemplateResponse: Rendered HTML with the average wins grouped by weight class.
    """
    results = await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="wins",
        math_func1=func.avg,
        label1="avg_wins",
    )
    title = "Average Wins per Weight Class"
    return templates.TemplateResponse(
        "stats.html", {"request": request, "result": results[0], "title": title}
    )


@extended_weightclass_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_avg_loss_per_weight_class(
    request: Request, db: AsyncSession = Depends(get_db)
):
    """Retrieve the average number of losses per weight class.

    Args:
        request (Request): FastAPI request object.
        db (AsyncSession): Active SQLAlchemy asynchronous session.

    Returns:
        TemplateResponse: Rendered HTML with the average losses grouped by weight class.
    """
    results = await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="loss",
        math_func1=func.avg,
        label1="avg_loss",
    )
    title = "Average Loss per Weight Class"
    return templates.TemplateResponse(
        "stats.html", {"request": request, "result": results[0], "title": title}
    )
