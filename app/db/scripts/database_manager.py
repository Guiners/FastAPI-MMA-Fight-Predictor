from typing import List, Union

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Base
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.logger import logger


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.stmt = select(Fighters).options(
            joinedload(Fighters.base_stats),
            joinedload(Fighters.extended_stats),
            joinedload(Fighters.fights_results),
        )  # question joinedload czy selectinload bedzie bardziej efektywny

    async def get_all_records_from_table(self, table):
        records = await self.db.execute(select(table))
        logger.info(f"Returning contents of {table.__name__}")
        fighters = [
            FighterSchema.model_validate(row) for row in records.scalars().all()
        ]
        return fighters

    async def _get_records_from_table_with_column_and_value(
        self, table, column: str, value: Union[str, int], extended: bool = False
    ):
        logger.debug(f"Trying to get data from column: {column} with value: {value}")
        if not hasattr(table, column):
            raise ValueError(f"Column '{column}' does not exist in Fighters model")
        column_attr = getattr(table, column)

        if extended:
            results = await self.db.execute(self.stmt.where(column_attr == value))
        else:
            results = await self.db.execute(select(table).where(column_attr == value))
        return results

    async def _get_all_fighter_statistics_with_dict(self, filters_dict: dict):
        filters = []
        for field, value in filters_dict.items():
            if hasattr(Fighters, field):
                column = getattr(Fighters, field)
                filters.append(column == value)
            else:
                raise ValueError(f"Column '{field}' does not exist in Fighters model")

        result = await self.db.execute(self.stmt.where(*filters))
        return result

    async def get_all_available_fighter_statistics_by_id(
        self, fighter_id: int
    ) -> Union[ExtendedFighter, None]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "fighter_id", fighter_id, True
        )
        fighter = records.scalars().first()
        if fighter is None:
            return None
        return ExtendedFighter.model_validate(fighter)

    async def get_data_by_fighter_id(
        self, table, fighter_id: int
    ) -> Union[FighterSchema, None]:
        fighter = await self.db.get(table, fighter_id)
        if fighter is None:
            return None
        return FighterSchema.model_validate(fighter)

    async def get_fighters_by_country(
        self, country: str
    ) -> Union[list[FighterSchema], None]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "country", country
        )
        fighters = records.scalars().all()
        if fighters is None:
            return None
        return [FighterSchema.model_validate(fighter) for fighter in fighters]

    async def get_all_available_fighter_statistics_by_country(
        self, country: str
    ) -> Union[list[ExtendedFighter], None]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "country", country, True
        )
        fighters = records.scalars().all()
        if fighters is None:
            return None
        return [ExtendedFighter.model_validate(fighter) for fighter in fighters]

    async def get_all_available_fighter_statistics_by_own_parameters(
        self, fighter_filters: FighterFilter
    ) -> Union[list[ExtendedFighter], None]:
        filters = fighter_filters.dict(exclude_none=True)
        logger.debug(f"fighter filter: {filters}")
        records = await self._get_all_fighter_statistics_with_dict(filters)
        fighters = records.scalars().all()
        if fighters is None:
            return None
        return [ExtendedFighter.model_validate(fighter) for fighter in fighters]

    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
