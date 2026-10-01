"""Domain layer for Minas Caixa rental research."""

from minascaixa.domain.primitives import (
    PropertyCode,
    PageNumber,
    RentalPrice,
    CitySlug,
    SortOrder,
)
from minascaixa.domain.models import (
    PropertySummary,
    SearchCriteria,
    PaginationSpec,
)
from minascaixa.domain.collections import (
    PropertyCollection,
    CityCollection,
    NeighborhoodCollection,
)
from minascaixa.domain.exceptions import (
    MinasCaixaError,
    ValidationError,
    ApiCommunicationError,
    PropertyNotFoundError,
)

__all__ = [
    "PropertyCode",
    "PageNumber",
    "RentalPrice",
    "CitySlug",
    "SortOrder",
    "PropertySummary",
    "SearchCriteria",
    "PaginationSpec",
    "PropertyCollection",
    "CityCollection",
    "NeighborhoodCollection",
    "MinasCaixaError",
    "ValidationError",
    "ApiCommunicationError",
    "PropertyNotFoundError",
]
