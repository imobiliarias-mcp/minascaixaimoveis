# Minas Caixa API Quick Reference

This document provides quick reference documentation, parameter matrices, and ready-to-execute `curl` recipes for developers integrating Minas Caixa Imóveis rental data.

---

## 1. Quick Recipes (cURL)

### 1.1 Search All Active Rentals in Timóteo (Page 1)
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/imoveis/ajax/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "imovel[finalidade]=aluguel" \
  --data-urlencode "imovel[codigocidade]=timoteo" \
  --data-urlencode "imovel[valorde]=0" \
  --data-urlencode "imovel[valorate]=0" \
  --data-urlencode "imovel[pagina]=1" \
  --data-urlencode "imovel[numeroquartos]=0-quartos" \
  --data-urlencode "imovel[numerovagas]=0-vaga" \
  --data-urlencode "imovel[numerosuite]=0-suite-ou-mais" \
  --data-urlencode "imovel[numerobanhos]=0-banheiro-ou-mais" \
  --data-urlencode "imovel[codigocondominio]=0" \
  --data-urlencode "imovel[ordenacao]=valordesc"
```

### 1.2 Search Rentals with Price & Bedroom Filters
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/imoveis/ajax/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "imovel[finalidade]=aluguel" \
  --data-urlencode "imovel[codigocidade]=timoteo" \
  --data-urlencode "imovel[numeroquartos]=3-quartos" \
  --data-urlencode "imovel[valorde]=2000" \
  --data-urlencode "imovel[valorate]=5000" \
  --data-urlencode "imovel[pagina]=1" \
  --data-urlencode "imovel[codigocondominio]=0"
```

### 1.3 Search Rentals (Page 2)
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/imoveis/ajax/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "imovel[finalidade]=aluguel" \
  --data-urlencode "imovel[codigocidade]=timoteo" \
  --data-urlencode "imovel[valorde]=0" \
  --data-urlencode "imovel[valorate]=0" \
  --data-urlencode "imovel[pagina]=2" \
  --data-urlencode "imovel[codigocondominio]=0"
```

### 1.4 Get Full Property Details by Code
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/imoveis/codigos/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "codigo=6161" \
  --data-urlencode "finalidade=aluguel"
```

### 1.5 Batch Property Details Retrieval
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/imoveis/codigos/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "codigo=6161,7989" \
  --data-urlencode "finalidade=aluguel"
```

### 1.6 Get Available Cities
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/cidadeAjax"
```

### 1.7 Get Available Neighborhoods in Timóteo
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/bairroAjax" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "cidade=timoteo"
```

### 1.8 Get Rental Property Types
```bash
curl -s -X POST "https://www.minascaixaimoveis.com.br/tipoAjax" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "finalidade=aluguel"
```

---

## 2. Parameter Matrix for Rental Searches

| Query Key | Parameter Value | Behavior |
|:---|:---|:---|
| `imovel[finalidade]` | `aluguel` | Required. Filters exclusively for rental listings. |
| `imovel[valorde]` | `0` or integer | Required. Minimum monthly rent budget in BRL. |
| `imovel[valorate]` | `0` or integer | Required. Maximum monthly rent budget (`0` = no maximum). |
| `imovel[pagina]` | `1`, `2`, ... | Required. 1-indexed pagination number. |
| `imovel[codigocondominio]` | `0` | Required. Condominium ID (`0` for all). |
| `imovel[codigocidade]` | `timoteo` | City slug filter. |
| `imovel[numeroquartos]` | `0-quartos`, `1-quartos`, `3-quartos` | Minimum number of bedrooms required. |
| `imovel[numerovagas]` | `0-vaga`, `1-vaga`, `2-vaga` | Minimum number of parking spaces required. |
| `imovel[numerosuite]` | `0-suite-ou-mais`, `1-suites` | Minimum number of suites required. |
| `imovel[numerobanhos]` | `0-banheiro-ou-mais`, `1-banheiro` | Minimum number of bathrooms required. |
| `imovel[ordenacao]` | `valordesc` or `valorasc` | Sort by highest price or lowest price first. |
