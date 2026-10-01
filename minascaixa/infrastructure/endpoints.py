"""Endpoint definitions and constants for Minas Caixa Imóveis API."""

BASE_URL = "https://www.minascaixaimoveis.com.br"

SEARCH_ENDPOINT = f"{BASE_URL}/imoveis/ajax/"
DETAIL_ENDPOINT = f"{BASE_URL}/imoveis/codigos/"
RELATED_ENDPOINT = f"{BASE_URL}/imoveis/relacionadosAjax/"
CITIES_ENDPOINT = f"{BASE_URL}/cidadeAjax"
NEIGHBORHOODS_ENDPOINT = f"{BASE_URL}/bairroAjax"
TYPES_ENDPOINT = f"{BASE_URL}/tipoAjax"
CONDOS_ENDPOINT = f"{BASE_URL}/condominios"

DEFAULT_RENTAL_PURPOSE = "aluguel"
DEFAULT_PAGE_SIZE = 20
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
