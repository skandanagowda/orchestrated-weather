# dags/weather_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from weather.ingest import fetch, save_raw, CITIES
from weather.transform import transform_file

def run_ingest():
    for city, (lat, lon) in CITIES.items():
        payload = fetch(lat, lon)
        save_raw(payload, city)

def run_transform():
    import glob
    files = glob.glob("data/bronze/*.json")
    if not files:
        print("No bronze files found. Run ingest first.")
    for fp in files:
        out = transform_file(fp)
        print("wrote:", out)

with DAG(
    dag_id="weather_local_ingest_transform",
    start_date=datetime(2025, 10, 1),
    schedule=None,  # manual trigger for now
    catchup=False,
    default_args={"owner": "data-eng"},
    tags=["weather", "local"],
) as dag:
    ingest = PythonOperator(task_id="ingest_open_meteo", python_callable=run_ingest)
    transform = PythonOperator(task_id="transform_to_silver", python_callable=run_transform)

    ingest >> transform
