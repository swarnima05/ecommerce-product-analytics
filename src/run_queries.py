"""Execute documented SQL files and persist their result tables."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DATABASE_PATH, QUERY_OUTPUT_DIR, SQL_DIR


def split_sql_statements(sql: str) -> list[str]:
    """Split this project's simple semicolon-terminated query files."""
    return [statement.strip() for statement in sql.split(";") if statement.strip()]


def execute_sql_file(sql_path: Path, database_path: Path = DATABASE_PATH) -> list[pd.DataFrame]:
    """Run all SELECT statements in one SQL file and return result frames."""
    with sqlite3.connect(database_path) as connection:
        return [pd.read_sql_query(statement, connection) for statement in split_sql_statements(sql_path.read_text())]


def run_all_queries() -> dict[str, list[pd.DataFrame]]:
    """Run metric queries and save each result to a report-friendly CSV."""
    QUERY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[pd.DataFrame]] = {}
    for sql_path in sorted(SQL_DIR.glob("*.sql")):
        frames = execute_sql_file(sql_path)
        results[sql_path.stem] = frames
        for index, frame in enumerate(frames, start=1):
            frame.to_csv(QUERY_OUTPUT_DIR / f"{sql_path.stem}_{index}.csv", index=False)
    return results


if __name__ == "__main__":
    for name, frames in run_all_queries().items():
        print(f"{name}: {', '.join(str(len(frame)) for frame in frames)} rows")
