from fastapi import FastAPI
import json
from statistics import mean
import numpy as np

app = FastAPI()

with open("q-vercel-latency.json") as f:
    DATA = json.load(f)

@app.post("/")
def analytics(body: dict):
    regions = body["regions"]
    threshold = body["threshold_ms"]

    result = {}

    for region in regions:
        records = [r for r in DATA if r["region"] == region]
        lat = [r["latency_ms"] for r in records]
        up = [r["uptime_pct"] for r in records]

        result[region] = {
            "avg_latency": round(mean(lat),2),
            "p95_latency": round(float(np.percentile(lat,95)),2),
            "avg_uptime": round(mean(up),2),
            "breaches": sum(1 for x in lat if x > threshold)
        }

    return result