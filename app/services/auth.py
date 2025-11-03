import os
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select, text
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

# secret_key = "83489hfyy46457943095789cf4879f3890"
# algorith = "HS256"
# #todo put in .env
# SECRET_KEY = os.getenv("SECRET_KEY", secret_key)
# ALGORITHM = os.getenv("ALGORITHM", algorith)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/auth/token")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    async def get_current_user(token=Depends(oauth2_bearer)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("id")

            if user_id is None or email is None:
                raise NotFoundException

            return {"email": email, "id": user_id}

        except Exception as e:
            logger.error(f"JTW ERROR")
            raise UnauthorizedException from e

    async def create_user(self, user_filter: UserFilter):
        try:
            user = Users(
                email=user_filter.email,
                hashed_password=bcrypt_context.hash(user_filter.password[:30]),
            )

            self.db.add(user)
            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"Creating user error: {e}")
            return False

    async def get_all_users(self):
        records = await self.db.execute(select(Users))
        logger.info(f"Returning contents of {Users.__name__}")
        return [UserSchema.model_validate(row) for row in records.scalars().all()]

    async def authenticate_user(self, user_filter: UserFilter):
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
            logger.error(f"Logging error")
            raise UnauthorizedException from e

        return user

    @staticmethod
    def create_access_token(
        user: UserSchema, expires_delta: timedelta = timedelta(minutes=30)
    ):
        encode = {
            "sub": user.email,
            "id": user.user_id,
            "exp": datetime.now() + expires_delta,
        }
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
