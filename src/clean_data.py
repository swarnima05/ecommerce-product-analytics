"""Create a cleaned Python-side order-line fact table; SQL metrics use raw tables."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DATABASE_PATH, PROCESSED_DATA_DIR, REVENUE_ORDER_STATUS

DATE_COLUMNS = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]


def build_order_line_fact(database_path: Path = DATABASE_PATH) -> pd.DataFrame:
    """Join normalized tables, remove duplicate order lines, and standardize datatypes."""
    with sqlite3.connect(database_path) as connection:
        orders = pd.read_sql("SELECT * FROM orders", connection)
        items = pd.read_sql("SELECT * FROM order_items", connection)
        customers = pd.read_sql("SELECT * FROM customers", connection)
        products = pd.read_sql("SELECT * FROM products", connection)
        payments = pd.read_sql("SELECT order_id, SUM(payment_value) AS order_payment_value FROM payments GROUP BY order_id", connection)
    for column in DATE_COLUMNS:
        if column in orders:
            orders[column] = pd.to_datetime(orders[column], utc=True, errors="coerce")
    items = items.drop_duplicates(subset=["order_id", "order_item_id", "product_id"], keep="first")
    fact = (items.merge(orders, on="order_id", how="inner")
                 .merge(customers, on="customer_id", how="left")
                 .merge(products, on="product_id", how="left")
                 .merge(payments, on="order_id", how="left"))
    fact["price"] = pd.to_numeric(fact["price"], errors="coerce").fillna(0.0)
    fact["freight_value"] = pd.to_numeric(fact["freight_value"], errors="coerce").fillna(0.0)
    fact["line_revenue"] = fact["price"] + fact["freight_value"]
    # Keep all statuses for diagnostics; a flag makes the revenue-recognition policy explicit.
    fact["is_revenue_order"] = fact["order_status"].eq(REVENUE_ORDER_STATUS)
    return fact


def save_clean_fact() -> Path:
    """Persist the analysis-ready fact table as a local parquet-compatible CSV."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DATA_DIR / "order_line_fact.csv"
    build_order_line_fact().to_csv(output, index=False)
    return output


if __name__ == "__main__":
    print(f"Saved {save_clean_fact()}")
