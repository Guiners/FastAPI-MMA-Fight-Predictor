from datetime import date

from pydantic import BaseModel

from app.tools.utils import create_filter_schema


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

    fighter_id: int | None = None
    weight: float | None = None
    height: float | None = None
    reach: float | None = None
    age: int | None = None
    last_updated: date

    model_config = {"from_attributes": True}


BaseStatsFilter = create_filter_schema(BaseStats)
