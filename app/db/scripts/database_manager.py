import asyncio
import json
from typing import Union

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.db.models import Base
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_records_from_table(self, table):
        records = await self.db.execute(select(table))
        rows = records.scalars().all()
        print(f"--- Contents of {table.__name__} ---")
        return rows

    async def get_all_fighter_statistics_by(self, column: str, value: Union[str, int]):
        if not hasattr(Fighters, column):
            raise ValueError(f"Column '{column}' does not exist in Fighters model")
        column_attr = getattr(Fighters, column)

        return await self.db.execute(
            select(Fighters)
            .options(selectinload(Fighters.base_stats))
            .options(selectinload(Fighters.extended_stats))
            .options(selectinload(Fighters.fights_results))
            .where(column_attr == value)
        )

    async def get_all_available_fighter_statistics_by_id(
        self, fighter_id: int
    ) -> ExtendedFighter:
        records = await self.get_all_fighter_statistics_by("fighter_id", fighter_id)
        return ExtendedFighter.model_validate(records.scalars().first())

    async def get_data_by_fighter_id(self, table, fighter_id: int):
        return await self.db.get(table, fighter_id)

    async def clear_all_tables(self):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            print("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
