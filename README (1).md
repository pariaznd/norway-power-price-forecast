# Norwegian Electricity Price Forecasting (NO1–NO5)

Predicting tomorrow's hourly electricity prices for Norway's 5 price zones.

**Data:** hourly day-ahead prices, Jan 2023 – Nov 2026, from [hvakosterstrommen.no](https://www.hvakosterstrommen.no)

## Results

Test period: 1 Jul 2025 – 19 Nov 2026. Metric: mean absolute error (MAE), lower is better.

| Model | MAE (NOK/kWh) |
|---|---|
| Baseline: same as yesterday | 0.174 |
| Baseline: same as last week | 0.254 |
| LightGBM, predicting the price | 0.176 |
| LightGBM, predicting the change from yesterday | **0.149** |

The residual LightGBM model is about 15% better than "same as yesterday", and better in all 5 zones.

## How to run

```
pip install -r requirements.txt
python src/download_prices.py
```
Then open `notebooks/01_explore_and_baseline.ipynb`.

## Status

- Done: data download, exploration, baseline and first model
- Next: weather features (MET Norway Frost API), reservoir levels (NVE), Databricks pipeline, FastAPI
