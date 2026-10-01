"""Verification and research runner script for Minas Caixa rental search MCP."""

import sys
from minascaixa import (
    create_rental_research_service,
    FrontendUrlParser,
    PropertyCode,
    PageNumber,
    PaginationSpec,
    SortOrder,
)

TARGET_SEARCH_URL = (
    "https://www.minascaixaimoveis.com.br/aluguel/imoveis/timoteo/todos-os-bairros/"
    "0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios"
    "?valorminimo=0&valormaximo=0&pagina=1"
)


def run_target_search(service, target_url: str):
    """Executes search for target URL and prints results summary."""
    print("=" * 60)
    print(f"Target URL: {target_url}\n")
    total_count, collection = service.search_by_url(target_url)
    print(f"Total matching rentals found: {total_count}")
    print(f"Items on Page 1: {collection.count()}\n")
    _display_sample_properties(collection)
    return total_count, collection


def _display_sample_properties(collection):
    print("Sample Properties (first 3):")
    for index, prop in enumerate(collection):
        if index >= 3:
            break
        print(f"  [{prop.code().value}] {prop.title()} - {prop.rental_value()}")
    print()


def run_pagination_check(service, target_url: str):
    """Fetches and verifies page 2."""
    parser = FrontendUrlParser()
    criteria, _ = parser.parse_url(target_url)
    page_two_spec = PaginationSpec(
        page_number=PageNumber(2),
        sort_order=SortOrder.price_descending(),
    )
    total, collection_p2 = service.search_rentals(criteria, page_two_spec)
    print(f"Page 2 Count: {collection_p2.count()} items (Total matching: {total})")
    _display_sample_properties(collection_p2)


def run_detail_verification(service, sample_code_value: int):
    """Retrieves and displays detailed attributes for a property."""
    print("=" * 60)
    print(f"Fetching full details for Property Code: {sample_code_value}")
    code = PropertyCode(sample_code_value)
    details = service.get_property_detail(code)
    print(f"Total attributes returned: {len(details)}")
    print(f"  Tipo: {details.get('tipo')}")
    print(f"  Bairro: {details.get('bairro')}")
    print(f"  Cidade: {details.get('cidade')}")
    print(f"  Valor: {details.get('valor')}")
    print(f"  Condomínio: {details.get('valorcondominio')}")
    print(f"  IPTU: {details.get('valoriptu')}")
    print(f"  Área Interna: {details.get('areainterna')} m²")
    print(f"  Quartos: {details.get('numeroquartos')}")
    print(f"  Banheiros: {details.get('numerobanhos')}")
    print(f"  Vagas: {details.get('numerovagas')}")
    print(f"  Fotos: {len(details.get('fotos', []))} images\n")


def run_filter_metadata(service):
    """Fetches and prints cities and neighborhoods summary."""
    print("=" * 60)
    cities = service.get_cities()
    print(f"Available Cities Count: {cities.count()}")
    from minascaixa.domain.primitives import CitySlug

    bairros = service.get_neighborhoods(CitySlug("timoteo"))
    print(f"Neighborhoods in Timóteo Count: {bairros.count()}\n")


def main() -> int:
    """Main verification routine."""
    service = create_rental_research_service(timeout_seconds=20)
    total_count, collection = run_target_search(service, TARGET_SEARCH_URL)
    run_pagination_check(service, TARGET_SEARCH_URL)

    if not collection.is_empty():
        sample_code = collection.first().code().value
        run_detail_verification(service, sample_code)

    run_filter_metadata(service)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
