from typing import List, Union

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Base
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter
from app.schemas.fighter import Fighter as FighterSchema
from app.utils.logger import logger


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_records_from_table(self, table):
        records = await self.db.execute(select(table))
        logger.info(f"Returning contents of {table.__name__}")
        fighters = [
            FighterSchema.model_validate(row) for row in records.scalars().all()
        ]
        return fighters

    async def _get_all_fighter_statistics_by(self, column: str, value: Union[str, int]):
        logger.debug(f"Trying to get data from column: {column} with value: {value}")
        if not hasattr(Fighters, column):
            raise ValueError(f"Column '{column}' does not exist in Fighters model")
        column_attr = getattr(Fighters, column)

        result = await self.db.execute(
            select(Fighters)
            .options(selectinload(Fighters.base_stats))
            .options(selectinload(Fighters.extended_stats))
            .options(selectinload(Fighters.fights_results))
            .where(column_attr == value)
        )
        logger.info(f"Successfully got data from column: {column} with value: {value}")
        return result

    async def _get_records_from_table_with_column_and_value(
        self, table, column: str, value: Union[str, int]
    ):
        logger.debug(f"Trying to get data from column: {column} with value: {value}")
        if not hasattr(Fighters, column):
            raise ValueError(f"Column '{column}' does not exist in Fighters model")
        column_attr = getattr(table, column)
        results = await self.db.execute(select(table).where(column_attr == value))
        records = results.scalars().all()
        logger.info(f"Successfully got data from column: {column} with value: {value}")
        return records

    async def get_all_available_fighter_statistics_by_id(
        self, fighter_id: int
    ) -> ExtendedFighter:
        records = await self._get_all_fighter_statistics_by("fighter_id", fighter_id)
        fighter = records.scalars().first()
        return ExtendedFighter.model_validate(fighter)

    async def get_data_by_fighter_id(self, table, fighter_id: int) -> FighterSchema:
        fighter = await self.db.get(table, fighter_id)
        return FighterSchema.model_validate(fighter)

    async def get_fighters_by_country(self, country: str) -> List[ExtendedFighter]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "country", country
        )
        return [ExtendedFighter.model_validate(fighter) for fighter in records]

    async def get_all_available_fighter_statistics_by_country(
        self, country: str
    ) -> list[ExtendedFighter]:
        records = await self._get_all_fighter_statistics_by("country", country)
        fighters = records.scalars().all()
        return [ExtendedFighter.model_validate(fighter) for fighter in fighters]

    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
