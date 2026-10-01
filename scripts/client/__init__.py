"""Client package exports."""

from scripts.client.configuration import MinasCaixaConfiguration
from scripts.client.http_transport import MinasCaixaHttpTransport
from scripts.client.query_builder import MinasCaixaQueryBuilder
from scripts.client.parsers import (
    SearchResultParser,
    PropertyDetailParser,
    FacetParser,
)

__all__ = [
    "MinasCaixaConfiguration",
    "MinasCaixaHttpTransport",
    "MinasCaixaQueryBuilder",
    "SearchResultParser",
    "PropertyDetailParser",
    "FacetParser",
]
