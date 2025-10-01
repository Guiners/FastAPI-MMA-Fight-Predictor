from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base

if TYPE_CHECKING:
    from .fighters import Fighters


class FightsResults(Base):
    """Detailed fight outcomes for a fighter.
    Attributes:
        fighter_id (int): Primary key and foreign key to Fighters.fighter_id.
        win_by_ko_tko (int): Number of wins by knockout or technical knockout.
        loss_by_ko_tko (int): Number of losses by knockout or technical knockout.
        win_by_sub (int): Number of wins by submission.
        loss_by_sub (int): Number of losses by submission.
        win_by_dec (int): Number of wins by decision.
        loss_by_dec (int): Number of losses by decision.
        non_contest (int): Number of fights declared as no contest.
        last_updated (date): Date when the record was last updated.
        fighter (Fighters): ORM relationship to the main Fighter record.
    """

    __tablename__ = "fights_results"
    fighter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fighters.fighter_id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    win_by_ko_tko: Mapped[int] = mapped_column(Integer)
    loss_by_ko_tko: Mapped[int] = mapped_column(Integer)
    win_by_sub: Mapped[int] = mapped_column(Integer)
    loss_by_sub: Mapped[int] = mapped_column(Integer)
    win_by_dec: Mapped[int] = mapped_column(Integer)
    loss_by_dec: Mapped[int] = mapped_column(Integer)
    non_contest: Mapped[int] = mapped_column(Integer)
    last_updated: Mapped[Date] = mapped_column(Date, default=func.now())

    # relationships
    fighter: Mapped["Fighters"] = relationship(
        back_populates="fights_results", uselist=False
    )
