import asyncio
import json

from sqlalchemy import select, text

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload, joinedload

from app.db.models import Base
from app.db.models.fighters import Fighters


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_records_from_table(self, table):
        records = await self.db.execute(select(table))
        rows = records.scalars().all()
        print(f"--- Contents of {table.__name__} ---")
        return rows

    async def get_all_available_fighter_statistics_by_id(self, fighter_id):
        records = await self.db.execute(
            select(Fighters)
            .options(joinedload(Fighters.base_stats))
            .options(joinedload(Fighters.extended_stats))
            .options(joinedload(Fighters.fight_results))
        )
        #todo posprawdzac http://localhost:8000/docs
        records = await self.db.execute(
            select(Fighters)
            .options(selectinload(Fighters.base_stats))
            .options(selectinload(Fighters.extended_stats))
            .options(selectinload(Fighters.fight_results))
        )
        fighter_info = records.unique().all()

    async def get_record_by_fighter_id(self, table, fighter_id: int):
        return await self.db.get(table, fighter_id)


    async def clear_all_tables(self):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            print("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
