"""Domain exceptions for the rental research MCP."""


class MinasCaixaError(Exception):
    """Base exception for all rental research domain errors."""


class ValidationError(MinasCaixaError):
    """Raised when an input value violates domain boundary validation."""


class ApiCommunicationError(MinasCaixaError):
    """Raised when an HTTP operation fails or returns invalid status."""


class PropertyNotFoundError(MinasCaixaError):
    """Raised when a requested property code does not exist."""


class InvalidFilterError(MinasCaixaError):
    """Raised when provided filter criteria are mutually contradictory or invalid."""
