import typing

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.users import UserFilter
from app.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_filter: UserFilter = Depends(),
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    """
    Register a new user.

    Args:
        user_filter (UserFilter): Data for the new user (email, password, etc.).
        db (AsyncSession): Asynchronous database session.

    Returns:
        typing.Dict[str, typing.Any]: Information about the created user.
    """
    return await AuthService(db).create_user(user_filter)


@auth_router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
) -> typing.List[typing.Dict[str, typing.Any]]:
    """
    Retrieve a list of all users.

    Args:
        db (AsyncSession): Asynchronous database session.

    Returns:
        typing.List[typing.Dict[str, typing.Any]]: List of users.
    """
    return await AuthService(db).get_all_users()


@auth_router.post("/token", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> typing.Dict[str, str]:
    """
    Authenticate a user and generate a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials (username, password).
        db (AsyncSession): Asynchronous database session.

    Returns:
        typing.Dict[str, str]: Dictionary containing the JWT access token and token type.
    """
    auth_manager = AuthService(db)
    user = await auth_manager.authenticate_user(
        UserFilter(email=form_data.username, password=form_data.password)
    )
    return {
        "access_token": auth_manager.create_access_token(user),
        "token_type": "bearer",
    }
