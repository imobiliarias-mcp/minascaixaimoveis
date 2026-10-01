"""Domain primitive value objects for rental research."""

from dataclasses import dataclass
from minascaixa.domain.exceptions import ValidationError


@dataclass(frozen=True)
class PropertyCode:
    """Encapsulates a valid unique property identifier."""

    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValidationError(f"Property code must be positive: {self.value}")

    def as_string(self) -> str:
        """Returns string representation of property code."""
        return str(self.value)


@dataclass(frozen=True)
class PageNumber:
    """Encapsulates a 1-indexed pagination number."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValidationError(f"Page number must be at least 1: {self.value}")

    def as_string(self) -> str:
        """Returns string representation of page number."""
        return str(self.value)


@dataclass(frozen=True)
class RentalPrice:
    """Encapsulates a rental monetary amount in Brazilian Reais."""

    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0.0:
            raise ValidationError(f"Rental price cannot be negative: {self.amount}")

    def as_integer_string(self) -> str:
        """Returns integer string for query parameter encoding."""
        return str(int(self.amount))


@dataclass(frozen=True)
class CitySlug:
    """Encapsulates a normalized city identifier slug."""

    value: str

    def __post_init__(self) -> None:
        cleaned_value = self.value.strip()
        if not cleaned_value:
            raise ValidationError("City slug cannot be blank")

    def normalized(self) -> str:
        """Returns normalized lowercase city slug."""
        return self.value.strip().lower()


@dataclass(frozen=True)
class SortOrder:
    """Encapsulates supported result sorting preferences."""

    value: str

    def __post_init__(self) -> None:
        allowed = {"valordesc", "valorasc", ""}
        if self.value not in allowed:
            raise ValidationError(f"Unsupported sort order: {self.value}")

    @classmethod
    def price_descending(cls) -> "SortOrder":
        """Sort by highest price first."""
        return cls("valordesc")

    @classmethod
    def price_ascending(cls) -> "SortOrder":
        """Sort by lowest price first."""
        return cls("valorasc")

    @classmethod
    def default(cls) -> "SortOrder":
        """Use portal default ordering."""
        return cls("")
