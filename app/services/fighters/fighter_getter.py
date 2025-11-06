import typing

from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_utils import FighterUtils
from app.tools.logger import logger


class FighterGetter(FighterUtils):
    """
    Service class for retrieving fighter records from the database.

    Inherits from:
        FighterUtils: Provides shared query-building and data access utilities.
    """

    async def get_all_fighters_records(self) -> typing.List[typing.Any]:
        """
        Retrieve all fighter records from the database.

        Returns:
            list[Any]: List of all fighter records validated against the schema.
        """
        records = await self.db.execute(self.stmt)
        logger.info(f"Returning contents of {self.fighter_schema.__name__}")
        return [
            self.fighter_schema.model_validate(row) for row in records.scalars().all()
        ]

    async def get_fighter_by_id(self, fighter_id: int) -> typing.Any:
        """
        Retrieve a fighter by their unique ID.

        Args:
            fighter_id (int): The unique identifier of the fighter.

        Returns:
            Any: The fighter record matching the provided ID.
        """
        return await self._get_records_by_single_value("fighter_id", fighter_id)

    async def get_fighters_by_country(self, country: str) -> typing.List[typing.Any]:
        """
        Retrieve all fighters belonging to a specific country.

        Args:
            country (str): Name of the country.

        Returns:
            list[Any]: List of fighters from the given country.
        """
        return await self._get_records_by_single_value("country", country)

    async def search_extended_fighter(
        self, fighter_filters: FighterFilter
    ) -> typing.List[typing.Any]:
        """
        Search for extended fighters using dynamic filter parameters.

        Args:
            fighter_filters (FighterFilter): Filter object defining search criteria.

        Returns:
            list[Any]: List of fighters matching the given filters.
        """
        return await self._get_records_with_where_stmt(
            self.build_where_stmt(fighter_filters)
        )
