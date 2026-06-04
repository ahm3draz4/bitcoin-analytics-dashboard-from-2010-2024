import pandas as pd
import numpy as np


# ── 1. LOAD & CLEAN ─────────────────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the CSV, clean column types, and return a tidy DataFrame.
    """
    df = pd.read_csv(filepath)

    # --- Parse Date ---
    df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y")

    # --- Clean numeric columns (remove commas) ---
    for col in ["Price", "Open", "High", "Low"]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(float)

    # --- Clean Volume: convert "86.85K" → 86850, "1.2M" → 1200000 ---
    def parse_volume(v):
        v = str(v).strip()
        if v in ("", "-", "nan"):
            return np.nan
        if v.endswith("K"):
            return float(v[:-1]) * 1_000
        if v.endswith("M"):
            return float(v[:-1]) * 1_000_000
        if v.endswith("B"):
            return float(v[:-1]) * 1_000_000_000
        return float(v)

    df["Vol."] = df["Vol."].apply(parse_volume)

    # --- Clean Change % ---
    df["Change %"] = df["Change %"].astype(str).str.replace("%", "").astype(float)

    # --- Derived columns (useful for charts) ---
    df["Year"]        = df["Date"].dt.year
    df["Month"]       = df["Date"].dt.month
    df["Month_Name"]  = df["Date"].dt.strftime("%b")
    df["DayRange"]    = df["High"] - df["Low"]          # daily price spread
    df["Direction"]   = df["Change %"].apply(lambda x: "Bullish" if x >= 0 else "Bearish")

    # Sort oldest → newest for time-series charts
    df = df.sort_values("Date").reset_index(drop=True)

    return df


# ── 2. FILTER FUNCTIONS ──────────────────────────────────────────────────────

def filter_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """Filter rows between start_date and end_date (inclusive)."""
    return df[(df["Date"] >= pd.Timestamp(start_date)) &
              (df["Date"] <= pd.Timestamp(end_date))]


def filter_by_price_range(df: pd.DataFrame, min_price: float, max_price: float) -> pd.DataFrame:
    """Keep rows where closing Price is within [min_price, max_price]."""
    return df[(df["Price"] >= min_price) & (df["Price"] <= max_price)]


def filter_by_direction(df: pd.DataFrame, directions: list) -> pd.DataFrame:
    """Keep rows matching selected directions (Bullish / Bearish)."""
    if not directions:
        return df
    return df[df["Direction"].isin(directions)]


def filter_by_years(df: pd.DataFrame, years: list) -> pd.DataFrame:
    """Keep rows for selected years."""
    if not years:
        return df
    return df[df["Year"].isin(years)]


def filter_by_keyword(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Text search: filter rows where the Date string contains the keyword.
    Example: typing '2020' returns all 2020 rows.
    """
    if not keyword.strip():
        return df
    kw = keyword.strip().lower()
    return df[df["Date"].astype(str).str.lower().str.contains(kw)]


def apply_all_filters(df, start_date, end_date, price_min, price_max,
                      directions, years, keyword):
    """
    Chain all filters together.  Used in app.py to get the final filtered df.
    """
    df = filter_by_date(df, start_date, end_date)
    df = filter_by_price_range(df, price_min, price_max)
    df = filter_by_direction(df, directions)
    df = filter_by_years(df, years)
    df = filter_by_keyword(df, keyword)
    return df
