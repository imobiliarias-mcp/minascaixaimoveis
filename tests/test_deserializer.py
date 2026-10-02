"""Unit tests for response deserializer."""

import pytest

from minascaixa.domain.exceptions import ValidationError
from minascaixa.domain.models import PropertySummary
from minascaixa.infrastructure.deserializer import ResponseDeserializer


def test_deserialize_search_results() -> None:
    deserializer = ResponseDeserializer()
    raw_payload = {
        "quantidade": 1,
        "lista": [
            {
                "codigo": 6161,
                "titulo": "predio-comercial-nos-funcionarios",
                "cidade": "Timóteo",
                "bairro": "Funcionarios",
                "valor": "R$ 20.000,00",
                "valorcondominio": "R$ 0,00",
                "numeroquartos": "0",
                "areainterna": "694,00",
            }
        ],
    }

    collection = deserializer.deserialize_search_results(raw_payload)
    assert collection.count() == 1
    assert not collection.is_empty()

    first = collection.first()
    assert first.code().value == 6161
    assert first.title() == "predio-comercial-nos-funcionarios"
    assert first.rental_value() == "R$ 20.000,00"


def test_deserialize_cities() -> None:
    deserializer = ResponseDeserializer()
    raw_cities = [
        {"codigo": 1, "nomeOriginal": "Timóteo"},
        {"codigo": 2, "nomeOriginal": "Coronel Fabriciano"},
    ]
    cities = deserializer.deserialize_cities(raw_cities)
    assert cities.count() == 2


def test_core_search_results_serialize_public_url_from_validated_codigo() -> None:
    deserializer = ResponseDeserializer(public_base_url="https://properties.example")
    payload = {
        "lista": [
            {
                "codigo": "6161",
                "id": 987654,
                "titulo": "predio-comercial",
                "valor": "R$ 20.000,00",
                "cidade": "Timóteo",
                "bairro": "Funcionários",
            }
        ]
    }

    collection = deserializer.deserialize_search_results(payload)
    listing = collection.to_dictionary_list()[0]
    assert listing["url"] == "https://properties.example/detalhe-imovel/6161"
    assert listing["code"] == 6161
    assert listing["title"] == "predio-comercial"
    assert listing["rental_value"] == "R$ 20.000,00"
    assert set(listing) == {"code", "title", "rental_value", "url"}


@pytest.mark.parametrize("codigo", [None, 0, -1, "invalid"])
def test_core_search_rejects_missing_or_invalid_public_codigo(codigo) -> None:
    deserializer = ResponseDeserializer()
    with pytest.raises(ValidationError, match="codigo"):
        deserializer.deserialize_search_results({"lista": [{"codigo": codigo}]})


def test_legacy_core_summary_preserves_constructor_and_rejects_missing_url() -> None:
    payload = {"lista": [{"codigo": 6161}]}
    summary = ResponseDeserializer().deserialize_search_results(payload).first()
    legacy_summary = PropertySummary(core=summary.core, profile=summary.profile)

    assert legacy_summary.core is summary.core
    assert legacy_summary.profile is summary.profile
    with pytest.raises(ValidationError, match="public property URL.*6161"):
        legacy_summary.to_dictionary()
