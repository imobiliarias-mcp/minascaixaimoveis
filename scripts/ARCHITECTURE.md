# Central Rental Research MCP Architecture & Design Standards

## 1. Context: Central Rental Research MCP

The **Central Rental Research MCP** aims to unify rental search capabilities across diverse real estate sources (regional portals, agency systems, multi-listing services) in the Vale do Aço and broader regions.

To achieve seamless pluggability, each real estate provider is developed as an isolated module exposing a uniform contract (`RentalProviderProtocol`). The **Minas Caixa Imóveis** module integrates with the underlying **Imoview CRM** while presenting a domain model completely agnostic of Imoview's internal quirks.

---

## 2. Object Calisthenics Compliance

Every file and class in this codebase adheres to the 9 rules of Object Calisthenics:

### Rule 1: Only One Level of Indentation per Method
Methods never nest loops inside conditionals or conditionals inside loops. Complex logic is broken down into concise, single-purpose helper methods.

### Rule 2: Don't Use the `else` Keyword
The `else` keyword is strictly prohibited. Guard clauses with early returns and polymorphic handlers handle branching without `else` branches.

### Rule 3: Wrap All Primitives and Strings
Domain concepts are represented as strongly-typed Value Objects:
- `ListingPrice`: Validates non-negative currency amounts in BRL.
- `PropertyCode`: Validates non-empty string codes.
- `GeoCoordinate`: Validates latitude (-90 to +90) and longitude (-180 to +180).
- `RentalFilter`: Validates search criteria (e.g. `min_price <= max_price`).

### Rule 4: First-Class Collections
Any class holding a collection contains no other instance variables. Collections are wrapped in dedicated domain classes:
- `RentalListingCollection`: Wraps `tuple[RentalListing, ...]`.
- `FacetCollection`: Wraps facet groups (`dict[str, tuple[str, ...]]`).
- `RentalSearchResult`: Wraps `RentalListingCollection` and total count integer.

### Rule 5: One Dot per Line
Chaining multiple method calls (e.g. `obj.a().b().c()`) violates the Law of Demeter. Intermediate variables are explicitly assigned on their own lines.

### Rule 6: Don't Abbreviate
All symbols use descriptive, clear names. Abbreviations such as `res`, `req`, `mgr`, `btn`, `val`, `cur` are avoided in favor of `response`, `request`, `manager`, `button`, `value`, `cursor`.

### Rule 7: Keep All Entities Small
Strict size ceilings:
- Functions and methods: **≤ 15 lines**.
- Classes: **≤ 100 lines**.
- Modules / files: **< 200 lines**.

### Rule 8: No Classes with More Than 2 Instance Variables
Classes declare at most 2 member attributes. Classes with richer state decompose into focused composite value objects or collaborators.

### Rule 9: No Getters / Setters / Properties Exposing Raw State (Tell, Don't Ask)
Objects expose behaviors and formatting methods (`format_brl()`, `format_summary()`, `to_dictionary()`), rather than acting as passive data bags.

---

## 3. SOLID Principles Compliance

1. **Single Responsibility (SRP)**:
   - `MinasCaixaConfiguration`: Endpoint configurations and URL assembly.
   - `MinasCaixaHttpTransport`: HTTP client, headers, and status validation.
   - `MinasCaixaQueryBuilder`: Translates domain filters into wire-format form payloads.
   - `SearchResultParser`: Parses search responses into domain collections.
   - `PropertyDetailParser`: Parses 219 attributes into detailed property views.
   - `FacetParser`: Parses cities and neighborhoods into facet groups.
   - `MinasCaixaRentalProvider`: Coordinates components to fulfill `RentalProviderProtocol`.

2. **Open / Closed (OCP)**:
   - Providers can be added without modifying the core MCP server or existing provider adapters.

3. **Liskov Substitution (LSP)**:
   - `MinasCaixaRentalProvider` implements `RentalProviderProtocol` identically to `CasaLinharesRentalProvider`, allowing drop-in substitution.

4. **Interface Segregation (ISP)**:
   - Segregated into fine-grained capability protocols (`RentalSearchCapability`, `RentalDetailCapability`, `RentalFacetsCapability`) united under `RentalProviderProtocol`.

5. **Dependency Inversion (DIP)**:
   - Providers and MCP adapters depend on domain abstractions and protocols rather than concrete client transports.
