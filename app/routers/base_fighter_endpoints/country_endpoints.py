from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.fighters_database_managers.fighter_database_manager_getter import \
    DatabaseManagerGetter
from app.schemas.fighter import Fighter as FighterSchema
from app.tools.tools import handle_empty_response

base_country_router = APIRouter(prefix="/country")

IS_EXTENDED = False


@base_country_router.get("/{country}")
@handle_empty_response
async def get_fighters_data_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> Union[List[FighterSchema], FighterSchema]:
    return await DatabaseManagerGetter(db, IS_EXTENDED).get_fighters_by_country(country)
