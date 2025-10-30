from __future__ import annotations

import typing

from sqlalchemy import Date, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base

if typing.TYPE_CHECKING:
    from .fighters import Fighters


class BaseStats(Base):
    """Detailed information about a fighter.
    Attributes:
        fighter_id (int): Primary key and foreign key to Fighters.fighter_id.
        weight (int): Weight of the fighter in kilograms.
        height (int): Height of the fighter in centimeters.
        reach (int): Reach of the fighter in centimeters
        age (int): Age of the fighter in years.
        last_updated (date): Date when the record was last updated.
        fighter (Fighters): ORM relationship to the main Fighter record.
    """

    __tablename__ = "base_stats"
    fighter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fighters.fighter_id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    reach: Mapped[float] = mapped_column(Float, nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    last_updated: Mapped[Date] = mapped_column(Date, default=func.now())

    # relationships
    fighter: Mapped["Fighters"] = relationship(
        back_populates="base_stats", uselist=False
    )
