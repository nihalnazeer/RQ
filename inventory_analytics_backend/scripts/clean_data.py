import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up from /scripts → project root

RAW_PATH = BASE_DIR / "data/raw"
CLEAN_PATH = BASE_DIR / "data/clean"
QUARANTINE_PATH = BASE_DIR / "data/quarantine"

CLEAN_PATH.mkdir(parents=True, exist_ok=True)
QUARANTINE_PATH.mkdir(parents=True, exist_ok=True)

def normalize_dates(df, column, quarantine_df, filename):
    """Standardize date format and quarantine invalid rows."""
    try:
        df[column] = pd.to_datetime(df[column], errors="coerce")
        invalid_rows = df[df[column].isna()]
        if not invalid_rows.empty:
            invalid_rows["reason"] = f"Invalid date format in {column}"
            quarantine_df.append(invalid_rows.assign(source_file=filename))
            df = df.drop(invalid_rows.index)
    except Exception:
        pass

    return df, quarantine_df


def detect_variable_weight(df, sku_col, price_col):
    """Mark SKUs with multiple prices as variable weight."""
    price_variation = df.groupby(sku_col)[price_col].nunique()
    variable_skus = price_variation[price_variation > 1].index.tolist()
    return variable_skus


def clean_products(filename):
    print(f"Cleaning {filename}...")
    df = pd.read_csv(RAW_PATH / filename)

    quarantine = []

    # Remove rows missing SKU or product name
    missing = df[df["sku_id"].isna() | df["product_name"].isna()]
    if not missing.empty:
        missing["reason"] = "Missing SKU or product name"
        quarantine.append(missing.assign(source_file=filename))
        df = df.drop(missing.index)

    df.to_csv(CLEAN_PATH / filename, index=False)

    if quarantine:
        pd.concat(quarantine).to_csv(QUARANTINE_PATH / f"{filename}_quarantine.csv", index=False)

    return df


def clean_stock(filename, product_df):
    print(f"Cleaning {filename}...")
    df = pd.read_csv(RAW_PATH / filename)

    quarantine = []

    # Normalize dates
    df, quarantine = normalize_dates(df, "receipt_date", quarantine, filename)

    # Quarantine missing SKU or cost
    missing = df[df["sku_id"].isna() | df["unit_cost"].isna()]
    if not missing.empty:
        missing["reason"] = "Missing SKU or unit_cost"
        quarantine.append(missing.assign(source_file=filename))
        df = df.drop(missing.index)

    # Quarantine unknown SKUs
    invalid_skus = df[~df["sku_id"].isin(product_df["sku_id"])]
    if not invalid_skus.empty:
        invalid_skus["reason"] = "SKU not found in product_master"
        quarantine.append(invalid_skus.assign(source_file=filename))
        df = df.drop(invalid_skus.index)

    df.to_csv(CLEAN_PATH / filename, index=False)

    if quarantine:
        pd.concat(quarantine).to_csv(QUARANTINE_PATH / f"{filename}_quarantine.csv", index=False)

    return df


def clean_sales(filename, product_df):
    print(f"Cleaning {filename}...")
    df = pd.read_csv(RAW_PATH / filename)

    quarantine = []

    # Normalize dates
    df, quarantine = normalize_dates(df, "transaction_date", quarantine, filename)

    # Quarantine missing SKU or sale_price
    missing = df[df["sku_id"].isna() | df["sale_price"].isna()]
    if not missing.empty:
        missing["reason"] = "Missing SKU or sale_price"
        quarantine.append(missing.assign(source_file=filename))
        df = df.drop(missing.index)

    # Quarantine negative qty (POS error)
    negative_qty = df[df["quantity_sold"] < 0]
    if not negative_qty.empty:
        negative_qty["reason"] = "Negative quantity (POS ptc issue)"
        quarantine.append(negative_qty.assign(source_file=filename))
        df = df.drop(negative_qty.index)

    # Check unknown SKUs
    invalid_skus = df[~df["sku_id"].isin(product_df["sku_id"])]
    if not invalid_skus.empty:
        invalid_skus["reason"] = "SKU not found in product_master"
        quarantine.append(invalid_skus.assign(source_file=filename))
        df = df.drop(invalid_skus.index)

    # Mark variable-weight SKUs
    variable_skus = detect_variable_weight(df, "sku_id", "sale_price")
    df["variable_weight"] = df["sku_id"].apply(lambda x: True if x in variable_skus else False)

    df.to_csv(CLEAN_PATH / filename, index=False)

    if quarantine:
        pd.concat(quarantine).to_csv(QUARANTINE_PATH / f"{filename}_quarantine.csv", index=False)

    return df


def run():
    product_df = clean_products("products.csv")
    clean_stock("stock.csv", product_df)
    clean_sales("sales.csv", product_df)
    print("\nCleaning complete ✔️")


if __name__ == "__main__":
    run()
