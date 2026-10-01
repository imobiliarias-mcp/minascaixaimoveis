# ADR 0001: Architecture & Design of Central Rental Research MCP Modules

## Status
Accepted

## Context

The system requires reverse-engineering the rental property search API of **Minas Caixa Imóveis** (`https://www.minascaixaimoveis.com.br/`) and architecting modular Python components intended for integration into a **Central Rental Research MCP (Model Context Protocol)** server.

A central MCP server allows AI assistants and client applications to query multiple real estate platforms (e.g. Casa Linhares, Minas Caixa, Netimóveis, QuintoAndar) through a unified tool contract. To achieve this, the integration must not be a monolithic scraping script, but rather a decoupled, highly cohesive, modular architecture.

Furthermore, the implementation must strictly satisfy:
- **SOLID Principles**
- **Clean Code**
- **Object Calisthenics** (9 strict rules)
- **Design Patterns** (Adapter, Strategy, Value Object, First-Class Collection, Factory)
- **Fail-Fast input validation**
- **Defensive error handling**

---

## Decision

We adopt a **Hexagonal / Ports-and-Adapters Architecture** partitioned into four explicit layers:

```
┌────────────────────────────────────────────────────────┐
│               Central Rental Research MCP              │
│               (Model Context Protocol Tools)           │
└──────────────────────────┬─────────────────────────────┘
                           │ uses Port (Protocol)
                           ▼
┌────────────────────────────────────────────────────────┐
│                   Domain Layer                         │
│  - Value Objects (ListingPrice, PropertyCode, etc.)    │
│  - First-Class Collections (Listings, Facets)          │
│  - Domain Exceptions                                   │
│  - Provider Port Interface (RentalProviderProtocol)    │
└──────────────────────────▲─────────────────────────────┘
                           │ implements Port
┌──────────────────────────┴─────────────────────────────┐
│                 Adapter / Provider Layer               │
│  - MinasCaixaRentalProvider                            │
│  - Adapts Minas Caixa API responses to Domain Entities │
└──────────────────────────┬─────────────────────────────┘
                           │ coordinates
┌──────────────────────────▼─────────────────────────────┐
│                  Infrastructure Layer                  │
│  - MinasCaixaConfiguration                             │
│  - MinasCaixaHttpTransport (fail-fast status checks)   │
│  - MinasCaixaQueryBuilder (guarantees mandatory fields)│
│  - Parsers (SearchResultParser, DetailParser, Facet)   │
└────────────────────────────────────────────────────────┘
```

---

## Object Calisthenics Enforcement Matrix

| Calisthenics Rule | Implementation Strategy in Python |
|:---|:---|
| **1. One level of indentation per method** | Methods with nested branching are refactored into focused private helper methods. |
| **2. Don't use the ELSE keyword** | Replaced with guard clauses, early returns, and polymorphic strategy methods. |
| **3. Wrap all primitives and strings** | Real-world concepts (`ListingPrice`, `PropertyCode`, `GeoCoordinate`) are immutable Value Objects. |
| **4. First-class collections** | Collections (`RentalListingCollection`, `FacetCollection`, `RentalSearchResult`) encapsulate sequencing behaviors. |
| **5. One dot per line** | Deep method and attribute chaining is eliminated; intermediate results are assigned explicitly. |
| **6. Don't abbreviate** | Variable and method names are fully descriptive; abbreviations (`mgr`, `btn`, `res`) are forbidden. |
| **7. Keep all entities small** | Functions ≤ 15 lines, Classes ≤ 100 lines, Modules < 200 lines. |
| **8. No classes with more than two instance variables** | Complex entities are decomposed into cohesive composite objects (e.g. `ListingCore`, `ListingDetails`). |
| **9. No getters/setters/properties exposing internal state** | Objects expose behavioral questions and formatted output methods instead of raw mutated state. |

---

## Consequences

- **Extensibility**: Adding new regional providers (e.g. Casa Linhares, Minas Caixa) requires only implementing `RentalProviderProtocol`.
- **Testability**: Pure domain and builder logic can be tested in sub-millisecond execution times without hitting the network.
- **Resilience**: The query builder guarantees all five mandatory fields required by the portal's backend `Api.php` engine, preventing fatal HTTP 500 errors.
