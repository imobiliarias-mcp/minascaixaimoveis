"""Application interface ports defining the Rental Research MCP boundary."""

from typing import Any, Dict, List, Protocol, Tuple
from minascaixa.domain.primitives import PropertyCode, CitySlug
from minascaixa.domain.models import SearchCriteria, PaginationSpec
from minascaixa.domain.collections import (
    PropertyCollection,
    CityCollection,
    NeighborhoodCollection,
)


class RentalSearchPort(Protocol):
    """Port for executing rental searches."""

    def search_rentals(
        self, criteria: SearchCriteria, pagination: PaginationSpec
    ) -> Tuple[int, PropertyCollection]:
        """Executes rental search and returns total count with current page items."""
        ...

    def search_by_url(self, target_url: str) -> Tuple[int, PropertyCollection]:
        """Parses a frontend search URL and executes the search."""
        ...


class PropertyDetailPort(Protocol):
    """Port for retrieving rich property details."""

    def get_property_detail(self, code: PropertyCode) -> Dict[str, Any]:
        """Retrieves 219 attributes for a single property code."""
        ...

    def get_properties_batch(
        self, codes: Tuple[PropertyCode, ...]
    ) -> List[Dict[str, Any]]:
        """Retrieves properties in batch using a single HTTP round-trip."""
        ...


class FilterCatalogPort(Protocol):
    """Port for discovering available filter options."""

    def get_cities(self) -> CityCollection:
        """Retrieves all available cities."""
        ...

    def get_neighborhoods(self, city: CitySlug) -> NeighborhoodCollection:
        """Retrieves neighborhoods for a specific city."""
        ...
