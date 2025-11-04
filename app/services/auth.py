import os
import typing
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import PREFIX
from app.db.models.users import Users
from app.schemas.users import User as UserSchema
from app.schemas.users import UserFilter
from app.tools import logger
from app.tools.exceptions.custom_api_exceptions import (
    NotFoundException,
    UnauthorizedException,
)

SECRET_KEY: str | None = os.getenv("SECRET_KEY")
ALGORITHM: str | None = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/auth/token")


class AuthService:
    """
    Service for user authentication and authorization.
    Handles user creation, login, and JWT-based token management.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the authentication service.

        Args:
            db (AsyncSession): SQLAlchemy asynchronous database session.
        """
        self.db = db

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_bearer),
    ) -> dict[str, typing.Any]:
        """
        Decode a JWT token and extract user data.

        Args:
            token (str): The JWT access token (automatically provided by OAuth2 dependency).

        Returns:
            dict[str, Any]: A dictionary containing user email and ID.

        Raises:
            UnauthorizedException: If the token is invalid or expired.
            NotFoundException: If the token payload is missing essential data.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str | None = payload.get("sub")
            user_id: int | None = payload.get("id")

            if user_id is None or email is None:
                raise NotFoundException

            return {"email": email, "id": user_id}

        except Exception as e:
            logger.error("JWT decoding error")
            raise UnauthorizedException from e

    async def create_user(self, user_filter: UserFilter) -> bool:
        """
        Create a new user record in the database.

        Args:
            user_filter (UserFilter): User registration data (email, password).

        Returns:
            bool: True if the user was successfully created, False otherwise.
        """
        try:
            user = Users(
                email=user_filter.email,
                hashed_password=bcrypt_context.hash(user_filter.password[:30]),
            )
            self.db.add(user)
            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"Error while creating user: {e}")
            return False

    async def get_all_users(self) -> typing.List[UserSchema]:
        """
        Retrieve all users from the database.

        Returns:
            list[UserSchema]: List of validated user schema objects.
        """
        records = await self.db.execute(select(Users))
        logger.info(f"Returning contents of {Users.__name__}")
        return [UserSchema.model_validate(row) for row in records.scalars().all()]

    async def authenticate_user(self, user_filter: UserFilter) -> Users:
        """
        Verify user credentials during login.

        Args:
            user_filter (UserFilter): The user's login credentials.

        Returns:
            Users: The authenticated user ORM object.

        Raises:
            UnauthorizedException: If credentials are invalid.
        """
        records = await self.db.execute(
            select(Users).filter(Users.email == user_filter.email)
        )
        user = records.scalar_one_or_none()
        if not user:
            raise UnauthorizedException

        try:
            if not bcrypt_context.verify(user_filter.password, user.hashed_password):
                raise UnauthorizedException
        except Exception as e:
            logger.error("Password verification error")
            raise UnauthorizedException from e

        return user

    @staticmethod
    def create_access_token(
        user: UserSchema,
        expires_delta: timedelta = timedelta(minutes=30),
    ) -> str:
        """
        Generate a new JWT access token for an authenticated user.

        Args:
            user (UserSchema): The authenticated user's data.
            expires_delta (timedelta, optional): Token expiration time. Defaults to 30 minutes.

        Returns:
            str: Encoded JWT access token.
        """
        encode = {
            "sub": user.email,
            "id": user.user_id,
            "exp": datetime.now() + expires_delta,
        }
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
