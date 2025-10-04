from typing import List, Union

from sqlalchemy import insert, select, text, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Base
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.logger import logger


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.extended_fighter_stmt = select(Fighters).options(
            joinedload(Fighters.base_stats),
            joinedload(Fighters.extended_stats),
            joinedload(Fighters.fights_results),
        )  # question joinedload czy selectinload bedzie bardziej efektywny

    #######################################GET METHODS#############################################

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
            results = await self.db.execute(
                self.extended_fighter_stmt.where(column_attr == value)
            )
        else:
            results = await self.db.execute(select(table).where(column_attr == value))
        return results

    @staticmethod
    def build_filters_from_model(_filters: FighterFilter, table=Fighters):
        filters_dict = _filters.dict(exclude_none=True)
        logger.debug(f"fighter filter: {filters_dict}")
        filters = []
        for field, value in filters_dict.items():
            if hasattr(table, field):
                column = getattr(table, field)
                filters.append(column == value)
            else:
                raise ValueError(f"Column '{field}' does not exist in Fighters model")
        # todo can be moved in tools, can be extended to work also to extended fighter
        return filters

    async def get_all_available_fighter_statistics_by_id(
        self, fighter_id: int
    ) -> Union[ExtendedFighterSchema, None]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "fighter_id", fighter_id, True
        )
        fighter = records.scalars().first()
        if fighter is None:
            return None
        return ExtendedFighterSchema.model_validate(fighter)

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
    ) -> Union[list[ExtendedFighterSchema], None]:
        records = await self._get_records_from_table_with_column_and_value(
            Fighters, "country", country, True
        )
        fighters = records.scalars().all()
        if fighters is None:
            return None
        return [ExtendedFighterSchema.model_validate(fighter) for fighter in fighters]

    async def get_all_available_fighter_statistics_by_own_parameters(
        self, fighter_filters: FighterFilter
    ) -> Union[list[ExtendedFighterSchema], None]:
        filters = self.build_filters_from_model(fighter_filters)
        result = await self.db.execute(self.extended_fighter_stmt.where(*filters))
        fighters = result.scalars().all()
        if fighters is None:
            return None
        return [ExtendedFighterSchema.model_validate(fighter) for fighter in fighters]

    #######################################POST METHODS#############################################

    async def post_single_base_data_to_database(
        self, data: FighterFilter
    ) -> CursorResult:
        stmt = insert(Fighters).values(**data)
        result = await self.db.execute(stmt)
        logger.critical(f"post_single_base_data_to_database {result}")
        await self.db.commit()
        return result


    async def post_single_extended_data_to_database(
        self, data: ExtendedFighterFilter
    ) -> CursorResult:
        stmt = insert(Fighters).values(**data)
        result = await self.db.execute(stmt)
        logger.critical(f"post_single_base_data_to_database {result}")
        await self.db.commit()
        return result

    # async def post_extended_base_data_to_database(
    #     self, data: Union[FighterFilter, ExtendedFighterFilter], extended: bool = False
    # ) -> None:
    #     data_dict = data.dict(exclude_none=True)
    #     fighter_data = []#todo dokonczyc
    #
    #     for field, value in data_dict.items():
    #         if hasattr(Fighters, field):  #czy to sprawdzi rowniez w relacjach tego modelu?
    #             column = getattr(Fighters, field)
    #             fighter_data.append(column == value)
    #         else:
    #             raise ValueError(f"Column '{field}' does not exist in Fighters model")
    #
    #
    # async def post_multiple_data_to_database(
    #         self, data: List[Union[FighterFilter, ExtendedFighterFilter]], extended: bool = False
    # ) -> None:
    #     fighters = [] #todo dokonczyc
    #     for fighter_data in data:
    #         data_dict = data.dict(exclude_none=True)
    #         for field, value in data_dict.items():
    #             if hasattr(Fighters, field):
    #                 column = getattr(Fighters, field)
    #                 fighters.append(column == value)
    #             else:
    #                 raise ValueError(f"Column '{field}' does not exist in Fighters model")

    # records = await self._get_all_fighter_statistics_with_dict(filters)
    # fighters = records.scalars().all()
    # if fighters is None:
    #     return None
    # return [ExtendedFighter.model_validate(fighter) for fighter in fighters]

    #####################################OTHER METHODS#############################################
    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info("Truncating:", table)
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
