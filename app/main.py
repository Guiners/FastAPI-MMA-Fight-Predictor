from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.fighters import Fighters
from app.db.models.base_stats import BaseStats
from app.db.models.extended_stats import ExtendedStats
from app.db.models.fights_results import FightsResults

from app.schemas.fighter import Fighter as FighterSchema

from app.db.database import get_db
from app.db.scripts.database_manager import DatabaseManager

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all_fighters")
async def get_all_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[FighterSchema]:
    return await DatabaseManager(db).get_all_records_from_table(Fighters)


@app.get("/fighter/{fighter_id}")
async def get_all_fighters_list(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManager(db).get_record_by_fighter_id(Fighters, fighter_id)


@app.get("/fighter/{fighter_id}")  # todo
async def get_all_available_fighter_statistics(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManager(db).get_record_by_fighter_id(Fighters, fighter_id)
