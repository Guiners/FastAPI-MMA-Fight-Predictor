import typing

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.fighter import Fighter as FighterSchema
from app.services.fighters.fighter_getter import FighterGetter

base_top_router = APIRouter(prefix="/top")

IS_EXTENDED = False


@base_top_router.get("/wins", status_code=status.HTTP_200_OK)
async def get_top_fighters_by_wins(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[FighterSchema] | FighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "wins", limit
    )


@base_top_router.get("/loss", status_code=status.HTTP_200_OK)
async def get_top_fighters_by_loss(
    limit: int, db: AsyncSession = Depends(get_db)
) -> typing.List[FighterSchema] | FighterSchema:
    return await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss", limit
    )
