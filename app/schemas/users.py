from pydantic import BaseModel, ConfigDict, constr


class UserFilter(BaseModel):
    """
    Schema for filtering or creating a user.

    Attributes:
        email (str): The user's email address.
        password (constr): The user's password (between 3 and 30 characters).
    """

    email: str
    password: constr(min_length=3, max_length=30)


class User(BaseModel):
    """
    Represents a user entity in the system.

    Attributes:
        user_id (int | None): The unique identifier of the user.
        email (str): The user's email address.
        hashed_password (str): The hashed password stored in the database.
    """

    user_id: int | None = None
    email: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
