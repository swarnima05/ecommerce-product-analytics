from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "data" / "ecommerce_analytics.db"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
QUERY_OUTPUT_DIR = PROJECT_ROOT / "reports" / "query_outputs"
SQL_DIR = PROJECT_ROOT / "sql"

# Revenue is recognized only for delivered orders. Cancelled and unavailable orders are
# retained in raw SQLite tables for operational analysis, but excluded from sales metrics.
REVENUE_ORDER_STATUS = "delivered"
