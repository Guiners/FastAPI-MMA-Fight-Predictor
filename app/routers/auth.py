import os
from typing import List
from warnings import deprecated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.auth_database_manager import AuthDataBaseManager
from app.db.models.users import Users
from app.schemas.token import Token as TokenSchema
from app.schemas.users import User as UserSchema
from app.schemas.users import UserFilter
from app.tools.tools import handle_empty_response

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_filter: UserFilter = Depends(), db: AsyncSession = Depends(get_db)
):
    return await AuthDataBaseManager(db).create_user(user_filter)


@auth_router.get("")
# @handle_empty_response
async def get_all_users(
    db: AsyncSession = Depends(get_db),
):
    return await AuthDataBaseManager(db).get_all_users()
