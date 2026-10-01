"""Translates domain search specifications into wire-format form payloads."""

from typing import Dict
from minascaixa.domain.models import SearchCriteria, PaginationSpec
from minascaixa.infrastructure.endpoints import DEFAULT_RENTAL_PURPOSE


class SearchPayloadBuilder:
    """Builds x-www-form-urlencoded compatible payload dictionaries."""

    def build_search_payload(
        self, criteria: SearchCriteria, pagination: PaginationSpec
    ) -> Dict[str, str]:
        """Assembles form dictionary guaranteeing mandatory fields."""
        payload: Dict[str, str] = {}
        self._populate_mandatory_fields(payload, criteria, pagination)
        self._populate_location_fields(payload, criteria)
        self._populate_room_fields(payload, criteria)
        self._populate_order_field(payload, pagination)
        return payload

    def _populate_mandatory_fields(
        self, payload: Dict[str, str], criteria: SearchCriteria, pagination: PaginationSpec
    ) -> None:
        payload["imovel[finalidade]"] = DEFAULT_RENTAL_PURPOSE
        min_price = criteria.filters.price_bounds.minimum_price
        max_price = criteria.filters.price_bounds.maximum_price
        payload["imovel[valorde]"] = min_price.as_integer_string()
        payload["imovel[valorate]"] = max_price.as_integer_string()
        payload["imovel[pagina]"] = pagination.page_number.as_string()
        payload["imovel[codigocondominio]"] = "0"

    def _populate_location_fields(
        self, payload: Dict[str, str], criteria: SearchCriteria
    ) -> None:
        city_slug = criteria.location.city.normalized()
        payload["imovel[codigocidade]"] = city_slug

    def _populate_room_fields(
        self, payload: Dict[str, str], criteria: SearchCriteria
    ) -> None:
        bedrooms = criteria.filters.room_filter.bedrooms
        vagas = criteria.filters.room_filter.parking_spaces
        payload["imovel[numeroquartos]"] = self._format_bedroom_param(bedrooms)
        payload["imovel[numerovagas]"] = self._format_parking_param(vagas)
        payload["imovel[numerosuite]"] = "0-suite-ou-mais"
        payload["imovel[numerobanhos]"] = "0-banheiro-ou-mais"

    def _format_bedroom_param(self, count: int) -> str:
        if count <= 0:
            return "0-quartos"
        return f"{count}-quartos"

    def _format_parking_param(self, count: int) -> str:
        if count <= 0:
            return "0-vaga"
        return f"{count}-vaga"

    def _populate_order_field(
        self, payload: Dict[str, str], pagination: PaginationSpec
    ) -> None:
        order_value = pagination.sort_order.value
        payload["imovel[ordenacao]"] = order_value
