from datetime import datetime

from fastapi.templating import Jinja2Templates


def short_date(value):
    return value.strftime("%d.%m.%Y")


templates = Jinja2Templates(directory="app/templates")

templates.env.globals.update(
    {
        "app_name": "MMA Fight Predictor",
        "year": lambda: datetime.now().year,
    }
)

templates.env.filters["short_date"] = short_date
# TODO DODAC STATIC, DODAC OBSLUGE EXTENDED FIGHTER, LISTY DLA BASE I EXTENDED, DO OGARNIECIA STATYSTYK Z TEGO GROUP BY HAVING
