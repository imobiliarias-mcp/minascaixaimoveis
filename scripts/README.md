# Central Rental Research MCP — Minas Caixa Module

This package implements the **Minas Caixa Imóveis** rental search provider designed as a plug-and-play adapter for a **Central Rental Research MCP (Model Context Protocol)** server.

---

## 1. Architectural Highlights

- **SOLID Principles**: Single responsibility classes, interface segregation, dependency inversion.
- **Strict Object Calisthenics**:
  - One indent level per method.
  - Zero `else` keywords (guard clauses and polymorphism only).
  - Wrapped primitives (Value Objects for prices, coordinates, filters).
  - First-class collections (`RentalListingCollection`, `FacetCollection`, `RentalSearchResult`).
  - One dot per line (intermediate assigned variables).
  - No abbreviations.
  - Entities size limits: functions ≤ 15 lines, classes ≤ 100 lines, modules < 200 lines.
  - ≤ 2 instance variables per class.
  - Tell, Don't Ask encapsulation.
- **Design Patterns**: Adapter, Strategy, Builder, Value Object, First-Class Collection, Factory.
- **Fail Fast**: Immediate boundary validation on inputs, raising descriptive typed domain exceptions.

---

## 2. Directory Layout

```
scripts/
├── README.md               # Package overview and developer instructions
├── ARCHITECTURE.md         # Calisthenics & SOLID design adherence documentation
├── USAGE.md                # Usage examples and MCP integration guide
├── research-plan.md        # Research plan, execution logs, and empirical test matrix
├── __init__.py
├── domain/                 # Pure domain layer
│   ├── __init__.py
│   ├── exceptions.py       # Domain exception hierarchy
│   ├── value_objects.py    # Immutable value objects (ListingPrice, PropertyCode, GeoCoordinate)
│   ├── criteria.py         # Search criteria, price ranges, and RentalFilter
│   ├── entities.py         # Domain models (RentalListing, PropertyDetail)
│   └── collections.py      # First-class collections (RentalListingCollection, FacetCollection)
├── interfaces/             # Port contracts (MCP Provider Protocols)
│   ├── __init__.py
│   └── provider.py         # RentalProviderProtocol interface
├── client/                 # Infrastructure & Minas Caixa HTTP client
│   ├── __init__.py
│   ├── configuration.py    # Minas Caixa client configuration
│   ├── http_transport.py   # HTTP transport
│   ├── query_builder.py    # Filter-to-query form payload translator
│   └── parsers.py          # Response parsers
├── providers/              # Adapter layer
│   ├── __init__.py
│   └── minascaixa.py       # MinasCaixaRentalProvider implementation
├── mcp/                    # MCP tool contracts & handlers
│   ├── __init__.py
│   └── tools.py            # Central Rental Research MCP tools
├── run_search.py           # CLI tool to run rental searches
├── run_property_detail.py  # CLI tool to fetch full property details
├── run_facets.py           # CLI tool to list search facets
└── run_tests.py            # Full test suite runner
```

---

## 3. Quickstart CLI Runners

### Run Complete Test Suite
```bash
python3 scripts/run_tests.py
```

### Search Rentals
```bash
python3 scripts/run_search.py --city timoteo
python3 scripts/run_search.py --city timoteo --bedrooms 3
```

### View Property Details
```bash
python3 scripts/run_property_detail.py 6161
```

### View Facets
```bash
python3 scripts/run_facets.py
```
