"""Translates domain RentalFilter into Minas Caixa portal form payload."""

from typing import Dict
from scripts.domain.criteria import RentalFilter


class MinasCaixaQueryBuilder:
    """Converts domain RentalFilter into wire-format form parameter dictionaries."""

    def build_parameters(self, search_filter: RentalFilter) -> Dict[str, str]:
        """Assembles form dictionary guaranteeing mandatory fields."""
        payload: Dict[str, str] = {
            "imovel[finalidade]": "aluguel",
            "imovel[codigocondominio]": "0",
            "imovel[ordenacao]": "valordesc",
        }
        self._append_pricing(payload, search_filter)
        self._append_pagination(payload, search_filter)
        self._append_location(payload, search_filter)
        self._append_specifications(payload, search_filter)
        return payload

    def _append_pricing(self, payload: Dict[str, str], search_filter: RentalFilter) -> None:
        price_range = search_filter.constraints.price_range
        min_amount = int(price_range.minimum_price.value())
        max_amount = int(price_range.maximum_price.value())
        payload["imovel[valorde]"] = str(min_amount)
        payload["imovel[valorate]"] = str(max_amount)

    def _append_pagination(self, payload: Dict[str, str], search_filter: RentalFilter) -> None:
        page_index = search_filter.constraints.pagination.page_number
        payload["imovel[pagina]"] = str(page_index)

    def _append_location(self, payload: Dict[str, str], search_filter: RentalFilter) -> None:
        city_name = search_filter.criteria.location.city.strip().lower()
        if not city_name:
            city_name = "timoteo"
        payload["imovel[codigocidade]"] = city_name

    def _append_specifications(
        self, payload: Dict[str, str], search_filter: RentalFilter
    ) -> None:
        bedrooms = search_filter.criteria.specifications.minimum_bedrooms
        payload["imovel[numeroquartos]"] = self._format_bedroom_param(bedrooms)
        payload["imovel[numerovagas]"] = "0-vaga"
        payload["imovel[numerosuite]"] = "0-suite-ou-mais"
        payload["imovel[numerobanhos]"] = "0-banheiro-ou-mais"

    def _format_bedroom_param(self, count: int) -> str:
        if count <= 0:
            return "0-quartos"
        return f"{count}-quartos"
