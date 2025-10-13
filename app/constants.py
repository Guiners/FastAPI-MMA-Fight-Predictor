from app.db.models.base_stats import BaseStats
from app.db.models.extended_stats import ExtendedStats
from app.db.models.fighters import Fighters
from app.db.models.fights_results import FightsResults

example_data_paths = {
    Fighters: "./app/db/example_data/fighters.json",
    BaseStats: "./app/db/example_data/base_stats.json",
    ExtendedStats: "./app/db/example_data/extended_stats.json",
    FightsResults: "./app/db/example_data/fights_results.json",
}

version = "v1"

PREFIX = f"/api/{version}"
