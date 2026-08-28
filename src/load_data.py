"""Load Olist source CSVs into normalized SQLite raw tables."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DATABASE_PATH, RAW_DATA_DIR

TABLE_FILES = {
    "orders": "olist_orders_dataset.csv", "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv", "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv", "reviews": "olist_order_reviews_dataset.csv",
}


def load_csvs_to_sqlite(raw_dir: Path = RAW_DATA_DIR, database_path: Path = DATABASE_PATH) -> None:
    """Replace SQLite raw tables with source CSV contents."""
    missing = [filename for filename in TABLE_FILES.values() if not (raw_dir / filename).exists()]
    if missing:
        raise FileNotFoundError(f"Missing CSVs in {raw_dir}: {', '.join(missing)}")
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        for table, filename in TABLE_FILES.items():
            pd.read_csv(raw_dir / filename).to_sql(table, connection, if_exists="replace", index=False)
        connection.executescript("""
            CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
            CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id);
            CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
        """)


if __name__ == "__main__":
    load_csvs_to_sqlite()
    print(f"Loaded raw tables into {DATABASE_PATH}")
