from .country_endpoints import base_country_router
from .fighter_details_endpoints import base_fighter_details_router
from .id_endpoints import base_id_router
from .multiple_endpoint import base_multiple_router

__all__ = [
    "base_country_router",
    "base_fighter_details_router",
    "base_id_router",
    "base_multiple_router",
]
