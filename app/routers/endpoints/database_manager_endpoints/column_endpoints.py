from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.database_manager import DataBaseManager

column_router = APIRouter(prefix="/column")


@column_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_column(
    table_name: str,
    column_name: str,
    column_type: str = "VARCHAR",
    column_size: int = 50,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Add a new column to a database table.

    Args:
        table_name (str): Name of the table to modify.
        column_name (str): Name of the new column to add.
        column_type (str, optional): SQL data type for the column. Defaults to "VARCHAR".
        column_size (int, optional): Size of the column (if applicable). Defaults to 50.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the operation result.
    """
    return await DataBaseManager(db).add_column(
        table_name, column_name, column_type, column_size
    )


@column_router.delete("/", status_code=status.HTTP_202_ACCEPTED)
async def remove_column(
    table_name: str,
    column_name: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Remove an existing column from a database table.

    Args:
        table_name (str): Name of the table to modify.
        column_name (str): Name of the column to remove.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the operation result.
    """
    return await DataBaseManager(db).remove_column(table_name, column_name)


@column_router.put("/rename", status_code=status.HTTP_202_ACCEPTED)
async def rename_column(
    table_name: str,
    old_column_name: str,
    new_column_name: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Rename a column in a database table.

    Args:
        table_name (str): Name of the table to modify.
        old_column_name (str): Current name of the column.
        new_column_name (str): New name for the column.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the operation result.
    """
    return await DataBaseManager(db).rename_column(
        table_name, old_column_name, new_column_name
    )


@column_router.put("/change_type", status_code=status.HTTP_202_ACCEPTED)
async def change_column_type(
    table_name: str,
    column_name: str,
    new_datatype: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Change the data type of a column in a database table.

    Args:
        table_name (str): Name of the table to modify.
        column_name (str): Name of the column to alter.
        new_datatype (str): New SQL data type for the column.
        db (AsyncSession): Active SQLAlchemy database session (dependency-injected).

    Returns:
        dict: Information about the operation result.
    """
    return await DataBaseManager(db).change_column_type(
        table_name, column_name, new_datatype
    )
