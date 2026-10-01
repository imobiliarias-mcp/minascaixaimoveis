# Minas Caixa Imóveis — Rental API Reverse Engineering Documentation

Welcome to the reverse-engineering and architecture documentation for **Minas Caixa Imóveis** (`https://www.minascaixaimoveis.com.br/`).

This repository contains the reverse-engineered API specifications, architectural decision records, and clean, modular Python components designed for integration into a **Central Rental Research MCP (Model Context Protocol)** server.

---

## Documentation Structure

- **[Single Source of Truth API Specification](file:///home/samuelcaldas/repos/imobiliarias/minascaixaimoveis/docs/sot/minascaixa_api_spec.md)** (`docs/sot/minascaixa_api_spec.md`):
  Comprehensive contract specification for all endpoints, headers, payload schemas, query matrices, and boundary validation rules.

- **[Architecture Decision Record 0001](file:///home/samuelcaldas/repos/imobiliarias/minascaixaimoveis/docs/adr/0001-rental-search-mcp-module-design.md)** (`docs/adr/0001-rental-search-mcp-module-design.md`):
  Detailed rationale on Ports-and-Adapters (Hexagonal) architecture, SOLID principles, Design Patterns, and strict Object Calisthenics enforcement.

- **[API Reference & Quick Recipes](file:///home/samuelcaldas/repos/imobiliarias/minascaixaimoveis/docs/api_reference.md)** (`docs/api_reference.md`):
  Developer reference featuring ready-to-run `curl` commands, parameter dictionaries, and implementation tips.

- **[Reverse-Engineering Research Findings](file:///home/samuelcaldas/repos/imobiliarias/minascaixaimoveis/docs/api-research.md)** (`docs/api-research.md`):
  In-depth research notes on DOM analysis, JavaScript deconstruction, and upstream CRM mechanics.

- **[Scripts & MCP Module Guide](file:///home/samuelcaldas/repos/imobiliarias/minascaixaimoveis/scripts/README.md)** (`scripts/README.md`):
  Developer guide for running the Python modules, CLI utilities, and MCP tool handlers.

---

## Key Technical Discoveries Summary

| Dimension | Discovery |
|:---|:---|
| **Underlying Platform** | Custom PHP/Apache web application integrated with Imoview CRM |
| **API Host** | `https://www.minascaixaimoveis.com.br` |
| **Search Endpoint** | `POST /imoveis/ajax/` (URL-encoded form body) |
| **Mandatory Parameters** | `imovel[finalidade]=aluguel`, `imovel[valorde]=0`, `imovel[valorate]=0`, `imovel[pagina]=1`, `imovel[codigocondominio]=0` |
| **Property Detail Endpoint** | `POST /imoveis/codigos/` (`codigo=6161`, returns 219 attributes) |
| **Cities Endpoint** | `POST /cidadeAjax` (26 cities) |
| **Neighborhoods Endpoint** | `POST /bairroAjax` (`cidade=timoteo`, 132 localities) |
| **Authentication Requirement** | None (public endpoints, no auth tokens, cookies, or origin checks needed) |
| **Pagination Model** | 20 items per page, 1-indexed page parameter, total count in `quantidade` |
