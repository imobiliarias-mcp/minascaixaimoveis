"""Minas Caixa Imóveis - Rental Research MCP Boundary Package."""

import requests
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
from minascaixa.infrastructure.http_transport import RequestsHttpTransport
from minascaixa.infrastructure.deserializer import ResponseDeserializer
from minascaixa.application.service import RentalResearchService
from minascaixa.application.url_parser import FrontendUrlParser


def create_rental_research_service(
    timeout_seconds: int = 15,
    public_base_url: str | None = None,
) -> RentalResearchService:
    """Factory creating a fully configured RentalResearchService instance."""
    session = requests.Session()
    transport = RequestsHttpTransport(session=session, timeout_seconds=timeout_seconds)
    deserializer = ResponseDeserializer() if public_base_url is None else ResponseDeserializer(public_base_url)
    return RentalResearchService(http_transport=transport, deserializer=deserializer)


__all__ = [
    "create_rental_research_service",
    "RentalResearchService",
    "FrontendUrlParser",
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
