"""Unit tests for RentalResearchService using mock transport."""

from dataclasses import replace
from typing import Any

import pytest

from minascaixa.application.service import RentalResearchService
from minascaixa.domain.exceptions import PropertyNotFoundError
from minascaixa.domain.primitives import PropertyCode
from minascaixa.infrastructure.deserializer import ResponseDeserializer
from scripts.client.configuration import MinasCaixaConfiguration
from scripts.client.parsers import SearchResultParser
from scripts.domain.criteria import RentalFilter
from scripts.domain.exceptions import InvalidPropertyCodeException
from scripts.mcp.tools import MinasCaixaMcpAdapter
from scripts.providers.minascaixa import MinasCaixaRentalProvider
from scripts.run_research import _display_sample_properties
from scripts.run_search import display_results


class MockHttpTransport:
    """Mock implementation of HttpTransportProtocol."""

    def __init__(self, response_map: dict[str, Any]) -> None:
        self._response_map = response_map

    def post_form(self, url: str, form_data: dict[str, Any]) -> Any:
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


MINAS_SEARCH_PAYLOAD = {
    "quantidade": 1,
    "lista": [
        {
            "codigo": "6161",
            "id": 987654,
            "titulo": "predio-comercial",
            "tipo": "Prédio",
            "valor": "R$ 20.000,00",
            "cidade": "Timóteo",
            "bairro": "Funcionários",
            "urlfotoprincipalp": "https://cdn.example/6161.jpg",
        }
    ],
}


class StubMinasTransport:
    """Record provider calls while returning only an offline listing fixture."""

    def __init__(self) -> None:
        self.calls = []

    def post_form(self, url, form_data):
        self.calls.append((url, form_data))
        return MINAS_SEARCH_PAYLOAD


def test_configuration_preserves_legacy_positional_user_agent() -> None:
    configuration = MinasCaixaConfiguration("https://api.example", "Custom agent")

    assert configuration.user_agent == "Custom agent"
    assert configuration.public_base_url == "https://www.minascaixaimoveis.com.br"
    transport = StubMinasTransport()
    provider = MinasCaixaRentalProvider(transport, configuration)
    result = provider.search_rentals(RentalFilter())

    assert result.to_dictionary()["listings"][0]["url"] == (
        "https://www.minascaixaimoveis.com.br/detalhe-imovel/6161"
    )
    assert transport.calls[0][0] == "https://api.example/imoveis/ajax/"


def test_script_search_uses_public_base_and_validated_codigo(capsys) -> None:
    configuration = MinasCaixaConfiguration(
        base_url="https://api.example",
        public_base_url="https://public.example",
    )
    transport = StubMinasTransport()
    provider = MinasCaixaRentalProvider(transport, configuration)

    result = provider.search_rentals(RentalFilter())
    listing = result.to_dictionary()["listings"][0]
    assert listing["url"] == "https://public.example/detalhe-imovel/6161"
    assert listing["media_url"] == "https://cdn.example/6161.jpg"
    assert len(transport.calls) == 1
    assert transport.calls[0][0] == "https://api.example/imoveis/ajax/"
    assert all("6161" != str(value) for value in transport.calls[0][1].values())

    display_results(result)
    output = capsys.readouterr().out
    assert "Link: https://public.example/detalhe-imovel/6161" in output


def test_script_mcp_search_keeps_public_url_and_makes_no_detail_call() -> None:
    configuration = MinasCaixaConfiguration()
    transport = StubMinasTransport()
    provider = MinasCaixaRentalProvider(transport, configuration)
    adapter = MinasCaixaMcpAdapter(provider)

    listing = adapter.search_rentals()["listings"][0]
    assert listing["url"] == "https://www.minascaixaimoveis.com.br/detalhe-imovel/6161"
    assert len(transport.calls) == 1
    assert "/imoveis/ajax/" in transport.calls[0][0]


def test_legacy_script_listing_rejects_serialization_without_public_url() -> None:
    provider = MinasCaixaRentalProvider(StubMinasTransport(), MinasCaixaConfiguration())
    listing = provider.search_rentals(RentalFilter()).listings().listings[0]
    legacy_details = replace(listing.details, public_url="")
    legacy_listing = replace(listing, details=legacy_details)
    with pytest.raises(ValueError, match="public property URL.*6161"):
        legacy_listing.to_dictionary()


def test_script_parser_rejects_missing_public_property_code() -> None:
    with pytest.raises(InvalidPropertyCodeException, match="codigo"):
        SearchResultParser().parse_search_response({"lista": [{"codigo": ""}]})


def test_core_verification_runner_prints_public_link(capsys) -> None:
    collection = ResponseDeserializer().deserialize_search_results(MINAS_SEARCH_PAYLOAD)
    _display_sample_properties(collection)
    assert "Link: https://www.minascaixaimoveis.com.br/detalhe-imovel/6161" in capsys.readouterr().out
