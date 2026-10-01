# Central Rental Research MCP — Usage Guide

This guide illustrates how to use the Minas Caixa rental search module both as a standalone library and as an MCP (Model Context Protocol) tool provider.

---

## 1. Python API Usage

### 1.1 Basic Search
```python
from scripts.providers.minascaixa import MinasCaixaRentalProvider
from scripts.domain.criteria import RentalFilter

provider = MinasCaixaRentalProvider.create_default()

# Search rentals in Timóteo
search_result = provider.search_rentals(RentalFilter().with_city("timoteo"))
print(f"Total found: {search_result.total_count()}")

for listing in search_result.listings():
    print(listing.format_summary())
```

### 1.2 Filtered Search
```python
from scripts.domain.criteria import RentalFilter
from scripts.domain.value_objects import ListingPrice

# Search 3+ bedroom rentals in Timóteo under R$ 5,000/month
criteria = (
    RentalFilter()
    .with_city("timoteo")
    .with_bedrooms(3)
    .with_price_ceiling(ListingPrice(5000.0))
)

result = provider.search_rentals(criteria)
for item in result.listings():
    print(item.format_summary())
```

### 1.3 Fetch Property Details
```python
from scripts.domain.value_objects import PropertyCode

code = PropertyCode("6161")
detail = provider.get_property_detail(code)
print(detail.format_detailed_view())
```

### 1.4 Inspect Available Facets (Cities & Neighborhoods)
```python
facets = provider.get_facets()
print("Cities:", facets.city_names())
print("Neighborhoods:", facets.neighborhood_names())
```

---

## 2. Integrating with a Central Rental Research MCP Server

```python
from scripts.mcp.tools import MinasCaixaMcpAdapter

adapter = MinasCaixaMcpAdapter.create_default()

# Search tool call
results_dict = adapter.search_rentals(
    city="timoteo",
    bedrooms=3,
    max_price=5000.0,
    page=1,
)

# Detail tool call
detail_dict = adapter.get_property_detail(property_code="6161")

# Facets tool call
facets_dict = adapter.get_facets()
```
