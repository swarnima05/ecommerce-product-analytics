# E-Commerce Product Analytics

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![SQLite](https://img.shields.io/badge/SQLite-analytics-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/) [![License](https://img.shields.io/badge/Scope-descriptive%20analytics-6b7280)](#design-decisions)

An end-to-end product analytics case study using Olist's relational Brazilian e-commerce data. It turns normalized marketplace records into defensible revenue, customer-repeat, product, and cohort-retention metrics—answering which products create value, whether customers return, and how those patterns should shape growth priorities.

## Business question

What is driving delivered-order revenue over time, which categories contribute the most value, and how effectively does the marketplace bring customers back after their first purchase? These answers help a product or commercial team distinguish acquisition-led growth from durable customer value and focus merchandising or lifecycle investment accordingly.

## Key metrics & definitions

| Metric | Definition |
|---|---|
| Revenue | Sum of item price + freight for **delivered** orders only. |
| AOV | Mean recognized revenue per delivered order (not per item). |
| Repeat purchase rate | Customers with 2+ delivered orders ÷ customers with at least 1 delivered order. It is not time-windowed. |
| Cohort retention | Share of customers in a first-delivered-purchase-month cohort that placed a delivered order in each later calendar month. |

Cancelled and unavailable orders remain in the database for operational analysis but are excluded from revenue and retention. This avoids treating unfulfilled orders as realized commercial value; it is a conservative and interview-defensible recognition policy.

## Visual output

The committed charts are generated from the reproducible offline sample. Re-run against the real Olist data to refresh them.

![Monthly revenue](reports/figures/monthly_revenue.png)

![Top categories](reports/figures/top_categories.png)

![Cohort retention](reports/figures/cohort_retention.png)

## Key findings & recommendations

This analysis uses the full Olist Brazilian E-Commerce public dataset (~99K orders, Oct 2016–Aug 2018), loaded from Kaggle and run through the project's SQL and Python pipeline.

- Overall AOV is 159.83 BRL, with delivered revenue growing steadily from late 2016 through 2018, stabilizing above 1M BRL/month by mid-2017 onward — compare revenue with AOV each period to see whether growth comes from order volume or basket size.
- Repeat purchase rate is low at 3.0% (2,801 of 93,358 customers placed more than one order) — a real, well-known characteristic of Olist's marketplace, where most sellers see one-time buyers. This suggests retention efforts (post-delivery engagement, loyalty incentives) may have more room for impact than acquisition spend alone.
- beleza_saude (health & beauty) leads all categories by revenue, followed by relogios_presentes and cama_mesa_banho — focus merchandising and seller-quality investigation here, while watching whether revenue share becomes over-concentrated in a few categories.
- Use cohort decay to prioritize post-delivery cross-sell and replenishment journeys where retention drops off fastest.
- Use customer order sequence and running revenue to define repeat-buyer segments and study which first purchases lead to a second order.

## Project structure

```
data/                    download guide; raw source is gitignored
sql/                     documented, executable metric queries
src/                     loading, cleaning, query execution, charting
notebooks/analysis.ipynb narrative walkthrough with rendered outputs
reports/figures/         generated PNGs and standalone interactive HTML
```

## How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Choose one data source
python -m src.generate_sample_data  # offline illustrative data
# Or follow data/download_instructions.md for Kaggle and place CSVs in data/raw

python -m src.load_data
python -m src.clean_data
python -m src.run_queries
python -m src.visualize
jupyter notebook notebooks/analysis.ipynb
```

`run_queries.py` executes the `.sql` assets against SQLite and writes query tables to `reports/query_outputs/`. The raw tables are kept normalized in SQLite; Python's joined order-line fact table is reserved for cleaning and downstream exploration.

## Design decisions

- **SQLite:** a portable, inspectable relational layer that demonstrates joins, aggregations, CTEs, and window functions without requiring infrastructure.
- **Revenue policy:** only delivered orders are recognized; canceled/unavailable records are preserved, but fulfillment did not occur.
- **Window functions:** `ROW_NUMBER()` and cumulative `SUM() OVER()` calculate ordered customer behavior in the database, avoiding fragile reimplementation in pandas.
- **Scope:** descriptive and exploratory analytics only. No claims of causal impact, A/B testing, statistical significance, or predictive modeling are made.

## Data source

Olist Brazilian E-Commerce Public Dataset on Kaggle. Source CSVs are not included in this repository; see [download instructions](data/download_instructions.md).
