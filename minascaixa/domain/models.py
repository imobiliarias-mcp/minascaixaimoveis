"""Domain models decomposed into focused objects with maximum two fields."""

from dataclasses import dataclass
from urllib.parse import urlsplit

from minascaixa.domain.exceptions import ValidationError
from minascaixa.domain.primitives import (
    CitySlug,
    PageNumber,
    PropertyCode,
    RentalPrice,
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
class PropertyNavigation:
    """Public property link associated with a listing code."""

    url: str = ""

    def validate_for(self, code: PropertyCode) -> str:
        """Return a valid property URL or raise with listing context."""
        code_value = code.as_string()
        try:
            parsed_url = urlsplit(self.url)
        except ValueError as exc:
            raise ValidationError(f"Invalid public property URL for codigo {code_value}") from exc
        expected_path = f"/detalhe-imovel/{code_value}"
        is_absolute = parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)
        if not is_absolute or parsed_url.path.rstrip("/") != expected_path:
            raise ValidationError(f"A valid public property URL is required for codigo {code_value}")
        return self.url


@dataclass(frozen=True)
class PropertyPresentation:
    """Composes listing profile and public navigation for presentation."""

    profile: PropertyProfile
    navigation: PropertyNavigation

    def public_url_for(self, code: PropertyCode) -> str:
        """Return the validated public property URL for a listing code."""
        return self.navigation.validate_for(code)


@dataclass(frozen=True, init=False)
class PropertySummary:
    """Composite summary retaining its original core/profile interface."""

    core: PropertyCore
    _presentation: PropertyPresentation

    def __init__(
        self,
        core: PropertyCore,
        profile: PropertyProfile,
        navigation: PropertyNavigation | None = None,
    ) -> None:
        """Build a summary while keeping the legacy core/profile arguments."""
        selected_navigation = navigation or PropertyNavigation()
        presentation = PropertyPresentation(profile, selected_navigation)
        object.__setattr__(self, "core", core)
        object.__setattr__(self, "_presentation", presentation)

    @property
    def profile(self) -> PropertyProfile:
        """Preserve direct access to the legacy listing profile."""
        return self._presentation.profile

    def code(self) -> PropertyCode:
        """Returns property code."""
        return self.core.identity.code

    def title(self) -> str:
        """Returns property title."""
        return self.core.identity.title

    def rental_value(self) -> str:
        """Returns formatted rental value."""
        return self.profile.pricing.rental_value

    def to_dictionary(self) -> dict:
        """Serialize the property summary for API and runner consumers."""
        public_url = self._presentation.public_url_for(self.code())
        return {
            "code": self.code().value,
            "title": self.title(),
            "rental_value": self.rental_value(),
            "url": public_url,
        }


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
