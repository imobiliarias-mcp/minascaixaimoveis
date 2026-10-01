"""HTTP transport implementation using httpx."""

from typing import Any, Dict
import httpx
from scripts.client.configuration import MinasCaixaConfiguration
from scripts.domain.exceptions import ProviderTransportException


class MinasCaixaHttpTransport:
    """Performs HTTP communication with fail-fast validation."""

    def __init__(
        self,
        configuration: MinasCaixaConfiguration,
        http_client: httpx.Client,
    ) -> None:
        self._configuration = configuration
        self._http_client = http_client

    def post_form(self, url: str, form_data: Dict[str, Any]) -> Any:
        """Executes HTTP POST with form payload and returns JSON."""
        headers = {"User-Agent": self._configuration.user_agent}
        response = self._execute_post(url, form_data, headers)
        self._verify_status_code(response, url)
        return self._extract_json(response, url)

    def _execute_post(
        self, url: str, form_data: Dict[str, Any], headers: Dict[str, str]
    ) -> httpx.Response:
        try:
            return self._http_client.post(url, data=form_data, headers=headers)
        except httpx.HTTPError as error:
            raise ProviderTransportException(f"Network error accessing {url}: {error}") from error

    def _verify_status_code(self, response: httpx.Response, url: str) -> None:
        if response.status_code != 200:
            status = response.status_code
            raise ProviderTransportException(f"Target {url} returned non-200 code: {status}")

    def _extract_json(self, response: httpx.Response, url: str) -> Any:
        try:
            return response.json()
        except ValueError as error:
            snippet = response.text[:200]
            raise ProviderTransportException(f"Invalid JSON returned from {url}: {snippet}") from error
