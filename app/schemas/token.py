from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    Represents an authentication token returned after successful user login.

    Attributes:
        access_token (str): The JWT access token used for authentication.
        token_type (str): The type of the token, usually set to "bearer".
    """

    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
