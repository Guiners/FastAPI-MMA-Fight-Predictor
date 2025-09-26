import json

from app.db.database import get_db
from sqlalchemy.orm import Session
from pathlib import Path
from app.db.constants import example_data_paths

class TableFiller:
    """Utility class for populating database tables with initial data from JSON files."""

    @staticmethod
    def _fill_table_from_json(database: Session, table, json_path: str) -> None:
        """Populate a single database table from a JSON file.

        Args:
            database (Session): Active SQLAlchemy session.
            table (Type): ORM model class representing the target table.
            json_path (str): Path to the JSON file containing records.
        """
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        with path.open(encoding="utf-8") as file:
            for data in json.load(file):
                database.add(table(**data))

    @staticmethod
    def fill_database_with_data(database: Session, data_dict: dict) -> None:
        """Populate all database tables defined in `example_data_paths`.
        This method iterates through the `example_data_paths` list and
        inserts the data into each corresponding table.

        Args:
            database (Session): Active SQLAlchemy session.
            data_dict (Sequence[Tuple[Type, str]]): A sequence of tuples
                where each tuple contains:
                    - ORM model class (table)
                    - Path to the JSON file with data.
        """
        for table, path in data_dict.items():
            try:
                TableFiller._fill_table_from_json(database, table, path)
                database.commit()
            except Exception as e:
                print('Exception: ', e)
                pass

if __name__ == "__main__":
    mma_db = next(get_db())
    TableFiller.fill_database_with_data(mma_db, example_data_paths)
