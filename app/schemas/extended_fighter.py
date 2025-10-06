from __future__ import annotations

from .base_stats import BaseStats, BaseStatsFilter
from .extended_stats import ExtendedStats, ExtendedStatsFilter
from .fighter import Fighter, FighterFilter
from .fights_results import FightsResults, FightsResultsFilter


class ExtendedFighter(Fighter):
    base_stats: BaseStats | None = None
    extended_stats: ExtendedStats | None = None
    fights_results: FightsResults | None = None

    class Config:
        from_attributes = True




class ExtendedFighterFilter(FighterFilter):
    base_stats: BaseStatsFilter | None = None
    extended_stats: ExtendedStatsFilter | None = None
    fights_results: FightsResultsFilter | None = None

    class Config:
        from_attributes = True
