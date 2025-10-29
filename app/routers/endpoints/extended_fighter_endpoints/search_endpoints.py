import typing

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.tools.utils import handle_empty_response

extended_search_router = APIRouter(prefix="/search")

IS_EXTENDED = True


@extended_search_router.get("", status_code=status.HTTP_200_OK)
@handle_empty_response
async def search_fighters(
    fighter_filters: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
) -> typing.List[ExtendedFighterSchema]|ExtendedFighterSchema:
    return await FighterGetter(db, IS_EXTENDED).search_extended_fighter(fighter_filters)
