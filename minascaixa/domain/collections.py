"""First-class collections wrapping sequences with domain behaviors."""

from typing import Iterator, Tuple
from minascaixa.domain.models import PropertySummary


class PropertyCollection:
    """First-class collection of property summaries."""

    def __init__(self, items: Tuple[PropertySummary, ...]) -> None:
        self._items = items

    def __iter__(self) -> Iterator[PropertySummary]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def count(self) -> int:
        """Returns the number of elements in the collection."""
        return len(self._items)

    def is_empty(self) -> bool:
        """Indicates whether collection has zero elements."""
        return len(self._items) == 0

    def first(self) -> PropertySummary:
        """Returns first property summary in collection."""
        if self.is_empty():
            raise IndexError("Collection is empty")
        return self._items[0]


class CityItem:
    """City entry with slug and display name."""

    def __init__(self, code: int, name: str) -> None:
        self._code = code
        self._name = name

    def code(self) -> int:
        """Returns city code."""
        return self._code

    def name(self) -> str:
        """Returns city display name."""
        return self._name


class CityCollection:
    """First-class collection of city items."""

    def __init__(self, items: Tuple[CityItem, ...]) -> None:
        self._items = items

    def __iter__(self) -> Iterator[CityItem]:
        return iter(self._items)

    def count(self) -> int:
        """Returns total cities count."""
        return len(self._items)


class NeighborhoodItem:
    """Neighborhood entry with code and display name."""

    def __init__(self, code: int, name: str) -> None:
        self._code = code
        self._name = name

    def code(self) -> int:
        """Returns neighborhood code."""
        return self._code

    def name(self) -> str:
        """Returns neighborhood display name."""
        return self._name


class NeighborhoodCollection:
    """First-class collection of neighborhood items."""

    def __init__(self, items: Tuple[NeighborhoodItem, ...]) -> None:
        self._items = items

    def __iter__(self) -> Iterator[NeighborhoodItem]:
        return iter(self._items)

    def count(self) -> int:
        """Returns total neighborhoods count."""
        return len(self._items)
