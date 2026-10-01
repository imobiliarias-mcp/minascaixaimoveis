"""Provider interfaces exports."""

from scripts.interfaces.provider import (
    RentalSearchCapability,
    RentalDetailCapability,
    RentalFacetsCapability,
    RentalProviderProtocol,
)

__all__ = [
    "RentalSearchCapability",
    "RentalDetailCapability",
    "RentalFacetsCapability",
    "RentalProviderProtocol",
]
