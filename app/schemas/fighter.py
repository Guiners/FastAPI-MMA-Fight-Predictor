from datetime import date

from pydantic import BaseModel


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
    name: str
    nickname: str
    surname: str
    country: str
    weight_class: str
    wins: int
    loss: int
    draw: int
    current_streak: int
    last_fight_date: date
    last_updated: date
