import typing

from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.services.fighters.fighter_getter import FighterGetter

extended_top_router = APIRouter(prefix="/top")

IS_EXTENDED = True


@extended_top_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_top_extended_fighters_by_wins(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[ExtendedFighterSchema] | ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "wins", limit
    )


@extended_top_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_top_fighters_by_loss(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[ExtendedFighterSchema] | ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss", limit
    )


@extended_top_router.get("/wins/ko", status_code=status.HTTP_200_OK)
async def get_top_fighters_by_ko_wins(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[ExtendedFighterSchema] | ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "win_by_ko_tko", limit
    )


@extended_top_router.get("/loss/ko", status_code=status.HTTP_200_OK)
async def get_top_fighters_by_ko_loss(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[ExtendedFighterSchema] | ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss_by_ko_tko", limit
    )
