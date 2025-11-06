from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.logger import logger


class DataBaseManager:
    """
    Utility class for performing dynamic DDL (Data Definition Language)
    operations on a PostgreSQL database using SQLAlchemy AsyncSession.

    Supports adding, removing, renaming, and altering table columns,
    as well as creating, deleting, and truncating entire tables.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the database manager.

        Args:
            db (AsyncSession): The SQLAlchemy asynchronous session.
        """
        self.db = db

    async def _execute_ddl(self, stmt: str) -> None:
        """
        Execute a raw SQL DDL statement.

        Args:
            stmt (str): The SQL statement to execute.

        Returns:
            None
        """
        await self.db.execute(text(stmt))
        await self.db.commit()
        logger.info("DDL executed successfully")

    async def add_column(
        self,
        table_name: str,
        column_name: str,
        column_type: str,
        column_size: int | None = None,
    ) -> None:
        """
        Add a new column to an existing table.

        Args:
            table_name (str): The name of the target table.
            column_name (str): The name of the column to add.
            column_type (str): The SQL type of the column (e.g. VARCHAR, INT).
            column_size (int | None, optional): The size of the column (used for VARCHAR/CHAR).

        Returns:
            None
        """
        column_def = (
            f"{column_type}({column_size})"
            if column_type.upper() in {"VARCHAR", "CHAR"} and column_size
            else column_type
        )
        await self._execute_ddl(
            f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_def};'
        )
        logger.info(f"Column '{column_name}' added to table '{table_name}'")

    async def remove_column(self, table_name: str, column_name: str) -> None:
        """
        Remove a column from a table if it exists.

        Args:
            table_name (str): The name of the target table.
            column_name (str): The column to remove.

        Returns:
            None
        """
        await self._execute_ddl(
            f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{column_name}";'
        )
        logger.info(f"Column '{column_name}' removed from '{table_name}'")

    async def rename_column(
        self, table_name: str, old_column_name: str, new_column_name: str
    ) -> None:
        """
        Rename a column in a table.

        Args:
            table_name (str): The name of the table.
            old_column_name (str): The current name of the column.
            new_column_name (str): The new name to assign.

        Returns:
            None
        """
        await self._execute_ddl(
            f'ALTER TABLE "{table_name}" RENAME COLUMN "{old_column_name}" TO "{new_column_name}";'
        )
        logger.info(
            f"Column '{old_column_name}' renamed to '{new_column_name}' in '{table_name}'"
        )

    async def change_column_type(
        self, table_name: str, column_name: str, new_datatype: str
    ) -> None:
        """
        Change the data type of a column.

        Args:
            table_name (str): The name of the table.
            column_name (str): The name of the column to modify.
            new_datatype (str): The new SQL data type.

        Returns:
            None
        """
        await self._execute_ddl(
            f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" '
            f'TYPE {new_datatype} USING "{column_name}"::{new_datatype};'
        )
        logger.info(f"Column '{column_name}' changed to type '{new_datatype}'")

    async def create_table(
        self, table_name: str, column_type_dict: dict[str, str]
    ) -> None:
        """
        Create a new table with the specified columns.

        Args:
            table_name (str): The name of the table to create.
            column_type_dict (dict[str, str]): A mapping of column names to SQL types.

        Returns:
            None
        """
        columns = ", ".join(
            f'"{col}" {_type}' for col, _type in column_type_dict.items()
        )
        await self._execute_ddl(
            f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        )
        logger.info(f"Table '{table_name}' created successfully")

    async def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.

        Args:
            table_name (str): The name of the table to delete.

        Returns:
            None
        """
        await self._execute_ddl(f'DROP TABLE IF EXISTS "{table_name}";')
        logger.info(f"Table '{table_name}' deleted successfully")

    async def truncate_table(self, table_name: str) -> None:
        """
        Truncate all data from a table (keep structure).

        Args:
            table_name (str): The name of the table to truncate.

        Returns:
            None
        """
        await self._execute_ddl(f'TRUNCATE TABLE "{table_name}";')
        logger.info(f"Table '{table_name}' truncated successfully")
