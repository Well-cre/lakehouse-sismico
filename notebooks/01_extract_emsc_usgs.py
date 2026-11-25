# Databricks notebook source
FONTES = {

    "usgs": {
        "api": "https://earthquake.usgs.gov/fdsnws/event/1",
        "format": "geojson",
        "ext": "geojson"
    },

    "emsc": {
        "api": "https://www.seismicportal.eu/fdsnws/event/1",
        "format": "json",
        "ext": "json"
    }

}


# COMMAND ----------

import time
import requests
import json

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
        "limit": 1
    },
    timeout=30
)

print("Status:", r.status_code)

dados = r.json()

print("Chaves do topo:")
print(dados.keys())

print()
print(json.dumps(dados, indent=2)[:3000])

# COMMAND ----------

def chamar(api_base, endpoint, params, tentativas=5):

    for i in range(tentativas):

        r = requests.get(
            f"{api_base}/{endpoint}",
            params=params,
            timeout=60
        )

        if r.status_code == 429 or r.status_code >= 500:
            print(
                f"{r.status_code} em /{endpoint}, "
                f"tentando novamente"
            )

            time.sleep(2 ** i)
            continue

        r.raise_for_status()

        return r

    r.raise_for_status()

# COMMAND ----------

r = chamar(
    "https://www.seismicportal.eu/fdsnws/event/1",
    "count",
    {
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5
    }
)

print(r.status_code)
print(r.json())

# COMMAND ----------

import os

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5
    }
)

destino = "/Volumes/sismos/bronze/landing/emsc/ano=2025/mes=07.json"

os.makedirs(
    os.path.dirname(destino),
    exist_ok=True
)

with open(destino, "wb") as f:
    f.write(r.content)

print("arquivo gravado")

# COMMAND ----------

def obter_count(api_base, formato, janela):

    r = chamar(
        api_base,
        "count",
        {
            **janela,
            "format": formato
        }
    )

    dados = r.json()

    return int(dados["count"])

# COMMAND ----------

# DBTITLE 1,janela_do_mes
def janela_do_mes(ano, mes):

    inicio = f"{ano}-{mes:02d}-01"

    fim = (
        f"{ano + 1}-01-01"
        if mes == 12
        else f"{ano}-{mes + 1:02d}-01"
    )

    return {
        "starttime": inicio,
        "endtime": fim,
        "minmagnitude": 2.5,
        "orderby": "time-asc"
    }

# COMMAND ----------

def extrair_mes(fonte, ano, mes):

    cfg = FONTES[fonte]

    janela = janela_do_mes(
        ano,
        mes
    )

    quantidade = obter_count(
        cfg["api"],
        cfg["format"],
        janela
    )

    resposta = chamar(
        cfg["api"],
        "query",
        {
            **janela,
            "format": cfg["format"]
        }
    )

    destino = (
        f"/Volumes/sismos/bronze/landing/"
        f"{fonte}/"
        f"ano={ano}/"
        f"mes={mes:02d}.{cfg['ext']}"
    )

    os.makedirs(
        os.path.dirname(destino),
        exist_ok=True
    )

    with open(destino, "wb") as f:
        f.write(resposta.content)

    return quantidade

# COMMAND ----------

def extrair_fonte(fonte, ano):

    total = 0

    for mes in range(1, 13):

        eventos = extrair_mes(
            fonte,
            ano,
            mes
        )

        total += eventos

        print(
            f"{fonte} "
            f"{ano}-{mes:02d}: "
            f"{eventos}"
        )

    print(
        f"TOTAL {fonte}: "
        f"{total}"
    )

# COMMAND ----------

dbutils.widgets.text("ano", "2025")
ANO = int(dbutils.widgets.get("ano"))

extrair_fonte("usgs", ANO)

extrair_fonte("emsc", ANO)