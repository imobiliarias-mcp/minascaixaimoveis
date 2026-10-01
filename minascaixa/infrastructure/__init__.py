"""Infrastructure layer for Minas Caixa rental research."""

from minascaixa.infrastructure.endpoints import (
    BASE_URL,
    SEARCH_ENDPOINT,
    DETAIL_ENDPOINT,
    CITIES_ENDPOINT,
    NEIGHBORHOODS_ENDPOINT,
)
from minascaixa.infrastructure.http_transport import (
    HttpTransportProtocol,
    RequestsHttpTransport,
)
from minascaixa.infrastructure.payload_builder import SearchPayloadBuilder
from minascaixa.infrastructure.deserializer import ResponseDeserializer

__all__ = [
    "BASE_URL",
    "SEARCH_ENDPOINT",
    "DETAIL_ENDPOINT",
    "CITIES_ENDPOINT",
    "NEIGHBORHOODS_ENDPOINT",
    "HttpTransportProtocol",
    "RequestsHttpTransport",
    "SearchPayloadBuilder",
    "ResponseDeserializer",
]
