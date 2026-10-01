"""Unit tests for the frontend URL parser."""

import pytest
from minascaixa.application.url_parser import FrontendUrlParser
from minascaixa.domain.exceptions import ValidationError

TARGET_URL = (
    "https://www.minascaixaimoveis.com.br/aluguel/imoveis/timoteo/todos-os-bairros/"
    "0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios"
    "?valorminimo=0&valormaximo=0&pagina=1"
)


def test_parse_target_url() -> None:
    parser = FrontendUrlParser()
    criteria, pagination = parser.parse_url(TARGET_URL)

    assert criteria.location.city.normalized() == "timoteo"
    assert criteria.filters.price_bounds.minimum_price.amount == 0.0
    assert criteria.filters.price_bounds.maximum_price.amount == 0.0
    assert criteria.filters.room_filter.bedrooms == 0
    assert criteria.filters.room_filter.parking_spaces == 0
    assert pagination.page_number.value == 1


def test_parse_url_with_custom_filters() -> None:
    url = (
        "https://www.minascaixaimoveis.com.br/aluguel/imoveis/coronel-fabriciano/todos-os-bairros/"
        "3-quartos/0-suite-ou-mais/2-vaga/0-banheiro-ou-mais/todos-os-condominios"
        "?valorminimo=1000&valormaximo=5000&pagina=2"
    )
    parser = FrontendUrlParser()
    criteria, pagination = parser.parse_url(url)

    assert criteria.location.city.normalized() == "coronel-fabriciano"
    assert criteria.filters.price_bounds.minimum_price.amount == 1000.0
    assert criteria.filters.price_bounds.maximum_price.amount == 5000.0
    assert criteria.filters.room_filter.bedrooms == 3
    assert criteria.filters.room_filter.parking_spaces == 2
    assert pagination.page_number.value == 2


def test_parse_invalid_url_not_rental() -> None:
    url = "https://www.minascaixaimoveis.com.br/venda/imoveis/timoteo"
    parser = FrontendUrlParser()
    with pytest.raises(ValidationError):
        parser.parse_url(url)
