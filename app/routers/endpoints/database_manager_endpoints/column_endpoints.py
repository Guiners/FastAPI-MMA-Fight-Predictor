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
):
    return await DataBaseManager(db).add_column(
        table_name, column_name, column_type, column_size
    )


@column_router.delete("/", status_code=status.HTTP_202_ACCEPTED)
async def remove_column(
    table_name: str,
    column_name: str,
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).remove_column(table_name, column_name)


@column_router.put("/rename", status_code=status.HTTP_202_ACCEPTED)
async def rename_column(
    table_name: str,
    old_column_name: str,
    new_column_name: str,
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).rename_column(
        table_name, old_column_name, new_column_name
    )


@column_router.put("/change_type", status_code=status.HTTP_202_ACCEPTED)
async def change_column_type(
    table_name: str,
    column_name: str,
    new_datatype: str,
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).change_column_type(
        table_name, column_name, new_datatype
    )
