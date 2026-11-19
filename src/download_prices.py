"""Download Norwegian electricity prices (NO1-NO5) into one CSV file.

Source: hvakosterstrommen.no (free, no API key).
Run:    pip install requests pandas
        python download_prices.py
Output: data/prices.csv (run from the main project folder) with columns: zone, time_start, NOK_per_kWh, EUR_per_kWh

Faster version:
- downloads 8 files at the same time
- saves each day in raw/ so if you stop and run again, it skips what you already have
"""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

START = date(2023, 1, 1)
END = date.today()
ZONES = ["NO1", "NO2", "NO3", "NO4", "NO5"]
URL = "https://www.hvakosterstrommen.no/api/v1/prices/{y}/{m:02d}-{d:02d}_{zone}.json"
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

session = requests.Session()


def fetch(job):
    day, zone = job
    path = RAW / f"{day}_{zone}.json"
    if path.exists():  # already downloaded before
        return
    url = URL.format(y=day.year, m=day.month, d=day.day, zone=zone)
    try:
        r = session.get(url, timeout=30)
    except requests.RequestException as e:
        print("error:", zone, day, e)
        return
    if r.status_code == 200:
        path.write_text(r.text)
    else:
        print("missing:", zone, day)


jobs = []
day = START
while day <= END:
    jobs += [(day, zone) for zone in ZONES]
    day += timedelta(days=1)

print(f"{len(jobs)} files to check...")
with ThreadPoolExecutor(max_workers=8) as pool:
    for i, _ in enumerate(pool.map(fetch, jobs), 1):
        if i % 500 == 0:
            print(f"{i}/{len(jobs)} done")

# Combine all saved files into one CSV
rows = []
for path in sorted(RAW.glob("*.json")):
    zone = path.stem.split("_")[1]
    for p in json.loads(path.read_text()):
        rows.append({
            "zone": zone,
            "time_start": p["time_start"],
            "NOK_per_kWh": p["NOK_per_kWh"],
            "EUR_per_kWh": p["EUR_per_kWh"],
        })

pd.DataFrame(rows).to_csv("data/prices.csv", index=False)
print("saved", len(rows), "rows to data/prices.csv")
