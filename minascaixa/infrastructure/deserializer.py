"""Deserializes raw JSON responses into domain models and collections."""

import re
from typing import Any, Dict, List
from urllib.parse import urlsplit

from minascaixa.domain.collections import (
    CityCollection,
    CityItem,
    NeighborhoodCollection,
    NeighborhoodItem,
    PropertyCollection,
)
from minascaixa.domain.exceptions import ValidationError
from minascaixa.domain.models import (
    PropertyCore,
    PropertyFeatures,
    PropertyIdentity,
    PropertyLocation,
    PropertyNavigation,
    PropertyPricing,
    PropertyProfile,
    PropertySummary,
)
from minascaixa.domain.primitives import PropertyCode


class ResponseDeserializer:
    """Transforms raw API responses into domain collections and entities."""

    def __init__(
        self,
        public_base_url: str = "https://www.minascaixaimoveis.com.br",
    ) -> None:
        """Configure and validate the base used for public property links."""
        parsed_url = urlsplit(public_base_url.strip())
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValidationError("Public base URL must use HTTP(S) and include a host")
        if parsed_url.query or parsed_url.fragment:
            raise ValidationError("Public base URL cannot contain a query or fragment")
        self._public_base_url = public_base_url.rstrip("/")

    def deserialize_search_results(self, data: Dict[str, Any]) -> PropertyCollection:
        """Parses property listing items into a PropertyCollection."""
        raw_list = data.get("lista", [])
        summaries = [self._deserialize_single_summary(item) for item in raw_list]
        return PropertyCollection(tuple(summaries))

    def _deserialize_single_summary(self, raw_item: Dict[str, Any]) -> PropertySummary:
        core = self._build_property_core(raw_item)
        profile = self._build_property_profile(raw_item)
        code = core.identity.code.as_string()
        public_url = f"{self._public_base_url}/detalhe-imovel/{code}"
        navigation = PropertyNavigation(url=public_url)
        return PropertySummary(core=core, profile=profile, navigation=navigation)

    def _validated_property_code(self, raw_code: Any) -> PropertyCode:
        code_string = str(raw_code).strip() if isinstance(raw_code, (str, int)) else ""
        if not re.fullmatch(r"[0-9]+", code_string):
            raise ValidationError(f"Invalid codigo for public property URL: {raw_code!r}")
        code_number = int(code_string)
        if code_number <= 0:
            raise ValidationError(f"Invalid codigo for public property URL: {raw_code!r}")
        return PropertyCode(code_number)

    def _build_property_core(self, item: Dict[str, Any]) -> PropertyCore:
        code = self._validated_property_code(item.get("codigo"))
        title = str(item.get("titulo", ""))
        identity = PropertyIdentity(code=code, title=title)
        city = str(item.get("cidade", ""))
        neighborhood = str(item.get("bairro", ""))
        location = PropertyLocation(city=city, neighborhood=neighborhood)
        return PropertyCore(identity=identity, location=location)

    def _build_property_profile(self, item: Dict[str, Any]) -> PropertyProfile:
        rental_val = str(item.get("valor", "R$ 0,00"))
        condo_val = str(item.get("valorcondominio", "R$ 0,00"))
        pricing = PropertyPricing(rental_value=rental_val, condo_fee=condo_val)
        rooms = str(item.get("numeroquartos", "0"))
        area = str(item.get("areainterna", "0"))
        features = PropertyFeatures(rooms_summary=rooms, area_summary=area)
        return PropertyProfile(pricing=pricing, features=features)

    def deserialize_cities(self, raw_cities: List[Dict[str, Any]]) -> CityCollection:
        """Parses raw cities array into a CityCollection."""
        items = [
            CityItem(code=int(c.get("codigo", 0)), name=str(c.get("nomeOriginal", "")))
            for c in raw_cities
        ]
        return CityCollection(tuple(items))

    def deserialize_neighborhoods(
        self, raw_neighborhoods: List[Dict[str, Any]]
    ) -> NeighborhoodCollection:
        """Parses raw neighborhoods array into a NeighborhoodCollection."""
        items = [
            NeighborhoodItem(
                code=int(b.get("codigo", 0)), name=str(b.get("nomeOriginal", ""))
            )
            for b in raw_neighborhoods
        ]
        return NeighborhoodCollection(tuple(items))
