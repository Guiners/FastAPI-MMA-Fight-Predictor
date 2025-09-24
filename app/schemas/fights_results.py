from datetime import date

from pydantic import BaseModel


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

    fighter_id: int
    win_by_ko_tko: int
    loss_by_ko_tko: int
    win_by_sub: int
    loss_by_sub: int
    win_by_dec: int
    loss_by_dec: int
    non_contest: int
    last_updated: date

    class Config:
        orm_mode = True
