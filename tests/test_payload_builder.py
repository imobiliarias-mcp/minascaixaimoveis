"""Unit tests for search payload builder."""

from minascaixa.infrastructure.payload_builder import SearchPayloadBuilder
from minascaixa.domain.primitives import (
    PropertyCode,
    PageNumber,
    RentalPrice,
    CitySlug,
    SortOrder,
)
from minascaixa.domain.models import (
    LocationScope,
    PriceBoundary,
    RoomFilter,
    FilterBundle,
    SearchCriteria,
    PaginationSpec,
)


def test_mandatory_fields_present_in_payload() -> None:
    builder = SearchPayloadBuilder()
    location = LocationScope(city=CitySlug("timoteo"), neighborhood_code=0)
    prices = PriceBoundary(
        minimum_price=RentalPrice(0.0), maximum_price=RentalPrice(0.0)
    )
    rooms = RoomFilter(bedrooms=0, parking_spaces=0)
    filters = FilterBundle(price_bounds=prices, room_filter=rooms)
    criteria = SearchCriteria(location=location, filters=filters)
    pagination = PaginationSpec(
        page_number=PageNumber(1), sort_order=SortOrder.price_descending()
    )

    payload = builder.build_search_payload(criteria, pagination)

    # All 5 mandatory fields must be present
    assert payload["imovel[finalidade]"] == "aluguel"
    assert payload["imovel[valorde]"] == "0"
    assert payload["imovel[valorate]"] == "0"
    assert payload["imovel[pagina]"] == "1"
    assert payload["imovel[codigocondominio]"] == "0"

    # Supporting filters
    assert payload["imovel[codigocidade]"] == "timoteo"
    assert payload["imovel[numeroquartos]"] == "0-quartos"
    assert payload["imovel[numerovagas]"] == "0-vaga"
    assert payload["imovel[ordenacao]"] == "valordesc"
