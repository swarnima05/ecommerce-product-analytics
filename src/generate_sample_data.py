"""Generate a deterministic Olist-shaped demo dataset for offline pipeline testing."""
from __future__ import annotations

from datetime import timedelta
import random

import pandas as pd

from src.config import RAW_DATA_DIR


def build_sample_data() -> dict[str, pd.DataFrame]:
    """Return linked tables using the Olist columns consumed by this project."""
    rng = random.Random(42)
    months = pd.date_range("2017-01-01", "2018-08-01", freq="MS")
    categories = ["bed_bath_table", "health_beauty", "computers_accessories", "sports_leisure"]
    products = pd.DataFrame([
        {"product_id": f"p{i:03d}", "product_category_name": categories[i % 4],
         "product_weight_g": 300 + i * 25, "product_length_cm": 20,
         "product_height_cm": 10, "product_width_cm": 15}
        for i in range(1, 25)
    ])
    customers = pd.DataFrame([
        {"customer_id": f"c{i:03d}", "customer_unique_id": f"u{i:03d}",
         "customer_zip_code_prefix": 10000 + i, "customer_city": "sao paulo",
         "customer_state": "SP" if i % 3 else "RJ"}
        for i in range(1, 81)
    ])
    orders: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    payments: list[dict[str, object]] = []
    reviews: list[dict[str, object]] = []
    n = 0
    for month_index, month in enumerate(months):
        for _ in range(12 + month_index % 7):
            n += 1
            order_id, customer = f"o{n:04d}", customers.iloc[rng.randrange(len(customers))]
            ordered = month + timedelta(days=rng.randrange(2, 26), hours=rng.randrange(24))
            status = "delivered" if rng.random() > 0.08 else rng.choice(["canceled", "unavailable"])
            orders.append({"order_id": order_id, "customer_id": customer.customer_id,
                "order_status": status, "order_purchase_timestamp": ordered.isoformat(),
                "order_approved_at": (ordered + timedelta(hours=4)).isoformat(),
                "order_delivered_carrier_date": (ordered + timedelta(days=2)).isoformat(),
                "order_delivered_customer_date": (ordered + timedelta(days=7)).isoformat() if status == "delivered" else None,
                "order_estimated_delivery_date": (ordered + timedelta(days=10)).isoformat()})
            line_count = 1 if rng.random() < .78 else 2
            total = 0.0
            for line in range(1, line_count + 1):
                product = products.iloc[rng.randrange(len(products))]
                price, freight = round(rng.uniform(25, 320), 2), round(rng.uniform(8, 40), 2)
                total += price + freight
                items.append({"order_id": order_id, "order_item_id": line, "product_id": product.product_id,
                    "seller_id": f"s{rng.randrange(1, 11):02d}", "shipping_limit_date": (ordered + timedelta(days=2)).isoformat(),
                    "price": price, "freight_value": freight})
            payments.append({"order_id": order_id, "payment_sequential": 1, "payment_type": "credit_card",
                "payment_installments": rng.randrange(1, 7), "payment_value": round(total, 2)})
            reviews.append({"review_id": f"r{n:04d}", "order_id": order_id, "review_score": rng.randrange(2, 6),
                "review_comment_title": None, "review_comment_message": None,
                "review_creation_date": (ordered + timedelta(days=8)).isoformat(), "review_answer_timestamp": (ordered + timedelta(days=9)).isoformat()})
    return {"olist_customers_dataset.csv": customers, "olist_orders_dataset.csv": pd.DataFrame(orders),
            "olist_order_items_dataset.csv": pd.DataFrame(items), "olist_products_dataset.csv": products,
            "olist_order_payments_dataset.csv": pd.DataFrame(payments), "olist_order_reviews_dataset.csv": pd.DataFrame(reviews)}


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, frame in build_sample_data().items():
        frame.to_csv(RAW_DATA_DIR / filename, index=False)
    print(f"Wrote sample CSVs to {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()
