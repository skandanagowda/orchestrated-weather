# Orchestrated Weather Platform

Daily pipeline that ingests free Open-Meteo forecasts, lands raw JSON (bronze), transforms to Parquet (silver), runs data-quality checks, and sends alerts — orchestrated with Airflow.

## Stack

- Orchestration: Apache Airflow (Docker)
- Data: Python, Pandas, Parquet
- Storage: S3 (bronze/silver)
- DQ: Great Expectations (or Athena SQL checks)
- Alerting: Amazon SNS

## Run locally

1. Copy `.env.example` to `.env` and fill values.
2. `docker compose -f docker/docker-compose.yaml up`
