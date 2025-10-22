# weather/transform.py
# goal: read JSON files from data/bronze/ and write tidy hourly CSV to data/silver/

import os, glob, json
import pandas as pd

# choose which hourly columns we want to keep from the API
KEEP_HOURLY = {
    "time": "time_utc",
    "temperature_2m": "temp_c",
    "apparent_temperature": "apparent_c",
    "precipitation": "precip_mm",
    "relative_humidity_2m": "rh_pct",
    "wind_speed_10m": "wind_ms",
}

def to_hourly_df(payload: dict) -> pd.DataFrame:
    """Turn the Open-Meteo hourly section into a tidy DataFrame."""
    hourly = payload.get("hourly", {})
    # Build a dict of lists using our selected columns and new names
    data = {}
    for src_key, new_name in KEEP_HOURLY.items():
        data[new_name] = hourly.get(src_key, [])
    df = pd.DataFrame(data)

    # Basic quality: drop completely empty rows, sort by time
    if "time_utc" in df.columns:
        df = df.dropna(subset=["time_utc"]).sort_values("time_utc").reset_index(drop=True)
    return df

def transform_file(src_path: str) -> str:
    """Read one JSON file from bronze and write a CSV to silver with a matching name."""
    with open(src_path, "r") as f:
        payload = json.load(f)

    df = to_hourly_df(payload)

    # Make output path under data/silver with .csv extension
    dst_path = src_path.replace("data/bronze", "data/silver").replace(".json", ".csv")
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    df.to_csv(dst_path, index=False)
    return dst_path

if __name__ == "__main__":
    files = glob.glob("data/bronze/*.json")
    if not files:
        print("No files found in data/bronze/. Run weather/ingest.py first.")
    else:
        for fp in files:
            out = transform_file(fp)
            print("wrote:", out)
