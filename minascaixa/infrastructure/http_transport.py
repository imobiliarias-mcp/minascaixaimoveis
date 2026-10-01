"""HTTP transport implementation with fail-fast validation and error wrapping."""

from typing import Any, Dict, Protocol
import requests
from minascaixa.domain.exceptions import ApiCommunicationError
from minascaixa.infrastructure.endpoints import DEFAULT_USER_AGENT


class HttpTransportProtocol(Protocol):
    """Protocol for performing POST requests."""

    def post_form(self, url: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submits form data to target URL and returns parsed JSON response."""
        ...


class RequestsHttpTransport:
    """Concrete HTTP transport backed by requests Session."""

    def __init__(self, session: requests.Session, timeout_seconds: int = 15) -> None:
        self._session = session
        self._timeout_seconds = timeout_seconds
        self._session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    def post_form(self, url: str, form_data: Dict[str, Any]) -> Any:
        """Executes HTTP POST and validates JSON payload returned."""
        self._validate_target_url(url)
        response = self._execute_request(url, form_data)
        self._ensure_successful_status(response, url)
        return self._extract_json(response, url)

    def _validate_target_url(self, url: str) -> None:
        if not url.strip():
            raise ApiCommunicationError("Target URL cannot be empty")

    def _execute_request(self, url: str, form_data: Dict[str, Any]) -> requests.Response:
        try:
            return self._session.post(url, data=form_data, timeout=self._timeout_seconds)
        except requests.RequestException as error:
            raise ApiCommunicationError(f"HTTP request failed: {error}") from error

    def _ensure_successful_status(self, response: requests.Response, url: str) -> None:
        if response.status_code != 200:
            status = response.status_code
            raise ApiCommunicationError(f"Request to {url} returned non-200 status: {status}")

    def _extract_json(self, response: requests.Response, url: str) -> Any:
        try:
            return response.json()
        except ValueError as error:
            preview = response.text[:200]
            raise ApiCommunicationError(f"Invalid JSON from {url}: {preview}") from error
