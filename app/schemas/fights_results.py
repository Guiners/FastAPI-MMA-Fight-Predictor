from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.tools.tools import create_filter_schema


class FightsResults(BaseModel):
    """Aggregated fight results for a fighter.
    Attributes:
        fighter_id (int): Unique ID of the fighter.
        win_by_ko_tko (int): Number of wins by knockout/technical knockout.
        loss_by_ko_tko (int): Number of losses by knockout/technical knockout.
        win_by_sub (int): Number of wins by submission.
        loss_by_sub (int): Number of losses by submission.
        win_by_dec (int): Number of wins by decision.
        loss_by_dec (int): Number of losses by decision.
        non_contest (int): Number of fights declared as no contest.
        last_updated (date): Date when the record was last updated.
    """

    fighter_id: Optional[int]
    win_by_ko_tko: Optional[int]
    loss_by_ko_tko: Optional[int]
    win_by_sub: Optional[int]
    loss_by_sub: Optional[int]
    win_by_dec: Optional[int]
    loss_by_dec: Optional[int]
    non_contest: Optional[int]
    last_updated: date

    class Config:
        from_attributes = True

FightsResultsFilter = create_filter_schema(FightsResults)
