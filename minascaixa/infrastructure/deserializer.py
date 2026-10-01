"""Deserializes raw JSON responses into domain models and collections."""

from typing import Any, Dict, List
from minascaixa.domain.primitives import PropertyCode
from minascaixa.domain.models import (
    PropertyIdentity,
    PropertyLocation,
    PropertyCore,
    PropertyPricing,
    PropertyFeatures,
    PropertyProfile,
    PropertySummary,
)
from minascaixa.domain.collections import (
    PropertyCollection,
    CityItem,
    CityCollection,
    NeighborhoodItem,
    NeighborhoodCollection,
)


class ResponseDeserializer:
    """Transforms raw API responses into domain collections and entities."""

    def deserialize_search_results(self, data: Dict[str, Any]) -> PropertyCollection:
        """Parses property listing items into a PropertyCollection."""
        raw_list = data.get("lista", [])
        summaries = [self._deserialize_single_summary(item) for item in raw_list]
        return PropertyCollection(tuple(summaries))

    def _deserialize_single_summary(self, raw_item: Dict[str, Any]) -> PropertySummary:
        core = self._build_property_core(raw_item)
        profile = self._build_property_profile(raw_item)
        return PropertySummary(core=core, profile=profile)

    def _build_property_core(self, item: Dict[str, Any]) -> PropertyCore:
        code_number = int(item.get("codigo", 0))
        code = PropertyCode(code_number)
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
