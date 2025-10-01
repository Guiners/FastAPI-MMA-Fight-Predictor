from datetime import date

from pydantic import BaseModel


class BaseStats(BaseModel):
    """Basic physical statistics for a fighter.
    Attributes:
        fighter_id (int): Unique ID of the fighter.
        weight (float): Weight of the fighter in kilograms.
        height (float): Height of the fighter in centimeters.
        reach (float): Reach of the fighter in centimeters.
        age (int): Age of the fighter in years.
        last_updated (date): Date when the record was last updated.
    """

    fighter_id: int
    weight: float
    height: float
    reach: float
    age: int
    last_updated: date

    class Config:
        from_attributes = True
