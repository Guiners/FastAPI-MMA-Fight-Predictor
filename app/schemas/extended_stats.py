from datetime import date

from pydantic import BaseModel

from app.tools.utils import create_filter_schema


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

    fighter_id: int | None
    stance: str | None
    slpm: float | None
    str_acc: float | None
    sapm: float | None
    str_def: float | None
    td_avg: float | None
    td_acc: float | None
    td_def: float | None
    sub_avg: float | None
    last_updated: date

    model_config = {"from_attributes": True}


ExtendedStatsFilter = create_filter_schema(ExtendedStats)
