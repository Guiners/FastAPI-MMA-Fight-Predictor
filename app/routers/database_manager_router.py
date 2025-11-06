from fastapi import APIRouter

from app.routers.endpoints.database_manager_endpoints.column_endpoints import (
    column_router,
)
from app.routers.endpoints.database_manager_endpoints.table_endpoints import (
    table_router,
)

database_manager_router = APIRouter(prefix="/db")

database_manager_router.include_router(column_router)
database_manager_router.include_router(table_router)
