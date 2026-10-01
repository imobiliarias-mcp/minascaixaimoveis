"""Parses website frontend URLs into domain SearchCriteria and PaginationSpec."""

from urllib.parse import urlparse, parse_qs
from typing import Tuple, Dict, List
from minascaixa.domain.primitives import (
    CitySlug,
    PageNumber,
    RentalPrice,
    SortOrder,
)
from minascaixa.domain.models import (
    LocationScope,
    PriceBoundary,
    RoomFilter,
    FilterBundle,
    SearchCriteria,
    PaginationSpec,
)
from minascaixa.domain.exceptions import ValidationError


class FrontendUrlParser:
    """Deconstructs frontend rental search URLs into typed search models."""

    def parse_url(self, url: str) -> Tuple[SearchCriteria, PaginationSpec]:
        """Parses target URL and returns search criteria with pagination."""
        parsed = urlparse(url)
        path_segments = self._extract_clean_segments(parsed.path)
        self._validate_path_segments(path_segments)
        query_params = parse_qs(parsed.query)

        location = self._extract_location(path_segments)
        filters = self._extract_filters(path_segments, query_params)
        pagination = self._extract_pagination(query_params)
        criteria = SearchCriteria(location=location, filters=filters)
        return criteria, pagination

    def _extract_clean_segments(self, path: str) -> List[str]:
        raw_segments = path.strip("/").split("/")
        return [seg for seg in raw_segments if seg]

    def _validate_path_segments(self, segments: List[str]) -> None:
        if len(segments) < 3:
            raise ValidationError(f"URL path contains too few segments: {segments}")
        if segments[0] != "aluguel":
            raise ValidationError(f"Expected rental URL segment 'aluguel', got: {segments[0]}")

    def _extract_location(self, segments: List[str]) -> LocationScope:
        city_raw = segments[2] if len(segments) > 2 else "timoteo"
        city = CitySlug(city_raw)
        return LocationScope(city=city, neighborhood_code=0)

    def _extract_filters(
        self, segments: List[str], query: Dict[str, List[str]]
    ) -> FilterBundle:
        price_bounds = self._extract_price_bounds(query)
        room_filter = self._extract_rooms(segments)
        return FilterBundle(price_bounds=price_bounds, room_filter=room_filter)

    def _extract_price_bounds(self, query: Dict[str, List[str]]) -> PriceBoundary:
        min_raw = query.get("valorminimo", ["0"])[0]
        max_raw = query.get("valormaximo", ["0"])[0]
        min_price = RentalPrice(float(min_raw))
        max_price = RentalPrice(float(max_raw))
        return PriceBoundary(minimum_price=min_price, maximum_price=max_price)

    def _extract_rooms(self, segments: List[str]) -> RoomFilter:
        bedrooms = self._parse_leading_integer(segments, 4)
        parking = self._parse_leading_integer(segments, 6)
        return RoomFilter(bedrooms=bedrooms, parking_spaces=parking)

    def _parse_leading_integer(self, segments: List[str], index: int) -> int:
        if len(segments) <= index:
            return 0
        part = segments[index].split("-")[0]
        if not part.isdigit():
            return 0
        return int(part)

    def _extract_pagination(self, query: Dict[str, List[str]]) -> PaginationSpec:
        page_raw = query.get("pagina", ["1"])[0]
        page_val = int(page_raw) if page_raw.isdigit() else 1
        page_number = PageNumber(page_val)
        sort_order = SortOrder.price_descending()
        return PaginationSpec(page_number=page_number, sort_order=sort_order)
