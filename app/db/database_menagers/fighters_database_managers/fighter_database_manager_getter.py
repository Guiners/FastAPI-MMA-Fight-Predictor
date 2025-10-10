from app.db.database_menagers.fighters_database_managers.fighter_database_manager_base import \
    DatabaseManagerBase
from app.schemas.fighter import FighterFilter
from app.tools.logger import logger


class DatabaseManagerGetter(DatabaseManagerBase):

    # todo typing
    async def get_all_fighters_records(self):
        records = await self.db.execute(self.stmt)
        logger.info(f"Returning contents of {self.fighter_schema.__name__}")
        return [
            self.fighter_schema.model_validate(row) for row in records.scalars().all()
        ]

    # todo typing
    async def get_fighter_by_id(self, fighter_id: int):
        return await self._get_records_by_single_value("fighter_id", fighter_id)

    # todo typing
    async def get_fighters_by_country(self, country: str):
        return await self._get_records_by_single_value("country", country)

    # todo typing
    async def search_extended_fighter(self, fighter_filters: FighterFilter):
        return await self._get_records_with_where_stmt(
            self.build_where_stmt(fighter_filters)
        )
