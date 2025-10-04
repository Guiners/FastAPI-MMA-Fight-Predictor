from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.base_stats import BaseStats
from app.db.models.extended_stats import ExtendedStats
from app.db.models.fighters import Fighters
from app.db.models.fights_results import FightsResults
from app.db.scripts.database_manager import DatabaseManager
from app.middleware.middlewares import log_requests
from app.schemas.extended_fighter import ExtendedFighter, ExtendedFighterFilter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.tools import handle_empty_response

app = FastAPI()

app.middleware("http")(log_requests)


@app.get("/")
async def root():
    return {"message": "Hello World"}


#######################################GET METHODS#############################################


@app.get("/all_fighters")
@handle_empty_response
async def get_all_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[FighterSchema]:
    return await DatabaseManager(db).get_all_records_from_table(Fighters)


@app.get("/fighter/id/{fighter_id}")
@handle_empty_response
async def get_fighter_data_by_fighter_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManager(db).get_data_by_fighter_id(Fighters, fighter_id)


@app.get("/fighter/country/{country}")
@handle_empty_response
async def get_fighters_data_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> List[FighterSchema]:
    return await DatabaseManager(db).get_fighters_by_country(country)


@app.get("/extended_fighter_stats/id/{fighter_id}")
@handle_empty_response
async def get_all_available_fighter_statistics_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> ExtendedFighter:
    return await DatabaseManager(db).get_all_available_fighter_statistics_by_id(
        fighter_id
    )


@app.get("/extended_fighter_stats/country/{country}")
@handle_empty_response
async def get_all_available_fighter_statistics_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> List[ExtendedFighter]:
    return await DatabaseManager(db).get_all_available_fighter_statistics_by_country(
        country
    )


@app.get("/extended_fighter_stats/search")
@handle_empty_response
async def search_fighters(
    fighter_filters: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
) -> List[ExtendedFighter]:
    return await DatabaseManager(
        db
    ).get_all_available_fighter_statistics_by_own_parameters(fighter_filters)


#######################################POST METHODS#############################################


@app.post("/create_base_fighter")
async def create_base_fighter(
    fighter_data: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
):
    data_to_add = fighter_data.dict(exclude_none=True)
    return await DatabaseManager(db).post_single_base_data_to_database(data_to_add)


@app.post("/create_multiple_base_fighter")
async def create_multiple_base_fighter(
    fighters_data: List[FighterFilter], db: AsyncSession = Depends(get_db)
):
    db_responses = []
    for fighter_data in fighters_data:
        fighter = fighter_data.dict(exclude_none=True)
        response = await DatabaseManager(db).post_single_base_data_to_database(fighter)
        db_responses.append(response)

    return db_responses


@app.post("/create_extended_fighter")
async def create_extended_fighter(
    fighter_data: ExtendedFighter = Depends(), db: AsyncSession = Depends(get_db)
):
    data_to_add = fighter_data.dict(exclude_none=True)
    return await DatabaseManager(db).post_single_base_data_to_database(data_to_add)