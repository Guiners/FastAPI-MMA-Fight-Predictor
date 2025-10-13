from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.auth import AuthService
from app.schemas.users import UserFilter

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_filter: UserFilter = Depends(), db: AsyncSession = Depends(get_db)
):
    return await AuthService(db).create_user(user_filter)


@auth_router.get("")
# @handle_empty_response
async def get_all_users(
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).get_all_users()


@auth_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    AuthManager = AuthService(db)
    user = await AuthManager.authenticate_user(
        UserFilter(email=form_data.username, password=form_data.password)
    )
    return {
        "access_token": AuthManager.create_access_token(user),
        "token_type": "bearer",
    }
