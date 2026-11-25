# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

def carregar_bronze(fonte):

    landing = (
        f"/Volumes/sismos/bronze/landing/{fonte}"
    )

    ckpt = (
        f"/Volumes/sismos/bronze/checkpoints/{fonte}_raw"
    )

    tabela = (
        f"sismos.bronze.{fonte}_raw"
    )

    consulta = (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("multiLine", "true")
            .option(
                "cloudFiles.inferColumnTypes",
                "true"
            )
            .option(
                "cloudFiles.schemaLocation",
                f"{ckpt}/_schema"
            )
            .option(
                "cloudFiles.partitionColumns",
                "ano"
            )
            .load(landing)

            .withColumn(
                "_ingested_at",
                F.current_timestamp()
            )

            .withColumn(
                "_source_file",
                F.col("_metadata.file_path")
            )

        .writeStream
            .option(
                "checkpointLocation",
                ckpt
            )
            .trigger(
                availableNow=True
            )
            .toTable(tabela)
    )

    consulta.awaitTermination()


# COMMAND ----------

carregar_bronze("usgs")

# COMMAND ----------

carregar_bronze("emsc")

# COMMAND ----------

# teste da estrutura da API EMSC
import requests

r = requests.get(
    "https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "starttime": "2025-07-01",
        "endtime": "2025-08-01",
        "minmagnitude": 2.5,
        "limit": 1
    }
)

print(r.json())