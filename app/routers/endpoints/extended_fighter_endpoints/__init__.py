from .country_endpoints import extended_country_router
from .fighter_details_endpoints import extended_fighter_details_router
from .id_endpoints import extended_id_router
from .multiple_endpoint import extended_multiple_router
from .search_endpoints import extended_search_router

__all__ = [
    "extended_country_router",
    "extended_fighter_details_router",
    "extended_id_router",
    "extended_multiple_router",
    "extended_search_router",
]
