from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.database_manager import DataBaseManager

table_router = APIRouter(prefix="/table")


@table_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_table(
    table_name: str,
    column_type_dict: dict = Body(...),
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).create_table(table_name, column_type_dict)


@table_router.delete("/", status_code=status.HTTP_202_ACCEPTED)
async def delete_table(
    table_name: str,
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).delete_table(table_name)


@table_router.delete("/truncate", status_code=status.HTTP_202_ACCEPTED)
async def truncate_table(
    table_name: str,
    db: AsyncSession = Depends(get_db),
):
    return await DataBaseManager(db).truncate_table(table_name)
