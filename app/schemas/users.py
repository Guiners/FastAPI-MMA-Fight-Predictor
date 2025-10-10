from typing import Optional

from pydantic import BaseModel, ConfigDict, constr


class UserFilter(BaseModel):
    email: str
    password: constr(min_length=3, max_length=30)


class User(BaseModel):
    user_id: Optional[int] = None
    email: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
