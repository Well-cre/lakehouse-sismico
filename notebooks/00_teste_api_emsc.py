# Databricks notebook source
import requests

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/count",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
    },
    timeout=30,
)

print("Status:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Resposta:", r.text[:1000])

# COMMAND ----------

import requests

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
        "limit": 10,
    },
    timeout=30,
)
dados = r.json()

print("URL consultada:", r.url)
print("Total retornado:", len(dados["features"]))
print("Metadata:", dados["metadata"])

print("\nDatas dos eventos:")

for evento in dados["features"]:
    print(evento["properties"]["time"])
    
print("Status:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Resposta:")
print(r.text[:3000])

# COMMAND ----------

import requests

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
        "limit": 10,
        "orderby": "time-asc",
    },
    timeout=30,
)

dados = r.json()

print("Status:", r.status_code)
print("Total retornado:", len(dados["features"]))
print("Metadata:", dados["metadata"])

print("\nDatas dos eventos:")

# COMMAND ----------

for evento in dados["features"]:
    propriedades = evento["properties"]

    print(
        "Data:", propriedades["time"],
        "| Magnitude:", propriedades["mag"],
        "| Região:", propriedades["flynn_region"]
    )


# COMMAND ----------

print("Total informado pelo COUNT:", 7289)

print("Total retornado pelo QUERY:", len(dados["features"]))

print("Limite configurado:", 10)


# COMMAND ----------

import requests

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
        "limit": 7289,
        "orderby": "time-asc",
    },
    timeout=120,
)

print("Status:", r.status_code)

dados = r.json()

print("Total retornado:", len(dados["features"]))
print("Contagem da metadata:", dados["metadata"])

if dados["features"]:
    print("Primeiro evento:", dados["features"][0]["properties"]["time"])
    print("Último evento:", dados["features"][-1]["properties"]["time"])

# COMMAND ----------

import requests

API = "https://www.seismicportal.eu/fdsnws/event/1"

params = {
    "format": "json",
    "starttime": "2025-07-01T00:00:00",
    "endtime": "2025-07-31T23:59:59.999999",
    "minmagnitude": 2.5,
}

# Primeiro: contar
r_count = requests.get(f"{API}/count", params=params, timeout=30)
r_count.raise_for_status()
total = r_count.json()["count"]

# Segundo: consultar os eventos
params_query = {
    **params,
    "limit": total,
    "orderby": "time-asc",
}

r_query = requests.get(f"{API}/query", params=params_query, timeout=120)
r_query.raise_for_status()
dados = r_query.json()

features = dados["features"]

print("Total do count:", total)
print("Total retornado:", len(features))
print("Metadata:", dados["metadata"])

if features:
    print("Primeiro evento:", features[0]["properties"]["time"])
    print("Último evento:", features[-1]["properties"]["time"])

# COMMAND ----------

import requests

API_EMSC = "https://www.seismicportal.eu/fdsnws/event/1"

PARAMS_BASE = {
    "format": "json",
    "start": "2025-07-01",
    "end": "2025-08-01",
    "minmag": 2.5,
    "orderby": "time-asc",
}

cliente = requests.Session()
cliente.headers.update({"User-Agent": "LakehouseSismico/1.0"})

print("API_EMSC =", API_EMSC)
print("PARAMS_BASE =", PARAMS_BASE)

teste = cliente.get(
    f"{API_EMSC}/query",
    params={
        **PARAMS_BASE,
        "limit": 1
    }
)

print("Status:", teste.status_code)

dados = teste.json()

print("Tipo:", dados.get("type"))
print("Features:", len(dados.get("features", [])))
print("Metadata:", dados.get("metadata"))

# COMMAND ----------

variaveis = [
    "API_EMSC",
    "PARAMS_BASE",
    "cliente",
    "TIMEOUT",
    "TENTATIVAS",
    "ESPERA_INICIAL"
]

for nome in variaveis:
    print(
        f"{nome}:",
        "OK" if nome in globals() else "NÃO ENCONTRADA"
    )

# COMMAND ----------

# Verificar se existe notebook atual carregado
print("Sessão ativa.")

# Mostrar informações básicas do ambiente
import sys

print("Python:", sys.version)