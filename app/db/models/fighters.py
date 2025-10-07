from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Date, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base

if TYPE_CHECKING:
    from .base_stats import BaseStats
    from .extended_stats import ExtendedStats
    from .fights_results import FightsResults


class Fighters(Base):
    """Represents a fighter in the database.
    Attributes:
        fighter_id (int): Primary key, auto-incremented unique ID of the fighter.
        name (str): First name of the fighter.
        nickname (str): Nickname of the fighter.
        surname (str): Last name (surname) of the fighter.
        country (str): Country of origin.
        weight_class (str): Weight division of the fighter.
        wins (int): Total number of wins.
        loss (int): Total number of losses.
        draw (int): Total number of draws.
        current_streak (int): Current winning or losing streak.
        last_fight_date (date): Date of the fighter's last fight.
        last_updated (date): Timestamp of the last update in the database.
    """

    __tablename__ = "fighters"
    fighter_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    weight_class: Mapped[str] = mapped_column(String(50), nullable=True)
    wins: Mapped[int] = mapped_column(Integer, nullable=True)
    loss: Mapped[int] = mapped_column(Integer, nullable=True)
    draw: Mapped[int] = mapped_column(Integer, nullable=True)
    current_streak: Mapped[int] = mapped_column(Integer, nullable=True)
    last_fight_date: Mapped[Date] = mapped_column(Date, nullable=True)
    last_updated: Mapped[Date] = mapped_column(Date, default=func.now())

    # relationships
    base_stats: Mapped["BaseStats"] = relationship(
        back_populates="fighter", uselist=False
    )
    extended_stats: Mapped["ExtendedStats"] = relationship(
        back_populates="fighter", uselist=False
    )
    fights_results: Mapped["FightsResults"] = relationship(
        back_populates="fighter", uselist=False
    )

    __table_args__ = (
        UniqueConstraint(
            "name", "nickname", "surname", name="uq_name_nickname_surname"
        ),
    )
