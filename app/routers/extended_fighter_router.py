from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import (
    FighterGetter,
)
from app.services.fighters.fighter_updater import FighterUpdater
from app.routers.endpoints.extended_fighter_endpoints.country_endpoints import (
    extended_country_router,
)
from app.routers.endpoints.extended_fighter_endpoints.fighter_details_endpoints import (
    extended_fighter_details_router,
)
from app.routers.endpoints.extended_fighter_endpoints.id_endpoints import (
    extended_id_router,
)
from app.routers.endpoints.extended_fighter_endpoints.multiple_endpoint import (
    extended_multiple_router,
)
from app.routers.endpoints.extended_fighter_endpoints.search_endpoints import (
    extended_search_router,
)
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.tools.utils import handle_empty_response

extended_fighter_router = APIRouter(prefix="/extended_fighter")

extended_fighter_router.include_router(extended_id_router)
extended_fighter_router.include_router(extended_country_router)
extended_fighter_router.include_router(extended_fighter_details_router)
extended_fighter_router.include_router(extended_multiple_router)
extended_fighter_router.include_router(extended_search_router)

IS_EXTENDED = True


@extended_fighter_router.get("", status_code=status.HTTP_200_OK)
@handle_empty_response
async def get_all_extended_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[ExtendedFighterSchema]:
    return await FighterGetter(db, IS_EXTENDED).get_all_fighters_records()


@extended_fighter_router.post("", status_code=status.HTTP_201_CREATED)
async def create_extended_fighter(
    fighter_data: ExtendedFighterFilter, db: AsyncSession = Depends(get_db)
):
    return await FighterUpdater(db, IS_EXTENDED).add_fighter(fighter_data)
