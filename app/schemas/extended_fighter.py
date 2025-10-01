from typing import Optional

from .base_stats import BaseStats
from .extended_stats import ExtendedStats
from .fighter import Fighter
from .fights_results import FightsResults


class ExtendedFighter(Fighter):
    base_stats: Optional[BaseStats] = None
    extended_stats: Optional[ExtendedStats] = None
    fights_results: Optional[FightsResults] = None

    class Config:
        from_attributes = True
