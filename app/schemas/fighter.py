from datetime import date
from typing import Optional

from pydantic import BaseModel, create_model

from app.tools.tools import create_filter_schema


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
    name: Optional[str]
    nickname: Optional[str]
    surname: Optional[str]
    country: Optional[str]
    weight_class: Optional[str]
    wins: Optional[int]
    loss: Optional[int]
    draw: Optional[int]
    current_streak: Optional[int]
    last_fight_date: Optional[date]
    last_updated: date

    class Config:
        from_attributes = True


FighterFilter = create_filter_schema(Fighter)
