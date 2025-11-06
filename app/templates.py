import typing
from datetime import datetime

from fastapi.templating import Jinja2Templates


def short_date(value: datetime) -> str:
    """Format a datetime object to a short date string (DD.MM.YYYY).

    Args:
        value (datetime): The datetime object to format.

    Returns:
        str: The formatted date string in the format "DD.MM.YYYY".
    """
    return value.strftime("%d.%m.%Y")


def clean_str(value: typing.Any) -> typing.Any | str:
    """Replace underscores with spaces in a string.

    Args:
        value (Any): The value to clean. If it's a string, underscores are replaced with spaces.

    Returns:
        Any | str: The cleaned string, or the original value if not a string.
    """
    if isinstance(value, str):
        return value.replace("_", " ")
    return value


templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

templates.env.globals.update(
    {
        "app_name": "MMA Fight Predictor",
        "year": lambda: datetime.now().year,
    }
)

templates.env.filters["short_date"] = short_date
templates.env.filters["clean_str"] = clean_str
