"""Render reproducible static and interactive charts from SQL results."""
from __future__ import annotations

import os
from pathlib import Path

from src.config import FIGURES_DIR, PROJECT_ROOT

# Headless, repository-local configuration keeps chart generation portable in CI.
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

from src.run_queries import run_all_queries


def save_revenue_charts(monthly: pd.DataFrame, output_dir: Path) -> None:
    """Save revenue and AOV trend as separate recruiter-friendly PNGs."""
    monthly["order_month"] = pd.to_datetime(monthly["order_month"])
    for metric, title, filename, color in [("revenue", "Monthly Delivered Revenue", "monthly_revenue.png", "#2563eb"), ("aov", "Monthly Average Order Value", "monthly_aov.png", "#0f766e")]:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=monthly, x="order_month", y=metric, marker="o", ax=ax, color=color)
        ax.set(title=title, xlabel="Purchase month", ylabel="BRL",)
        fig.tight_layout(); fig.savefig(output_dir / filename, dpi=160); plt.close(fig)


def save_category_chart(categories: pd.DataFrame, output_dir: Path) -> None:
    """Save top category revenue ranking."""
    chart = categories.sort_values("revenue").tail(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=chart, x="revenue", y="category", ax=ax, color="#7c3aed")
    ax.set(title="Top Categories by Delivered Revenue", xlabel="Revenue (BRL)", ylabel="Category")
    fig.tight_layout(); fig.savefig(output_dir / "top_categories.png", dpi=160); plt.close(fig)


def save_retention_heatmap(retention: pd.DataFrame, output_dir: Path) -> None:
    """Save cohort retention matrix, masking future/unobserved cells."""
    table = retention.pivot(index="cohort_month", columns="month_number", values="retention_pct")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(table, annot=True, fmt=".0f", cmap="Blues", vmin=0, vmax=100, ax=ax, cbar_kws={"label": "Retention %"})
    ax.set(title="Delivered-Order Cohort Retention", xlabel="Months since first purchase", ylabel="First purchase month")
    fig.tight_layout(); fig.savefig(output_dir / "cohort_retention.png", dpi=160); plt.close(fig)


def save_interactive_revenue(monthly: pd.DataFrame, output_dir: Path) -> None:
    """Export a standalone Plotly chart for interactive exploration."""
    px.line(monthly, x="order_month", y="revenue", markers=True, title="Monthly Delivered Revenue").write_html(output_dir / "monthly_revenue_interactive.html", include_plotlyjs=True)


def main() -> None:
    """Run SQL then render all report figures."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    results = run_all_queries()
    save_revenue_charts(results["01_revenue_metrics"][0], FIGURES_DIR)
    save_category_chart(results["03_top_products"][1], FIGURES_DIR)
    save_retention_heatmap(results["05_cohort_retention"][0], FIGURES_DIR)
    save_interactive_revenue(results["01_revenue_metrics"][0], FIGURES_DIR)


if __name__ == "__main__":
    main()
