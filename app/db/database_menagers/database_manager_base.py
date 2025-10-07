from typing import List, Union

from sqlalchemy import CursorResult, delete, insert, select, text
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
#todo split it to DatabaseManagerGetter? i DatabaseManagerUpdater czy cos

class DatabaseManagerBase:
    def __init__(self, db: AsyncSession, extended: bool):
        self.db = db
        self.stmt = EXTENDED_STMT if extended else BASE_STMT
        self.fighter_schema = ExtendedFighterSchema if extended else FighterSchema

    #######################################GET METHODS#############################################


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


    async def _get_records_with_where_stmt(self, where_stmt: list):
        records = await self.db.execute(self.stmt.where(*where_stmt))
        fighters_list = records.scalars().all()

        if fighters_list is None:
            return None

        if len(fighters_list) > 1:
            return [self.fighter_schema.model_validate(fighter) for fighter in fighters_list]
        return self.fighter_schema.model_validate(fighters_list[0])


    async def get_fighter_by_name_nickname_surname(
        self, name: str, nickname: str, surname: str
    ):
        where_stmt = [Fighters.name == name,
            Fighters.nickname == nickname,
            Fighters.surname == surname]
        return await self._get_records_with_where_stmt(where_stmt)


    #######################################POST METHODS#############################################

    async def post_single_base_data_to_database(self, data: FighterFilter) -> bool:
        self.db.add(Fighters(**data))
        await self.db.commit()
        return True

    async def post_single_extended_data_to_database(self, data: dict):
        data["base_stats"] = BaseStats(**data["base_stats"])
        data["extended_stats"] = ExtendedStats(**data["extended_stats"])
        data["fights_results"] = FightsResults(**data["fights_results"])
        fighter = Fighters(**data)
        self.db.add(fighter)
        await self.db.commit()

    #######################################PUT METHODS#############################################

    async def update_base_fighter_by_id(self, fighter_id: int, data: dict) -> bool:
        fighter = await self.db.get(Fighters, fighter_id)
        for key, value in data.items():
            setattr(fighter, key, value)
        await self.db.commit()
        await self.db.refresh(fighter)
        return True

    async def update_base_fighter_name_nickname_surname(
        self, name: str, nickname: str, surname: str, data: dict
    ) -> bool:
        fighter = await self.get_fighter_by_name_nickname_surname(
            name, nickname, surname
        )
        for key, value in data.items():
            setattr(fighter, key, value)
        await self.db.commit()
        await self.db.refresh(fighter)
        return True

    async def update_extender_fighter_by_id(self, fighter_id: int, data: dict) -> bool:
        fighter = await self.db.get(Fighters, fighter_id)
        data["base_stats"] = BaseStats(**data["base_stats"])
        data["extended_stats"] = ExtendedStats(**data["extended_stats"])
        data["fights_results"] = FightsResults(**data["fights_results"])
        for key, value in data.items():
            setattr(fighter, key, value)
        await self.db.commit()
        await self.db.refresh(fighter)
        return True

    async def update_extender_fighter_name_nickname_surname(
        self, name: str, nickname: str, surname: str, data: dict
    ) -> bool:
        fighter = await self.get_fighter_by_name_nickname_surname(
            name, nickname, surname
        )
        data["base_stats"] = BaseStats(**data["base_stats"])
        data["extended_stats"] = ExtendedStats(**data["extended_stats"])
        data["fights_results"] = FightsResults(**data["fights_results"])
        for key, value in data.items():
            setattr(fighter, key, value)
        await self.db.commit()
        await self.db.refresh(fighter)
        return True

    #######################################DELETE METHODS#############################################

    async def remove_record_by_fighter_id(self, fighter_id: int):
        stmt = delete(Fighters).where(Fighters.fighter_id == fighter_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True

    #####################################OTHER METHODS#############################################
    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
