from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.database_manager import DataBaseManager

table_router = APIRouter(prefix="/table")


@table_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_table(
    table_name: str,
    column_type_dict: dict = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Create a new table in the database.

    Args:
        table_name (str): Name of the table to create.
        column_type_dict (dict): Dictionary mapping column names to their SQL types.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the created table.
    """
    return await DataBaseManager(db).create_table(table_name, column_type_dict)


@table_router.delete("/", status_code=status.HTTP_202_ACCEPTED)
async def delete_table(
    table_name: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete an existing table from the database.

    Args:
        table_name (str): Name of the table to delete.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the deletion result.
    """
    return await DataBaseManager(db).delete_table(table_name)


@table_router.delete("/truncate", status_code=status.HTTP_202_ACCEPTED)
async def truncate_table(
    table_name: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Truncate (empty) a database table, removing all records but keeping its structure.

    Args:
        table_name (str): Name of the table to truncate.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the truncation result.
    """
    return await DataBaseManager(db).truncate_table(table_name)
