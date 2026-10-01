"""Live integration tests against minascaixaimoveis.com.br."""

import pytest
from minascaixa import (
    create_rental_research_service,
    PropertyCode,
    PageNumber,
    PaginationSpec,
    SortOrder,
    CitySlug,
    FrontendUrlParser,
)

TARGET_URL = (
    "https://www.minascaixaimoveis.com.br/aluguel/imoveis/timoteo/todos-os-bairros/"
    "0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios"
    "?valorminimo=0&valormaximo=0&pagina=1"
)


@pytest.fixture(scope="module")
def rental_service():
    return create_rental_research_service(timeout_seconds=20)


def test_live_search_target_url(rental_service) -> None:
    total_count, collection = rental_service.search_by_url(TARGET_URL)
    assert total_count >= 1
    assert collection.count() <= 20
    assert not collection.is_empty()

    first_property = collection.first()
    assert first_property.code().value > 0
    assert first_property.title() != ""
    assert "R$" in first_property.rental_value()


def test_live_pagination_pages(rental_service) -> None:
    parser = FrontendUrlParser()
    criteria, _ = parser.parse_url(TARGET_URL)

    # Page 1
    page1_spec = PaginationSpec(
        page_number=PageNumber(1), sort_order=SortOrder.price_descending()
    )
    total_1, collection_p1 = rental_service.search_rentals(criteria, page1_spec)
    assert collection_p1.count() == 20

    # Page 2
    page2_spec = PaginationSpec(
        page_number=PageNumber(2), sort_order=SortOrder.price_descending()
    )
    total_2, collection_p2 = rental_service.search_rentals(criteria, page2_spec)
    assert total_1 == total_2
    assert collection_p2.count() > 0

    # Page 3 (should be empty for 29 items)
    page3_spec = PaginationSpec(
        page_number=PageNumber(3), sort_order=SortOrder.price_descending()
    )
    _, collection_p3 = rental_service.search_rentals(criteria, page3_spec)
    assert collection_p3.is_empty()


def test_live_property_detail(rental_service) -> None:
    code = PropertyCode(6161)
    detail = rental_service.get_property_detail(code)
    assert detail["codigo"] == 6161
    assert "valor" in detail
    assert "cidade" in detail
    assert "fotos" in detail
    assert len(detail.keys()) > 100


def test_live_batch_detail(rental_service) -> None:
    codes = (PropertyCode(6161), PropertyCode(7989))
    results = rental_service.get_properties_batch(codes)
    assert len(results) == 2
    codes_returned = {item["codigo"] for item in results}
    assert 6161 in codes_returned
    assert 7989 in codes_returned


def test_live_cities_and_neighborhoods(rental_service) -> None:
    cities = rental_service.get_cities()
    assert cities.count() >= 20

    neighborhoods = rental_service.get_neighborhoods(CitySlug("timoteo"))
    assert neighborhoods.count() >= 30
