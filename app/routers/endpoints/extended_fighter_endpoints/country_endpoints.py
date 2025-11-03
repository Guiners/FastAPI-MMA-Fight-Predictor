import typing

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates
from app.tools.utils import handle_empty_response

extended_country_router = APIRouter(prefix="/country")

IS_EXTENDED = True


@extended_country_router.get("/{country}", status_code=status.HTTP_200_OK)
async def get_extended_fighters_by_country(
    request: Request, country: str, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_country(country)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_country_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_avg_wins_per_country(db: AsyncSession = Depends(get_db)):
    return await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="country",
        param_name2="wins",
        math_func1=func.avg,
        label1="avg_wins",
    )


@extended_country_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_avg_loss_per_country(db: AsyncSession = Depends(get_db)):
    return await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="country",
        param_name2="loss",
        math_func1=func.avg,
        label1="avg_loss",
    )
