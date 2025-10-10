from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Users(Base):

    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        autoincrement=True,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


# https://www.youtube.com/watch?v=0A_GCXBCNUQ
