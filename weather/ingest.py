# weather/ingest.py
# goal: download weather JSON for a few cities and save to data/bronze/

import requests, json, time, os
from datetime import datetime

# 3 demo cities (you can add more later)
CITIES = {
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
}

def fetch(lat, lon):
    """Call the free Open-Meteo API and return JSON."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
        "&timezone=UTC"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def save_raw(payload, city):
    """Write JSON to data/bronze with a simple timestamped filename."""
    os.makedirs("data/bronze", exist_ok=True)
    run_date = datetime.utcnow().date().isoformat()  # YYYY-MM-DD
    ts = int(time.time())
    safe_city = city.replace(" ", "_")
    path = f"data/bronze/{safe_city}_{run_date}_{ts}.json"
    with open(path, "w") as f:
        json.dump(payload, f)
    print("saved:", path)

if __name__ == "__main__":
    for city, (lat, lon) in CITIES.items():
        data = fetch(lat, lon)
        save_raw(data, city)
