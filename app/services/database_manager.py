from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.logger import logger


class DataBaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _execute_ddl(
        self,
        stmt: str,
    ):
        await self.db.execute(text(stmt))
        await self.db.commit()
        logger.info("DDL Executed")

    async def add_column(
        self,
        table_name: str,
        column_name: str,
        column_type: str,
        column_size: int,
    ):
        column_def = (
            f"{column_type}({column_size})"
            if column_type.upper() in ["VARCHAR", "CHAR"]
            else column_type
        )
        await self._execute_ddl(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}"
        )
        logger.info(f"Column {column_name} added to {table_name}")

    #     await self.column_exists(table_name, column_name)
    #
    # async def column_exists(self, table_name: str, column_name: str):
    #     query = f"""
    #         SELECT 1
    #         FROM information_schema.columns
    #         WHERE table_name = '{table_name}'
    #         AND column_name = '{column_name}'
    #     """
    #     result = await self._execute_ddl(query)
    #     logger.critical(result)
    #     return result.scalar()

    async def remove_column(self, table_name: str, column_name: str):
        await self._execute_ddl(
            f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {column_name}"
        )
        logger.info(f"Column {column_name} removed from {table_name}")

    async def rename_column(
        self, table_name: str, old_column_name: str, new_column_name: str
    ):
        await self._execute_ddl(
            f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}"
        )
        logger.info(f"Column {old_column_name} renamed to {new_column_name}")

    async def change_column_type(
        self, table_name: str, column_name: str, new_datatype: str
    ):
        await self._execute_ddl(
            f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_datatype} USING {column_name}::{new_datatype}"
        )
        logger.info(f"Column {column_name} changed type to {new_datatype}")

    async def create_table(self, table_name: str, column_type_dict: dict):
        columns = ", ".join(f"{col} {_type}" for col, _type in column_type_dict.items())

        await self._execute_ddl(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        logger.info(f"Table {table_name} created successfully")

    async def delete_table(self, table_name: str):
        await self._execute_ddl(f"DROP TABLE {table_name}")
        logger.info(f"Table {table_name} deleted successfully")

    async def truncate_table(self, table_name: str):
        await self._execute_ddl(f"TRUNCATE TABLE {table_name}")
        logger.info(f"Table {table_name} truncated successfully")
