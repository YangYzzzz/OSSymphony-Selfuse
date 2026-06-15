"""
Initial Setup: Data engineering workspace with Python extension only
Task ID: vscode_we_090
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_090'
PROJECT_DIR = f'{WORKDIR}/projects/data-pipeline'


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
    # 1. Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/notebooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/configs', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.github/workflows', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # 2. Create realistic data engineering project files
    # Main pipeline script
    with open(f'{PROJECT_DIR}/src/pipeline.py', 'w') as f:
        f.write('''"""Data pipeline for processing customer transaction records."""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class TransactionPipeline:
    """ETL pipeline for customer transactions."""

    def __init__(self, source_path: str, output_path: str):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.run_timestamp = datetime.now().isoformat()

    def extract(self) -> pd.DataFrame:
        """Read raw transaction data from CSV."""
        logger.info(f"Extracting data from {self.source_path}")
        df = pd.read_csv(self.source_path)
        logger.info(f"Extracted {len(df)} records")
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and transform transaction data."""
        df = df.dropna(subset=["transaction_id", "amount"])
        df["amount"] = df["amount"].astype(float).round(2)
        df["processed_at"] = self.run_timestamp
        return df

    def load(self, df: pd.DataFrame) -> None:
        """Write processed data to parquet."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        output_file = self.output_path / f"transactions_{self.run_timestamp[:10]}.parquet"
        df.to_parquet(output_file, index=False)
        logger.info(f"Loaded {len(df)} records to {output_file}")

    def run(self):
        """Execute full ETL pipeline."""
        raw = self.extract()
        clean = self.transform(raw)
        self.load(clean)
        return clean
''')

    # Database connector module
    with open(f'{PROJECT_DIR}/src/db_connector.py', 'w') as f:
        f.write('''"""Database connection utilities for PostgreSQL and SQLite."""

import sqlite3
from contextlib import contextmanager

@contextmanager
def get_sqlite_connection(db_path: str):
    """Context manager for SQLite connections."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(conn, query: str, params=None):
    """Execute a SQL query and return results."""
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    return cursor.fetchall()
''')

    # Jupyter notebook placeholder
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Data Exploration Notebook\\n", "\\n", "Analyze transaction patterns and anomalies."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import pandas as pd\\n", "import matplotlib.pyplot as plt\\n", "\\n", "# Load processed data\\n", "df = pd.read_parquet('../output/transactions_latest.parquet')\\n", "df.head()"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Transaction volume by day\\n", "daily = df.groupby(df['date'].dt.date)['amount'].sum()\\n", "daily.plot(kind='bar', figsize=(12, 5), title='Daily Transaction Volume')\\n", "plt.tight_layout()"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(f'{PROJECT_DIR}/notebooks/exploration.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=1)

    # GitHub Actions workflow (YAML)
    with open(f'{PROJECT_DIR}/.github/workflows/ci.yml', 'w') as f:
        f.write('''name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v
''')

    # Config file
    with open(f'{PROJECT_DIR}/configs/pipeline_config.yaml', 'w') as f:
        f.write('''pipeline:
  name: transaction-etl
  version: "1.2.0"
  schedule: "0 6 * * *"

sources:
  transactions:
    type: csv
    path: /data/raw/transactions/
    format: "*.csv"

destinations:
  warehouse:
    type: parquet
    path: /data/processed/
    partition_by: date

logging:
  level: INFO
  file: /var/log/pipeline.log
''')

    # Requirements file
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''pandas>=2.0.0
pyarrow>=14.0.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pyyaml>=6.0
pytest>=7.4.0
jupyter>=1.0.0
matplotlib>=3.8.0
''')

    # Test file
    with open(f'{PROJECT_DIR}/tests/test_pipeline.py', 'w') as f:
        f.write('''"""Tests for the transaction pipeline."""

import pytest
import pandas as pd
from src.pipeline import TransactionPipeline

def test_transform_removes_nulls():
    pipeline = TransactionPipeline("dummy.csv", "output/")
    df = pd.DataFrame({
        "transaction_id": ["TXN001", None, "TXN003"],
        "amount": [100.0, 200.0, None],
        "date": ["2025-01-01", "2025-01-02", "2025-01-03"]
    })
    result = pipeline.transform(df)
    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == "TXN001"

def test_transform_rounds_amounts():
    pipeline = TransactionPipeline("dummy.csv", "output/")
    df = pd.DataFrame({
        "transaction_id": ["TXN001"],
        "amount": [99.999],
        "date": ["2025-01-01"]
    })
    result = pipeline.transform(df)
    assert result.iloc[0]["amount"] == 100.0
''')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.pyc
.venv/
output/
*.parquet
.env
.DS_Store
''')

    # README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Data Pipeline

ETL pipeline for processing customer transaction records.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python -m src.pipeline
```
''')

    print(f'Project structure created at: {PROJECT_DIR}')

    # 3. Install only ms-python.python extension (pre-existing)
    subprocess.run(['code', '--install-extension', 'ms-python.python', '--force'],
                   capture_output=True, text=True)
    print('Installed ms-python.python extension')

    # Verify no .vscode directory exists (should not since we didn't create it)
    assert not os.path.exists(f'{PROJECT_DIR}/.vscode'), \
        ".vscode directory should NOT exist in initial state"

    # 4. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
