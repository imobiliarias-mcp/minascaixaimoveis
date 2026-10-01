"""Domain models decomposed into focused objects with maximum two fields."""

from dataclasses import dataclass
from minascaixa.domain.primitives import (
    PropertyCode,
    PageNumber,
    RentalPrice,
    CitySlug,
    SortOrder,
)


@dataclass(frozen=True)
class PropertyIdentity:
    """Core identifiers for a property."""

    code: PropertyCode
    title: str


@dataclass(frozen=True)
class PropertyLocation:
    """Geographic placement of a property."""

    city: str
    neighborhood: str


@dataclass(frozen=True)
class PropertyCore:
    """Aggregates identity and location."""

    identity: PropertyIdentity
    location: PropertyLocation


@dataclass(frozen=True)
class PropertyPricing:
    """Monetary attributes for a listing."""

    rental_value: str
    condo_fee: str


@dataclass(frozen=True)
class PropertyFeatures:
    """Spatial and structural attributes."""

    rooms_summary: str
    area_summary: str


@dataclass(frozen=True)
class PropertyProfile:
    """Aggregates pricing and spatial features."""

    pricing: PropertyPricing
    features: PropertyFeatures


@dataclass(frozen=True)
class PropertySummary:
    """Composite summary of a rental listing."""

    core: PropertyCore
    profile: PropertyProfile

    def code(self) -> PropertyCode:
        """Returns property code."""
        return self.core.identity.code

    def title(self) -> str:
        """Returns property title."""
        return self.core.identity.title

    def rental_value(self) -> str:
        """Returns formatted rental value."""
        return self.profile.pricing.rental_value


@dataclass(frozen=True)
class PriceBoundary:
    """Price range bounds."""

    minimum_price: RentalPrice
    maximum_price: RentalPrice


@dataclass(frozen=True)
class RoomFilter:
    """Minimum room requirements."""

    bedrooms: int
    parking_spaces: int


@dataclass(frozen=True)
class FilterBundle:
    """Aggregated search filter preferences."""

    price_bounds: PriceBoundary
    room_filter: RoomFilter


@dataclass(frozen=True)
class LocationScope:
    """Geographic scope for search execution."""

    city: CitySlug
    neighborhood_code: int


@dataclass(frozen=True)
class PaginationSpec:
    """Pagination and ordering preferences."""

    page_number: PageNumber
    sort_order: SortOrder


@dataclass(frozen=True)
class SearchCriteria:
    """High-level search configuration."""

    location: LocationScope
    filters: FilterBundle
