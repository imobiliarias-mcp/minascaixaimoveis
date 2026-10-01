"""Unit tests for RentalResearchService using mock transport."""

from typing import Any, Dict
import pytest
from minascaixa.application.service import RentalResearchService
from minascaixa.infrastructure.deserializer import ResponseDeserializer
from minascaixa.domain.primitives import PropertyCode, CitySlug
from minascaixa.domain.exceptions import PropertyNotFoundError


class MockHttpTransport:
    """Mock implementation of HttpTransportProtocol."""

    def __init__(self, response_map: Dict[str, Any]) -> None:
        self._response_map = response_map

    def post_form(self, url: str, form_data: Dict[str, Any]) -> Any:
        return self._response_map.get(url, {})


def test_service_get_property_detail_found() -> None:
    fake_detail = {
        "quantidade": 1,
        "lista": [{"codigo": 6161, "tipo": "Prédio", "valor": "R$ 20.000,00"}],
    }
    mock_transport = MockHttpTransport(
        {"https://www.minascaixaimoveis.com.br/imoveis/codigos/": fake_detail}
    )
    service = RentalResearchService(
        http_transport=mock_transport, deserializer=ResponseDeserializer()
    )

    detail = service.get_property_detail(PropertyCode(6161))
    assert detail["codigo"] == 6161
    assert detail["tipo"] == "Prédio"


def test_service_get_property_detail_not_found() -> None:
    empty_response = {"quantidade": 0, "lista": []}
    mock_transport = MockHttpTransport(
        {"https://www.minascaixaimoveis.com.br/imoveis/codigos/": empty_response}
    )
    service = RentalResearchService(
        http_transport=mock_transport, deserializer=ResponseDeserializer()
    )

    with pytest.raises(PropertyNotFoundError):
        service.get_property_detail(PropertyCode(999999))
