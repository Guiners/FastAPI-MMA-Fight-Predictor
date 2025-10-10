import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.users import Users
from app.schemas.token import Token as TokenSchema
from app.schemas.users import User as UserSchema
from app.schemas.users import UserFilter
from app.tools import logger

secret_key = "83489hfyy46457943095789cf4879f3890"
algorith = "HS256"

SECRET_KEY = os.getenv("SECRET_KEY", secret_key)
ALGORITHM = os.getenv("ALGORITHM", algorith)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthDataBaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_filter: UserFilter):
        user = Users(
            email=user_filter.email,
            hashed_password=bcrypt_context.hash(user_filter.password[:30]),
        )

        self.db.add(user)
        await self.db.commit()
        return True

    async def get_all_users(self):
        records = await self.db.execute(select(Users))
        logger.info(f"Returning contents of {Users.__name__}")
        return [UserSchema.model_validate(row) for row in records.scalars().all()]
