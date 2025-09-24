from datetime import date

from pydantic import BaseModel


class ExtendedStats(BaseModel):
    """Extended statistical information for a fighter.
    Attributes:
        fighter_id (int): Unique ID of the fighter.
        stance (str): Fighter's stance (e.g., Orthodox, Southpaw).
        slpm (float): Significant Strikes Landed per Minute.
        str_acc (float): Significant Striking Accuracy (% of strikes landed).
        sapm (float): Significant Strikes Absorbed per Minute.
        str_def (float): Significant Strike Defence (% of opponent strikes that did not land).
        td_avg (float): Average Takedowns Landed per 15 minutes.
        td_acc (float): Takedown Accuracy (% of successful takedowns).
        td_def (float): Takedown Defense (% of opponent takedowns that did not land).
        sub_avg (float): Average Submissions Attempted per 15 minutes.
        last_updated (date): Date when the record was last updated.
    """

    fighter_id: int
    stance: str
    slpm: float
    str_acc: float
    sapm: float
    str_def: float
    td_avg: float
    td_acc: float
    td_def: float
    sub_avg: float
    last_updated: date

    class Config:
        orm_mode = True
