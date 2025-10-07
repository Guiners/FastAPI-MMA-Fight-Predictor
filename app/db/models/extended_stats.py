from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base

if TYPE_CHECKING:
    from .base_stats import BaseStats
    from .fighters import Fighters


class ExtendedStats(Base):
    """Extended statistical information for a fighter.
    Attributes:
        fighter_id (int): Primary key and foreign key to Fighters.fighter_id.
        stance (str): Fighter's stance (e.g., Orthodox, Southpaw).
        slpm (float): Significant Strikes Landed per Minute.
        str_acc (float): Significant Striking Accuracy (% of significant strikes landed).
        sapm (float): Significant Strikes Absorbed per Minute.
        str_def (float): Significant Strike Defence (% of opponents' strikes that did not land).
        td_avg (float): Average Takedowns Landed per 15 minutes.
        td_acc (float): Takedown Accuracy (% of successful takedowns).
        td_def (float): Takedown Defense (% of opponents' takedown attempts that did not land).
        sub_avg (float): Average Submissions Attempted per 15 minutes.
        last_updated (date): Date when the record was last updated.
        fighter (Fighters): ORM relationship to the main Fighter record.
        base_stats (BaseStats): ORM relationship to base statistical data for the fighter.
    """

    __tablename__ = "extended_stats"
    fighter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fighters.fighter_id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    stance: Mapped[str] = mapped_column(String(50), nullable=True)
    slpm: Mapped[float] = mapped_column(Float, nullable=True)
    str_acc: Mapped[float] = mapped_column(Float, nullable=True)
    sapm: Mapped[float] = mapped_column(Float, nullable=True)
    str_def: Mapped[float] = mapped_column(Float, nullable=True)
    td_avg: Mapped[float] = mapped_column(Float, nullable=True)
    td_acc: Mapped[float] = mapped_column(Float, nullable=True)
    td_def: Mapped[float] = mapped_column(Float, nullable=True)
    sub_avg: Mapped[float] = mapped_column(Float, nullable=True)
    last_updated: Mapped[Date] = mapped_column(Date, default=func.now())

    # relationships
    fighter: Mapped["Fighters"] = relationship(
        back_populates="extended_stats", uselist=False
    )
    # base_stats: Mapped["BaseStats"] = relationship(
    #     back_populates="extended_stats", uselist=False
    # )
