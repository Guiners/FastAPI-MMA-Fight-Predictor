from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.database_manager_getter import \
    DatabaseManagerGetter
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.tools.tools import handle_empty_response

extended_country_router = APIRouter(prefix="/country")

IS_EXTENDED = True


@extended_country_router.get("/{country}")
@handle_empty_response
async def get_extended_fighters_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> Union[List[ExtendedFighterSchema], ExtendedFighterSchema]:
    return await DatabaseManagerGetter(db, IS_EXTENDED).get_fighters_by_country(country)
