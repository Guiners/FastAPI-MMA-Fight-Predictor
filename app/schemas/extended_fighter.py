from __future__ import annotations

from .base_stats import BaseStats, BaseStatsFilter
from .extended_stats import ExtendedStats, ExtendedStatsFilter
from .fighter import Fighter, FighterFilter
from .fights_results import FightsResults, FightsResultsFilter


class ExtendedFighter(Fighter):
    """
    Represents an extended fighter model that includes additional statistics and fight results.

    Attributes:
        base_stats (BaseStats | None): Basic physical and personal statistics of the fighter.
        extended_stats (ExtendedStats | None): Detailed extended statistics such as strike accuracy or takedown data.
        fights_results (FightsResults | None): Summary of the fighter's recent fight outcomes.
    """

    base_stats: BaseStats | None = None
    extended_stats: ExtendedStats | None = None
    fights_results: FightsResults | None = None

    model_config = {"from_attributes": True}


class ExtendedFighterFilter(FighterFilter):
    """
    Filter schema for querying extended fighter data.

    Attributes:
        base_stats (BaseStatsFilter | None): Filters applied to base statistics.
        extended_stats (ExtendedStatsFilter | None): Filters applied to extended statistics.
        fights_results (FightsResultsFilter | None): Filters applied to fight result data.
    """

    base_stats: BaseStatsFilter | None = None
    extended_stats: ExtendedStatsFilter | None = None
    fights_results: FightsResultsFilter | None = None

    model_config = {"from_attributes": True}
