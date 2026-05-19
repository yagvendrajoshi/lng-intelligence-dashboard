# fetcher.py
# US LNG export volumes by destination — EIA API → data/eia_exports.csv

import requests
import pandas as pd
from config import EIA_API_KEY

# 1 MMcf = 1,020 MMBtu (standard energy conversion)
MMCF_TO_MMBTU = 1020


def fetch_lng_exports():
    """
    Fetch monthly US LNG vessel export volumes by destination country.
    Filters for vessel exports only — excludes truck, pipeline, prices.
    Returns clean DataFrame, saves to data/eia_exports.csv.
    """

    print("Fetching US LNG export data from EIA...")

    url = "https://api.eia.gov/v2/natural-gas/move/expc/data/"

    params = {
        "api_key"            : EIA_API_KEY,
        "frequency"          : "monthly",
        "data[0]"            : "value",
        "sort[0][column]"    : "period",
        "sort[0][direction]" : "desc",
        "length"             : 5000,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"EIA API error — status {response.status_code}")
        print(response.text)
        return None

    rows = response.json()["response"]["data"]
    df   = pd.DataFrame(rows)

    print(f"Total rows before filter: {len(df)}")

    # Keep vessel LNG exports by country — volumes only, no prices
    # "by Vessel to" captures country-level vessel shipments
    # Excludes: pipeline, truck, re-exports, price series
    mask = (
        df["series-description"].str.contains("Liquefied", na=False) &
        df["series-description"].str.contains("by Vessel to", na=False) &
        ~df["series-description"].str.contains("Price", na=False) &
        ~df["series-description"].str.contains("Re-Export", na=False)
    )

    df = df[mask].copy()

    print(f"LNG vessel export rows after filter: {len(df)}")

    if len(df) == 0:
        print("No rows matched filter — check series descriptions")
        return None

    # Extract destination country from series description
    # Pattern: "... by Vessel to COUNTRY (Million Cubic Feet)"
    df["destination"] = (
        df["series-description"]
        .str.extract(r"by Vessel to (.+?)\s*\(")[0]
        .str.strip()
    )

    # Keep useful columns only
    df = df[["period", "destination", "value"]].copy()
    df.columns = ["period", "destination", "volume_mmcf"]

    # Convert types
    df["period"]       = pd.to_datetime(df["period"])
    df["volume_mmcf"]  = pd.to_numeric(df["volume_mmcf"], errors="coerce")

    # Convert MMcf to MMBtu
    df["volume_mmbtu"] = df["volume_mmcf"] * MMCF_TO_MMBTU

    # Sort by date then destination
    df = df.sort_values(
        ["period", "destination"], ascending=True
    ).reset_index(drop=True)

    # Save to CSV
    df.to_csv("data/eia_exports.csv", index=False)

    print(f"\nSaved {len(df)} rows to data/eia_exports.csv")
    print("\nSample — top destinations:")
    print(df.groupby("destination")["volume_mmbtu"].sum()
            .sort_values(ascending=False)
            .head(10))

    return df


if __name__ == "__main__":
    fetch_lng_exports()