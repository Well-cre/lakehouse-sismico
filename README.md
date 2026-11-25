# 🌎 Lakehouse Sísmico

Projeto desenvolvido no Databricks utilizando arquitetura Medallion para ingestão, armazenamento e análise de eventos sísmicos provenientes de duas APIs públicas.

## 🎯 Objetivo

Comparar eventos sísmicos registrados por duas instituições independentes:

- 🇺🇸 USGS (United States Geological Survey)
- 🇪🇺 EMSC (European-Mediterranean Seismological Centre)

Além disso, demonstrar o uso de:

- Databricks
- Auto Loader
- Delta Lake
- Streaming Batch (availableNow)
- Landing Zone
- Camada Bronze
- Dashboards Analíticas

---

## 🏗 Arquitetura

```text
USGS API
    ↓
Landing/usgs
    ↓
Bronze/usgs_raw
    ↓
Dashboard

EMSC API
    ↓
Landing/emsc
    ↓
Bronze/emsc_raw
    ↓
Dashboard
```

---

## 📂 Estrutura do Projeto

```text
lakehouse-sismico/

notebooks/
├── 00_teste_api.py
├── 00_teste_apiEU.py
├── 01_extract.py
├── _extract_v2.py
├── 02_bronze.py
├── 02_bronze_EU.py
└── 03_dashboard_usgs_emsc.py
```

---

## 🔧 Tecnologias Utilizadas

- Python
- PySpark
- SQL
- Databricks
- Delta Lake
- Auto Loader
- GitHub

---

## 📊 Resultados Obtidos

| Fonte | Eventos |
|---------|---------:|
| USGS | 29.323 |
| EMSC | 82.254 |

A análise demonstrou diferenças significativas entre os catálogos sísmicos das duas instituições para o mesmo período analisado.

---

## ✅ Validações Realizadas

- Conferência do `/count` das APIs com os dados carregados na Bronze.
- Comparação mensal entre USGS e EMSC.
- Validação do schema inferido pelo Auto Loader.
- Teste de idempotência utilizando checkpoints independentes.
- Verificação do histórico Delta com `DESCRIBE HISTORY`.

---

## 📈 Dashboard

O notebook `03_dashboard_usgs_emsc` contém:

- Comparação mensal USGS × EMSC
- Volume total de eventos
- Diferença mensal entre fontes
- Validação API × Bronze
- Histórico Delta
- Teste de idempotência

---

## 🚀 Autor

Projeto desenvolvido como desafio de Engenharia de Dados utilizando Databricks e arquitetura Lakehouse.