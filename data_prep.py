"""
data_prep.py — Prepare Superstore data for Google Sheets / Looker Studio
Author: Guilherme Dionysio
"""

import pandas as pd
from pathlib import Path

INPUT_PATH  = Path("data/superstore.csv")
OUTPUT_PATH = Path("data/superstore_clean.csv")


def prepare_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin-1")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Parse dates
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    df["ship_date"]  = pd.to_datetime(df["ship_date"]).dt.strftime("%Y-%m-%d")

    # Drop duplicates and critical nulls
    df = df.drop_duplicates()
    df = df.dropna(subset=["order_date", "sales", "product_name", "region"])

    # Add helper columns useful for Looker Studio
    df["year"]       = pd.to_datetime(df["order_date"]).dt.year
    df["month"]      = pd.to_datetime(df["order_date"]).dt.month
    df["month_name"] = pd.to_datetime(df["order_date"]).dt.strftime("%B")
    df["year_month"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m")

    # Round financial columns
    df["sales"]    = df["sales"].round(2)
    df["profit"]   = df["profit"].round(2)
    df["discount"] = df["discount"].round(2)

    return df


def main():
    print("\n[START] Preparing data for Google Sheets...\n")

    df = prepare_data(INPUT_PATH)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"[OK] Records exported: {len(df):,}")
    print(f"[OK] Columns:          {', '.join(df.columns.tolist())}")
    print(f"[OK] File saved:       {OUTPUT_PATH}")
    print(f"\n[DONE] Upload '{OUTPUT_PATH}' to Google Sheets.\n")


if __name__ == "__main__":
    main()