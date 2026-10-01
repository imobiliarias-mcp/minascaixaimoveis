"""Unit tests for domain primitive value objects."""

import pytest
from minascaixa.domain.primitives import (
    PropertyCode,
    PageNumber,
    RentalPrice,
    CitySlug,
    SortOrder,
)
from minascaixa.domain.exceptions import ValidationError


def test_property_code_valid() -> None:
    code = PropertyCode(6161)
    assert code.value == 6161
    assert code.as_string() == "6161"


def test_property_code_invalid() -> None:
    with pytest.raises(ValidationError):
        PropertyCode(0)
    with pytest.raises(ValidationError):
        PropertyCode(-5)


def test_page_number_valid() -> None:
    page = PageNumber(1)
    assert page.value == 1
    assert page.as_string() == "1"


def test_page_number_invalid() -> None:
    with pytest.raises(ValidationError):
        PageNumber(0)


def test_rental_price_valid() -> None:
    price = RentalPrice(1500.0)
    assert price.amount == 1500.0
    assert price.as_integer_string() == "1500"


def test_rental_price_invalid() -> None:
    with pytest.raises(ValidationError):
        RentalPrice(-1.0)


def test_city_slug_normalization() -> None:
    city = CitySlug("  Timoteo  ")
    assert city.normalized() == "timoteo"


def test_city_slug_empty_invalid() -> None:
    with pytest.raises(ValidationError):
        CitySlug("   ")


def test_sort_order_valid() -> None:
    order = SortOrder.price_descending()
    assert order.value == "valordesc"
    asc_order = SortOrder.price_ascending()
    assert asc_order.value == "valorasc"


def test_sort_order_invalid() -> None:
    with pytest.raises(ValidationError):
        SortOrder("invalid_sort")
