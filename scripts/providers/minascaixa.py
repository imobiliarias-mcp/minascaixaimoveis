"""Minas Caixa rental search provider implementation."""

import httpx
from scripts.client.configuration import MinasCaixaConfiguration
from scripts.client.http_transport import MinasCaixaHttpTransport
from scripts.client.query_builder import MinasCaixaQueryBuilder
from scripts.client.parsers import (
    SearchResultParser,
    PropertyDetailParser,
    FacetParser,
)
from scripts.domain.criteria import RentalFilter
from scripts.domain.value_objects import PropertyCode
from scripts.domain.entities import RentalPropertyDetail
from scripts.domain.collections import (
    RentalSearchResult,
    FacetCollection,
)
from scripts.interfaces.provider import RentalProviderProtocol


class MinasCaixaRentalProvider(RentalProviderProtocol):
    """Adapter implementing RentalProviderProtocol for Minas Caixa portal."""

    def __init__(
        self,
        transport: MinasCaixaHttpTransport,
        configuration: MinasCaixaConfiguration,
    ) -> None:
        self._transport = transport
        self._configuration = configuration

    @classmethod
    def create_default(cls) -> "MinasCaixaRentalProvider":
        """Factory method constructing provider with default configurations."""
        configuration = MinasCaixaConfiguration()
        client = httpx.Client(timeout=20.0)
        transport = MinasCaixaHttpTransport(
            configuration=configuration, http_client=client
        )
        return cls(transport=transport, configuration=configuration)

    def provider_name(self) -> str:
        """Return unique provider identifier for central MCP registry."""
        return "minas_caixa"

    def search_rentals(self, search_filter: RentalFilter) -> RentalSearchResult:
        """Search rental listings using criteria."""
        endpoint = self._configuration.search_endpoint()
        query_builder = MinasCaixaQueryBuilder()
        form_payload = query_builder.build_parameters(search_filter)
        raw_response = self._transport.post_form(endpoint, form_payload)
        parser = SearchResultParser(self._configuration.public_base_url)
        return parser.parse_search_response(raw_response)

    def get_property_detail(self, code: PropertyCode) -> RentalPropertyDetail:
        """Retrieve full details for a single property by code."""
        endpoint = self._configuration.detail_endpoint()
        payload = {"codigo": code.value(), "finalidade": "aluguel"}
        raw_response = self._transport.post_form(endpoint, payload)
        parser = PropertyDetailParser(self._configuration.public_base_url)
        return parser.parse_detail_response(raw_response)

    def get_facets(self) -> FacetCollection:
        """Retrieve available cities and neighborhoods facets."""
        cities_url = self._configuration.cities_endpoint()
        raw_cities = self._transport.post_form(cities_url, {})
        bairros_url = self._configuration.neighborhoods_endpoint()
        raw_bairros = self._transport.post_form(bairros_url, {"cidade": "timoteo"})
        parser = FacetParser()
        return parser.parse_facets(raw_cities, raw_bairros)
