"""Unit tests for response deserializer."""

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
