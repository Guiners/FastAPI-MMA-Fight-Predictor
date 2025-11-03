from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from app.constants import PREFIX, version
from app.middleware.middlewares import log_requests
from app.routers.auth_router import auth_router
from app.routers.base_fighter_router import base_fighter_router
from app.routers.database_manager_router import database_manager_router
from app.routers.extended_fighter_router import extended_fighter_router
from app.services.auth import AuthService
from app.tools.exception_handlers import register_exception_handlers
from app.tools.exceptions.custom_api_exceptions import UnauthorizedException

app = FastAPI(version=version)

app.middleware("http")(log_requests)
app.include_router(base_fighter_router, prefix=PREFIX)
app.include_router(extended_fighter_router, prefix=PREFIX)
app.include_router(auth_router, prefix=PREFIX)
app.include_router(database_manager_router, prefix=PREFIX)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

register_exception_handlers(app)


@app.get("/", response_model=None)
async def user(
    user: dict = Depends(AuthService.get_current_user),
):
    if user is None:
        raise UnauthorizedException

    return {"User": user}
