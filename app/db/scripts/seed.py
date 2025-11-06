import asyncio
import json
import typing
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import example_data_paths
from app.db.database import get_db
from app.services.fighters.fighter_utils import FighterUtils
from app.tools.exceptions.custom_api_exceptions import InternalServerError
from app.tools.logger import logger

LAST_FIGHT_DATE = "last_fight_date"
LAST_UPDATED = "last_updated"


class TableFiller:
    """Utility class for populating database tables with initial data from JSON files."""

    @staticmethod
    def _fill_table_from_json(
        db: AsyncSession, table: typing.Type, json_path: str
    ) -> None:
        """Populate a single database table with data from a JSON file.

        Args:
            db (AsyncSession): Active SQLAlchemy session.
            table (typing.Type): ORM model class representing the target table.
            json_path (str): Path to the JSON file containing records.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.
        """
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        with path.open(encoding="utf-8") as file:
            logger.info(f"Updating table: {table.__name__}")
            for data in json.load(file):
                TableFiller.fix_data_column(data, LAST_FIGHT_DATE)
                TableFiller.fix_data_column(data, LAST_UPDATED)
                db.add(table(**data))

    @staticmethod
    async def fill_database_with_data(
        db: AsyncSession, data_dict: typing.List[typing.Tuple[typing.Type, str]]
    ) -> None:
        """Populate multiple database tables defined in the provided data mapping.

        Args:
            db (AsyncSession): Active SQLAlchemy session.
            data_dict (List[Tuple[Type, str]]): A list of tuples where each
                contains:
                    - ORM model class (table)
                    - Path to the JSON file with data.

        Raises:
            InternalServerError: If an error occurs during database seeding.
        """
        try:
            for table, path in data_dict:
                TableFiller._fill_table_from_json(db, table, path)
            await db.commit()
            logger.info("Database seeded successfully.")
        except Exception as e:
            logger.error("An error occurred during database seeding.")
            await db.rollback()
            raise InternalServerError from e

    @staticmethod
    def fix_data_column(
        data: typing.Dict[str, typing.Any], column_name: str, _format: str = "%Y-%m-%d"
    ) -> None:
        """Convert a string date column in a dictionary to a datetime.date object.

        Args:
            data (Dict[str, Any]): A dictionary containing record data.
            column_name (str): The key name for the date field.
            _format (str, optional): Date format to parse. Defaults to "%Y-%m-%d".
        """
        if column_name in data and isinstance(data[column_name], str):
            data[column_name] = datetime.strptime(data[column_name], _format).date()


async def main() -> None:
    """Clear all tables and populate them with initial data from JSON files."""
    async for mma_db in get_db():
        await FighterUtils(mma_db, False).clear_all_tables()
        await TableFiller.fill_database_with_data(mma_db, example_data_paths)


if __name__ == "__main__":
    asyncio.run(main())
