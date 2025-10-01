from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.base_stats import BaseStats
from app.db.models.extended_stats import ExtendedStats
from app.db.models.fighters import Fighters
from app.db.models.fights_results import FightsResults
from app.db.scripts.database_manager import DatabaseManager
from app.middleware.middlewares import log_requests
from app.schemas.extended_fighter import ExtendedFighter
from app.schemas.fighter import Fighter as FighterSchema

app = FastAPI()

app.middleware("http")(log_requests)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all_fighters")
async def get_all_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[FighterSchema]:
    return await DatabaseManager(db).get_all_records_from_table(Fighters)


@app.get("/fighter/id/{fighter_id}")
async def get_fighter_data_by_fighter_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManager(db).get_data_by_fighter_id(Fighters, fighter_id)


@app.get("/fighter/country/{country}")
async def get_fighters_data_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> List[FighterSchema]:
    return await DatabaseManager(db).get_fighters_by_country(country)


@app.get("/extended_fighter_stats/id/{fighter_id}")
async def get_all_available_fighter_statistics_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> ExtendedFighter:
    return await DatabaseManager(db).get_all_available_fighter_statistics_by_id(
        fighter_id
    )


@app.get("/extended_fighter_stats/country/{country}")
async def get_all_available_fighter_statistics_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> List[ExtendedFighter]:
    return await DatabaseManager(db).get_all_available_fighter_statistics_by_country(
        country
    )
