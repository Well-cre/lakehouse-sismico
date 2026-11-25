# Databricks notebook source
import requests

r = requests.get(
    "https://earthquake.usgs.gov/fdsnws/event/1/count",
    params={
        "format": "geojson",
        "starttime": "2025-07-01", "endtime": "2025-08-01",
        "minmagnitude": 2.5,
    },
    timeout=30,
)
print(r.status_code, r.json())