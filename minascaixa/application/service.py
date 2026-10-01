"""Primary service facade implementing the central Rental Research MCP boundary."""

from typing import Any, Dict, List, Tuple
from minascaixa.domain.primitives import PropertyCode, CitySlug
from minascaixa.domain.models import SearchCriteria, PaginationSpec
from minascaixa.domain.collections import (
    PropertyCollection,
    CityCollection,
    NeighborhoodCollection,
)
from minascaixa.domain.exceptions import PropertyNotFoundError
from minascaixa.infrastructure.endpoints import (
    SEARCH_ENDPOINT,
    DETAIL_ENDPOINT,
    CITIES_ENDPOINT,
    NEIGHBORHOODS_ENDPOINT,
)
from minascaixa.infrastructure.http_transport import HttpTransportProtocol
from minascaixa.infrastructure.payload_builder import SearchPayloadBuilder
from minascaixa.infrastructure.deserializer import ResponseDeserializer
from minascaixa.application.url_parser import FrontendUrlParser


class RentalResearchService:
    """Central service coordinator for rental research MCP integration."""

    def __init__(
        self,
        http_transport: HttpTransportProtocol,
        deserializer: ResponseDeserializer,
    ) -> None:
        self._http_transport = http_transport
        self._deserializer = deserializer

    def search_rentals(
        self, criteria: SearchCriteria, pagination: PaginationSpec
    ) -> Tuple[int, PropertyCollection]:
        """Performs rental search and returns total count and items collection."""
        builder = SearchPayloadBuilder()
        payload = builder.build_search_payload(criteria, pagination)
        raw_data = self._http_transport.post_form(SEARCH_ENDPOINT, payload)
        total_count = int(raw_data.get("quantidade", 0))
        collection = self._deserializer.deserialize_search_results(raw_data)
        return total_count, collection

    def search_by_url(self, target_url: str) -> Tuple[int, PropertyCollection]:
        """Parses target URL and executes rental search."""
        parser = FrontendUrlParser()
        criteria, pagination = parser.parse_url(target_url)
        return self.search_rentals(criteria, pagination)

    def get_property_detail(self, code: PropertyCode) -> Dict[str, Any]:
        """Retrieves full 219 attributes for a single property code."""
        batch_results = self.get_properties_batch((code,))
        if not batch_results:
            raise PropertyNotFoundError(f"Property with code {code.value} not found")
        return batch_results[0]

    def get_properties_batch(
        self, codes: Tuple[PropertyCode, ...]
    ) -> List[Dict[str, Any]]:
        """Retrieves full details for multiple property codes in a single request."""
        if not codes:
            return []
        codes_string = ",".join(c.as_string() for c in codes)
        payload = {"codigo": codes_string, "finalidade": "aluguel"}
        raw_data = self._http_transport.post_form(DETAIL_ENDPOINT, payload)
        raw_list = raw_data.get("lista", [])
        return list(raw_list)

    def get_cities(self) -> CityCollection:
        """Retrieves all available cities."""
        raw_data = self._http_transport.post_form(CITIES_ENDPOINT, {})
        return self._deserializer.deserialize_cities(raw_data)

    def get_neighborhoods(self, city: CitySlug) -> NeighborhoodCollection:
        """Retrieves all neighborhoods for a specific city."""
        payload = {"cidade": city.normalized()}
        raw_data = self._http_transport.post_form(NEIGHBORHOODS_ENDPOINT, payload)
        return self._deserializer.deserialize_neighborhoods(raw_data)
