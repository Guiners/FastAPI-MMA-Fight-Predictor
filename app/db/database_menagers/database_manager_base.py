from typing import Union

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Base, BaseStats, ExtendedStats, FightsResults
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.logger import logger

BASE_STMT = select(Fighters)
EXTENDED_STMT = select(Fighters).options(
    joinedload(Fighters.base_stats),
    joinedload(Fighters.extended_stats),
    joinedload(Fighters.fights_results),
)


class DatabaseManagerBase:
    def __init__(self, db: AsyncSession, extended: bool):
        self.db = db
        self.is_extended = extended
        self.stmt = EXTENDED_STMT if extended else BASE_STMT
        self.fighter_schema = ExtendedFighterSchema if extended else FighterSchema

    @staticmethod
    def build_where_stmt(filters: Union[FighterFilter, ExtendedFighterFilter]):
        filters_dict = filters.dict(exclude_none=True)
        logger.debug(f"fighter filter: {filters_dict}")
        where_stmt = []
        for field, value in filters_dict.items():
            if hasattr(Fighters, field):
                column = getattr(Fighters, field)
                where_stmt.append(column == value)
            else:
                raise ValueError(f"Column '{field}' does not exist in Fighters model")
        return where_stmt

    @staticmethod
    def convert_stats_dicts_to_models(data):
        data["base_stats"] = BaseStats(**data["base_stats"])
        data["extended_stats"] = ExtendedStats(**data["extended_stats"])
        data["fights_results"] = FightsResults(**data["fights_results"])

    async def _get_records_with_where_stmt(
        self, where_stmt: list, validate: bool = True
    ):
        records = await self.db.execute(self.stmt.where(*where_stmt))
        fighters_list = records.scalars().all()

        if not fighters_list:
            return None

        convert = self.fighter_schema.model_validate if validate else (lambda x: x)

        if len(fighters_list) > 1:
            return [convert(fighter) for fighter in fighters_list]

        return convert(fighters_list[0])

    # todo typing
    async def _get_records_by_single_value(
        self, column: str, value: Union[str, int], validate: bool = True
    ):
        column_attr = getattr(Fighters, column)
        return await self._get_records_with_where_stmt([column_attr == value], validate)

    async def get_fighter_by_name_nickname_surname(
        self, name: str, nickname: str, surname: str, validate: bool = True
    ):
        where_stmt = [
            Fighters.name == name,
            Fighters.nickname == nickname,
            Fighters.surname == surname,
        ]
        return await self._get_records_with_where_stmt(where_stmt, validate)

    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info(f"Truncating: {table}")
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
