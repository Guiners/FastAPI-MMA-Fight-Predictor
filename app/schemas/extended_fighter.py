from __future__ import annotations

from typing import Optional

from pydantic import create_model

from .base_stats import BaseStats
from .extended_stats import ExtendedStats
from .fighter import Fighter
from .fights_results import FightsResults


class ExtendedFighter(Fighter):
    base_stats: BaseStats | None = None
    extended_stats: ExtendedStats | None = None
    fights_results: FightsResults | None = None

    class Config:
        from_attributes = True


ExtendedFighterFilter = create_model(
    "ExtendedFighterFilterFilter",
    **{
        field: (Optional[typ.annotation], None)
        for field, typ in ExtendedFighter.model_fields.items()
        if field != "fighter_id" or "last_updated"
    },
)
