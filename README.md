# Minas Caixa Imóveis - Rental Research MCP Module

Reverse-engineered API integration and domain module boundary for the rental search system of Minas Caixa Imóveis (`minascaixaimoveis.com.br`).

## 1. Scope & Capabilities

- **Rental Search & Listing**: Reverse-engineered client-side AJAX endpoint (`POST /imoveis/ajax/`).
- **Filter Discovery**: Endpoints for cities (`/cidadeAjax`), neighborhoods (`/bairroAjax`), property types (`/tipoAjax`), and condominiums (`/condominios`).
- **Pagination Mechanics**: 20 items per page, 1-indexed page parameter, total count tracking.
- **Full Property Detail Retrieval**: Batch and single property retrieval (`POST /imoveis/codigos/`) returning 219 attributes per property.
- **Unauthenticated**: No authentication, tokens, or cookies required for rental listing and research.

## 2. Architecture & Design Principles

Designed as the central Rental Research MCP boundary interface adhering to:
- **Priority**: Correctness first, modularity second, style principles third.
- **SOLID & Clean Code**: Single responsibility, clear ports and adapters, explicit interfaces.
- **Object Calisthenics**:
  - One indent level per method.
  - No `else` statements (guard clauses, early returns, polymorphism).
  - Domain primitive wrapping (`PropertyCode`, `RentalPrice`, `PageNumber`, `CitySlug`, `SortOrder`).
  - First-class collections (`PropertyCollection`, `CityCollection`, `NeighborhoodCollection`).
  - One dot per line.
  - No abbreviations.
  - Entities kept small (functions ≤ 15 lines, classes ≤ 100 lines, modules < 200 lines).
  - Maximum 2 instance variables per class.

## 3. Directory Layout

```text
├── docs/
│   └── api-research.md          # Comprehensive reverse-engineered API documentation
├── scripts/
│   ├── research-plan.md         # Research plan, empirical test matrix, and findings log
│   └── run_research.py          # Verification and execution runner script
├── minascaixa/                  # Reusable Python package (MCP module boundary)
│   ├── __init__.py              # Factory and public API exports
│   ├── domain/                  # Value objects, models, collections, and exceptions
│   │   ├── exceptions.py
│   │   ├── primitives.py
│   │   ├── models.py
│   │   └── collections.py
│   ├── infrastructure/          # HTTP transport, endpoints, payload builder, deserializer
│   │   ├── endpoints.py
│   │   ├── http_transport.py
│   │   ├── payload_builder.py
│   │   └── deserializer.py
│   └── application/             # Interfaces, URL parser, and RentalResearchService facade
│       ├── interfaces.py
│       ├── url_parser.py
│       └── service.py
├── tests/                       # Unit and live integration test suite
│   ├── test_domain_primitives.py
│   ├── test_url_parser.py
│   ├── test_payload_builder.py
│   ├── test_deserializer.py
│   ├── test_service_mock.py
│   └── test_live_integration.py
└── requirements.txt             # Frozen dependencies
```

## 4. Quickstart

### Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running Verification Script
```bash
python scripts/run_research.py
```

### Running Test Suite
```bash
pytest -v
```
