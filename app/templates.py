from datetime import datetime

from fastapi.templating import Jinja2Templates


def short_date(value):
    return value.strftime("%d.%m.%Y")

def clean_str(value):
    if type(value) is str:
        return value.replace("_", " ")
    return value



templates = Jinja2Templates(directory="app/templates")

templates.env.globals.update(
    {
        "app_name": "MMA Fight Predictor",
        "year": lambda: datetime.now().year,
    }
)

templates.env.filters["short_date"] = short_date
templates.env.filters["clean_str"] = clean_str
