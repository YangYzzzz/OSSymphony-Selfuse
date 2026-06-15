"""
Initial Setup: Configure a comprehensive devcontainer with custom Docker build
Task ID: vscode_gf3_084
Domain: vscode

Creates a data-pipeline project with requirements.txt, .env, and source files.
Does NOT create the .devcontainer directory — that is the agent's task.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_084'
PROJECT_DIR = f'{WORKDIR}/projects/data-pipeline'
SRC_DIR = f'{PROJECT_DIR}/src'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)

    # --- requirements.txt ---
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("""psycopg2==2.9.9
boto3==1.34.62
pandas==2.2.1
sqlalchemy==2.0.28
python-dotenv==1.0.1
requests==2.31.0
pydantic==2.6.3
celery==5.3.6
redis==5.0.3
""")

    # --- .env (sample environment variables) ---
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write("""# Database Configuration
DATABASE_HOST=db.internal.company.com
DATABASE_PORT=5432
DATABASE_NAME=analytics_prod
DATABASE_USER=pipeline_svc
DATABASE_PASSWORD=changeme_in_production

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA_PLACEHOLDER
AWS_SECRET_ACCESS_KEY=placeholder_secret_key
S3_BUCKET=company-data-lake

# Redis Configuration
REDIS_URL=redis://redis.internal.company.com:6379/0

# Pipeline Settings
BATCH_SIZE=5000
LOG_LEVEL=INFO
""")

    # --- src/pipeline.py ---
    with open(f'{SRC_DIR}/pipeline.py', 'w') as f:
        f.write('''"""
Data Pipeline - ETL from PostgreSQL to S3 Data Lake

Extracts analytics events from the production PostgreSQL database,
transforms them into Parquet format, and loads to S3 for downstream
consumption by the BI team.
"""

import os
import logging
from datetime import datetime, timedelta

import boto3
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT", "5432")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
S3_BUCKET = os.getenv("S3_BUCKET")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5000"))


def get_db_connection():
    """Create a connection to the analytics PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def extract_events(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Extract analytics events for the given date range."""
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    query = f"""
        SELECT event_id, user_id, event_type, event_data,
               created_at, session_id, device_type, country_code
        FROM analytics.events
        WHERE created_at >= %s AND created_at < %s
        ORDER BY created_at
    """
    df = pd.read_sql(query, engine, params=[start_date, end_date])
    logger.info(f"Extracted {len(df)} events from {start_date} to {end_date}")
    return df


def transform_events(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform raw events for the data lake."""
    df = df.copy()
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["event_date"] = df["created_at"].dt.date
    df["event_hour"] = df["created_at"].dt.hour
    df = df.dropna(subset=["user_id", "event_type"])
    df["country_code"] = df["country_code"].fillna("UNKNOWN")
    df["device_type"] = df["device_type"].fillna("other")
    return df


def load_to_s3(df: pd.DataFrame, partition_date: str):
    """Upload transformed data as Parquet to S3, partitioned by date."""
    s3 = boto3.client("s3")
    key = f"analytics/events/dt={partition_date}/events.parquet"
    parquet_buffer = df.to_parquet(index=False)
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=parquet_buffer)
    logger.info(f"Uploaded {len(df)} records to s3://{S3_BUCKET}/{key}")


def run_pipeline(target_date: datetime = None):
    """Run the full ETL pipeline for a single day."""
    if target_date is None:
        target_date = datetime.now() - timedelta(days=1)

    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    logger.info(f"Starting pipeline for {start.date()}")
    raw_df = extract_events(start, end)

    if raw_df.empty:
        logger.warning(f"No events found for {start.date()}")
        return

    transformed_df = transform_events(raw_df)
    load_to_s3(transformed_df, str(start.date()))
    logger.info(f"Pipeline complete for {start.date()}")


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    run_pipeline()
''')

    # --- src/__init__.py ---
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_pipeline.py ---
    with open(f'{PROJECT_DIR}/tests/test_pipeline.py', 'w') as f:
        f.write('''"""Unit tests for the data pipeline."""

import pytest
import pandas as pd
from datetime import datetime


def test_transform_fills_missing_country():
    """Verify transform fills missing country codes with UNKNOWN."""
    df = pd.DataFrame({
        "event_id": [1, 2],
        "user_id": ["u1", "u2"],
        "event_type": ["click", "view"],
        "event_data": ["{}", "{}"],
        "created_at": [datetime(2025, 3, 15, 10, 0), datetime(2025, 3, 15, 11, 0)],
        "session_id": ["s1", "s2"],
        "device_type": ["mobile", None],
        "country_code": ["US", None],
    })
    # Import would require DB connection, so we test logic directly
    df["country_code"] = df["country_code"].fillna("UNKNOWN")
    df["device_type"] = df["device_type"].fillna("other")
    assert df.loc[1, "country_code"] == "UNKNOWN"
    assert df.loc[1, "device_type"] == "other"


def test_transform_drops_null_user():
    """Events without user_id should be dropped."""
    df = pd.DataFrame({
        "event_id": [1, 2, 3],
        "user_id": ["u1", None, "u3"],
        "event_type": ["click", "view", None],
        "event_data": ["{}", "{}", "{}"],
        "created_at": [datetime(2025, 3, 15)] * 3,
        "session_id": ["s1", "s2", "s3"],
        "device_type": ["mobile", "desktop", "tablet"],
        "country_code": ["US", "GB", "DE"],
    })
    df = df.dropna(subset=["user_id", "event_type"])
    assert len(df) == 1
''')

    # --- config/logging.yaml ---
    with open(f'{PROJECT_DIR}/config/logging.yaml', 'w') as f:
        f.write("""version: 1
disable_existing_loggers: false
formatters:
  standard:
    format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    formatter: standard
    filename: /var/log/data-pipeline/pipeline.log
root:
  level: INFO
  handlers: [console, file]
""")

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(""".env
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
build/
.pytest_cache/
""")

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Data Pipeline

ETL pipeline that extracts analytics events from PostgreSQL, transforms them,
and loads Parquet files to S3 for the BI team.

## Setup

1. Copy `.env.example` to `.env` and fill in credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python src/pipeline.py`

## Architecture

- **Extract**: Reads from `analytics.events` table via SQLAlchemy
- **Transform**: Cleans nulls, adds date partitions, normalizes fields
- **Load**: Writes Parquet to `s3://<bucket>/analytics/events/dt=<date>/`
""")

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
