from datetime import date

from pydantic import BaseModel

from app.tools.utils import create_filter_schema


class Fighter(BaseModel):
    """Main information about a fighter.
    Attributes:
        fighter_id (int): Unique ID of the fighter.
        name (str): First name of the fighter.
        nickname (str): Fighter's nickname.
        surname (str): Last name of the fighter.
        country (str): Country of origin.
        weight_class (str): Fighter's weight division.
        wins (int): Total number of wins.
        loss (int): Total number of losses.
        draw (int): Total number of draws.
        current_streak (int): Current winning/losing streak.
        last_fight_date (date): Date of the fighter's last fight.
        last_updated (date): Date when the record was last updated.
    """

    fighter_id: int
    name: str | None
    nickname: str | None
    surname: str | None
    country: str | None
    weight_class: str | None
    wins: int | None
    loss: int | None
    draw: int | None
    current_streak: int | None
    last_fight_date: date | None
    last_updated: date

    model_config = {"from_attributes": True}


FighterFilter = create_filter_schema(Fighter)
