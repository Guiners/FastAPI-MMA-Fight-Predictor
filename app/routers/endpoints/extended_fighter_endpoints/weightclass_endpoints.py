import typing

from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.services.fighters.fighter_getter import FighterGetter

extended_weightclass_router = APIRouter(prefix="/weightclass")

IS_EXTENDED = True


@extended_weightclass_router.get("/age", status_code=status.HTTP_200_OK)
async def get_avg_age_per_weightclass(db: AsyncSession = Depends(get_db)):
    return await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="age",
        math_func1=func.avg,
        label1="avg_age",
    )


@extended_weightclass_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_avg_wins_per_weightclass(db: AsyncSession = Depends(get_db)):
    return await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="wins",
        math_func1=func.avg,
        label1="avg_wins",
    )


@extended_weightclass_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_avg_loss_per_weightclass(db: AsyncSession = Depends(get_db)):
    return await FighterGetter(db, IS_EXTENDED).get_grouped_stat(
        param_name1="weight_class",
        param_name2="loss",
        math_func1=func.avg,
        label1="avg_loss",
    )
