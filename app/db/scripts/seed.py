import asyncio
import json
from datetime import datetime
from sqlalchemy import select, text

from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from app.db.models.base import Base
from app.db.constants import example_data_paths

LAST_FIGHT_DATE = "last_fight_date"
LAST_UPDATED = "last_updated"

class TableFiller:
    """Utility class for populating database tables with initial data from JSON files."""

    @staticmethod
    async def clear_tables(database: AsyncSession):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            print("Truncating:", table)
            await database.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))
        await database.commit()

    @staticmethod
    def _fix_data_column(data, column_name: str, _format: str = "%Y-%m-%d"):
        if column_name in data and isinstance(data[column_name], str):
            data[column_name] = datetime.strptime(data[column_name], _format).date()


    @staticmethod
    def _fill_table_from_json(db: AsyncSession, table, json_path: str) -> None:
        """Populate a single database table from a JSON file.

        Args:
            db (AsyncSession): Active SQLAlchemy session.
            table (Type): ORM model class representing the target table.
            json_path (str): Path to the JSON file containing records.
        """
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        with path.open(encoding="utf-8") as file:
            print("Updating table:", table)
            for data in json.load(file):
                TableFiller._fix_data_column(data, LAST_FIGHT_DATE)
                TableFiller._fix_data_column(data, LAST_UPDATED)
                db.add(table(**data))

    @staticmethod
    async def fill_database_with_data(db: AsyncSession, data_dict: dict) -> None:
        """Populate all database tables defined in `example_data_paths`.
        This method iterates through the `example_data_paths` list and
        inserts the data into each corresponding table.

        Args:
            db (AsyncSession): Active SQLAlchemy session.
            data_dict (Sequence[Tuple[Type, str]]): A sequence of tuples
                where each tuple contains:
                    - ORM model class (table)
                    - Path to the JSON file with data.
        """
        try:
            for table, path in data_dict.items():
                TableFiller._fill_table_from_json(db, table, path)
            await db.commit()
            print("Database seeded successfully. Verifying data...")
            for table in data_dict.keys():
                result = await db.execute(select(table))
                rows = result.scalars().all()
                print(f"--- Contents of {table.__name__} ---")
                for row in rows:
                    print(vars(row))

        except Exception as e:
            print(f'An error occurred during database seeding: {e}')
            await db.rollback()
            raise


async def main():
    async for mma_db in get_db():
        await TableFiller.clear_tables(mma_db)
        await TableFiller.fill_database_with_data(mma_db, example_data_paths)

if __name__ == "__main__":
    asyncio.run(main())
