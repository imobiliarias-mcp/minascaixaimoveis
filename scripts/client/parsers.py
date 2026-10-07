"""Parsers converting raw Minas Caixa JSON responses into domain entities."""

import re
from typing import Any, Dict, List
from urllib.parse import urlsplit
from scripts.domain.value_objects import ListingPrice, PropertyCode
from scripts.domain.entities import (
    ListingIdentity,
    ListingValuation,
    ListingCore,
    ListingDetails,
    RentalListing,
    DetailedProfile,
    RentalPropertyDetail,
)
from scripts.domain.collections import (
    RentalListingCollection,
    RentalSearchResult,
    FacetCollection,
)
from scripts.domain.exceptions import (
    InvalidPropertyCodeException,
    PropertyNotFoundException,
)


class SearchResultParser:
    """Parses property search response payloads into RentalSearchResult."""

    def __init__(
        self, public_base_url: str = "https://www.minascaixaimoveis.com.br"
    ) -> None:
        """Validate the public portal base used for property links."""
        parsed_url = urlsplit(public_base_url.strip())
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("Public base URL must use HTTP(S) and include a host")
        if parsed_url.query or parsed_url.fragment:
            raise ValueError("Public base URL cannot contain a query or fragment")
        self._public_base_url = public_base_url.rstrip("/")

    def _validated_property_code(self, raw_code: Any) -> PropertyCode:
        code_string = str(raw_code).strip() if isinstance(raw_code, (str, int)) else ""
        if not re.fullmatch(r"[0-9]+", code_string) or int(code_string) <= 0:
            raise InvalidPropertyCodeException(
                f"Invalid codigo for public property URL: {raw_code!r}"
            )
        return PropertyCode(code_string)

    def _parse_price_float(self, raw_price_string: str) -> float:
        cleaned = re.sub(r"[^\d,]", "", str(raw_price_string))
        normalized = cleaned.replace(",", ".")
        if not normalized:
            return 0.0
        return float(normalized)

    def _build_core(self, item: Dict[str, Any]) -> ListingCore:
        code_vo = self._validated_property_code(item.get("codigo"))
        title_string = str(item.get("titulo", ""))
        identity = ListingIdentity(code=code_vo, title=title_string)
        price_amount = self._parse_price_float(item.get("valor", "0"))
        price_vo = ListingPrice(price_amount)
        property_type = str(item.get("tipo", "Imóvel"))
        condo_amount = self._parse_price_float(item.get("valorcondominio", "0"))
        condo_fee = condo_amount if condo_amount > 0.0 else None
        valuation = ListingValuation(
            rental_price=price_vo, property_type=property_type, condo_fee=condo_fee
        )
        return ListingCore(identity=identity, valuation=valuation)

    def _build_details(self, item: Dict[str, Any], property_code: str) -> ListingDetails:
        neighborhood = str(item.get("bairro", ""))
        city = str(item.get("cidade", ""))
        location = f"{neighborhood}, {city}" if neighborhood and city else city
        cover_url = str(item.get("urlfotoprincipalp", ""))
        public_url = f"{self._public_base_url}/detalhe-imovel/{property_code}"
        return ListingDetails(
            location_summary=location,
            media_url=cover_url,
            public_url=public_url,
        )

    def _extract_single_listing(self, item: Dict[str, Any]) -> RentalListing:
        core = self._build_core(item)
        property_code = core.identity.code.value()
        details = self._build_details(item, property_code)
        return RentalListing(core=core, details=details)

    def parse_search_response(self, response_data: Dict[str, Any]) -> RentalSearchResult:
        """Parse complete search response dictionary."""
        raw_items = response_data.get("lista", [])
        total_count = int(response_data.get("quantidade", len(raw_items)))
        parsed_listings = [self._extract_single_listing(item) for item in raw_items]
        collection = RentalListingCollection(listings=tuple(parsed_listings))
        return RentalSearchResult(
            collection=collection, total_listings_count=total_count
        )


class PropertyDetailParser:
    """Parses raw property detail payload into RentalPropertyDetail."""

    def __init__(
        self, public_base_url: str = "https://www.minascaixaimoveis.com.br"
    ) -> None:
        """Configure public URLs for a property detail response."""
        self._search_parser = SearchResultParser(public_base_url)

    def parse_detail_response(self, response_data: Dict[str, Any]) -> RentalPropertyDetail:
        """Extract full details from single property API response."""
        raw_list = response_data.get("lista", [])
        if not raw_list:
            raise PropertyNotFoundException("Property record not found in response")
        item = raw_list[0]
        listing = self._search_parser._extract_single_listing(item)
        description = str(item.get("descricao", item.get("metadescription", "")))
        amenities = self._extract_amenities_summary(item)
        profile = DetailedProfile(description=description, amenities_summary=amenities)
        return RentalPropertyDetail(listing=listing, profile=profile)

    def _extract_amenities_summary(self, item: Dict[str, Any]) -> str:
        features: List[str] = []
        bedrooms = str(item.get("numeroquartos", "0"))
        features.append(f"{bedrooms} quartos")
        bathrooms = str(item.get("numerobanhos", "0"))
        features.append(f"{bathrooms} banheiros")
        vagas = str(item.get("numerovagas", "0"))
        features.append(f"{vagas} vagas")
        area = str(item.get("areainterna", "0"))
        features.append(f"{area} m²")
        return ", ".join(features)


class FacetParser:
    """Parses cities and neighborhoods lists into FacetCollection."""

    def parse_facets(
        self, cities_raw: List[Dict[str, Any]], neighborhoods_raw: List[Dict[str, Any]]
    ) -> FacetCollection:
        """Assembles cities and neighborhoods into unified FacetCollection."""
        city_names = tuple(str(c.get("nomeOriginal", "")) for c in cities_raw if c.get("nomeOriginal"))
        bairro_names = tuple(str(b.get("nomeOriginal", "")) for b in neighborhoods_raw if b.get("nomeOriginal"))
        facet_map = {
            "cities": city_names,
            "neighborhoods": bairro_names,
        }
        return FacetCollection(facet_map=facet_map)
