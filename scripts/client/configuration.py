"""Configuration settings for Minas Caixa Imóveis API client."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MinasCaixaConfiguration:
    """Holds configuration parameters for Minas Caixa portal communication."""

    base_url: str = "https://www.minascaixaimoveis.com.br"
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
    public_base_url: str = "https://www.minascaixaimoveis.com.br"

    def search_endpoint(self) -> str:
        """Endpoint for rental property search queries."""
        return f"{self.base_url}/imoveis/ajax/"

    def detail_endpoint(self) -> str:
        """Endpoint for full property detail retrieval."""
        return f"{self.base_url}/imoveis/codigos/"

    def cities_endpoint(self) -> str:
        """Endpoint for discovering available cities."""
        return f"{self.base_url}/cidadeAjax"

    def neighborhoods_endpoint(self) -> str:
        """Endpoint for discovering neighborhoods by city."""
        return f"{self.base_url}/bairroAjax"

    def types_endpoint(self) -> str:
        """Endpoint for discovering property types."""
        return f"{self.base_url}/tipoAjax"
