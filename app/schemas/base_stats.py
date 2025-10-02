from datetime import date
from typing import Optional

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

    fighter_id: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    reach: Optional[float] = None
    age: Optional[int] = None
    last_updated: date

    class Config:
        from_attributes = True
