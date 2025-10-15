from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.database_manager_getter import \
    DatabaseManagerGetter
from app.db.database_menagers.database_manager_updater import \
    DatabaseManagerUpdater
from app.routers.base_fighter_endpoints.country_endpoints import \
    base_country_router
from app.routers.base_fighter_endpoints.fighter_details_endpoints import \
    base_fighter_details_router
from app.routers.base_fighter_endpoints.id_endpoints import base_id_router
from app.routers.base_fighter_endpoints.multiple_endpoint import \
    base_multiple_router
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.tools import handle_empty_response

base_fighter_router = APIRouter(prefix="/base_fighter")

base_fighter_router.include_router(base_id_router)
base_fighter_router.include_router(base_country_router)
base_fighter_router.include_router(base_fighter_details_router)
base_fighter_router.include_router(base_multiple_router)

IS_EXTENDED = False


@base_fighter_router.get("")
@handle_empty_response
async def get_all_base_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[FighterSchema]:
    return await DatabaseManagerGetter(db, IS_EXTENDED).get_all_fighters_records()


@base_fighter_router.post("")
async def create_base_fighter(
    fighter_data: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, IS_EXTENDED).add_fighter(fighter_data)
