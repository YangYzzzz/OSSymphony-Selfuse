"""
Initial Setup: Configure VSCode workspace with project structure but no SQLTools connections
Task ID: vscode_gf3_091
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_091'
PROJECT_DIR = f'{WORKDIR}/projects/data-platform'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
SETTINGS_PATH = f'{VSCODE_DIR}/settings.json'

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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/queries', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/scripts', exist_ok=True)

    # Create .vscode/settings.json with basic workspace settings (NO SQLTools connections)
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "files.trimTrailingWhitespace": True,
        "files.insertFinalNewline": True,
        "editor.rulers": [80, 120],
        "search.exclude": {
            "**/__pycache__": True,
            "**/node_modules": True
        }
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created workspace settings: {SETTINGS_PATH}')

    # Create realistic project files

    # Main Python ETL module
    with open(f'{PROJECT_DIR}/src/etl_pipeline.py', 'w') as f:
        f.write('''"""ETL Pipeline for Data Platform
Handles extraction from PostgreSQL analytics DB,
transformation logic, and loading into SQLite warehouse.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DataExtractor:
    """Extracts data from the analytics PostgreSQL database."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.last_run = None

    def extract_daily_metrics(self, date: str) -> list:
        """Extract daily aggregated metrics from analytics DB."""
        query = """
            SELECT metric_name, metric_value, recorded_at
            FROM daily_metrics
            WHERE DATE(recorded_at) = %s
            ORDER BY metric_name
        """
        logger.info(f"Extracting metrics for {date}")
        # Implementation would use psycopg2 or sqlalchemy
        return []

    def extract_user_sessions(self, start_date: str, end_date: str) -> list:
        """Extract user session data for the given date range."""
        query = """
            SELECT user_id, session_start, session_end,
                   page_views, events_count
            FROM user_sessions
            WHERE session_start BETWEEN %s AND %s
        """
        logger.info(f"Extracting sessions from {start_date} to {end_date}")
        return []


class CacheManager:
    """Manages Redis cache for frequently accessed data."""

    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port

    def invalidate_dashboard_cache(self):
        """Clear cached dashboard aggregations."""
        keys_pattern = "dashboard:*"
        logger.info(f"Invalidating cache keys matching {keys_pattern}")

    def warm_up_cache(self, metrics: list):
        """Pre-populate cache with fresh metric data."""
        for metric in metrics:
            cache_key = f"metric:{metric['name']}:{metric['date']}"
            logger.info(f"Caching {cache_key}")


class WarehouseLoader:
    """Loads transformed data into the SQLite warehouse."""

    def __init__(self, db_path: str = "./data/warehouse.db"):
        self.db_path = db_path

    def load_daily_summary(self, records: list):
        """Insert daily summary records into warehouse."""
        logger.info(f"Loading {len(records)} records into warehouse")

    def create_tables_if_needed(self):
        """Ensure warehouse tables exist."""
        logger.info("Checking warehouse schema")


def run_pipeline():
    """Execute the full ETL pipeline."""
    extractor = DataExtractor("postgresql://analytics-db.local:5432/analytics")
    cache = CacheManager()
    loader = WarehouseLoader()

    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Starting ETL pipeline for {today}")

    # Extract
    metrics = extractor.extract_daily_metrics(today)
    sessions = extractor.extract_user_sessions(today, today)

    # Transform & Load
    loader.create_tables_if_needed()
    loader.load_daily_summary(metrics)

    # Refresh cache
    cache.invalidate_dashboard_cache()
    cache.warm_up_cache(metrics)

    logger.info("Pipeline complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
''')

    # SQL query files
    with open(f'{PROJECT_DIR}/queries/daily_metrics.sql', 'w') as f:
        f.write('''-- Daily Metrics Aggregation Query
-- Runs against: analytics-db.local (PostgreSQL)

SELECT
    dm.metric_name,
    dm.metric_value,
    dm.recorded_at,
    d.department_name
FROM daily_metrics dm
JOIN departments d ON dm.department_id = d.id
WHERE DATE(dm.recorded_at) = CURRENT_DATE
ORDER BY dm.metric_name, d.department_name;
''')

    with open(f'{PROJECT_DIR}/queries/user_sessions.sql', 'w') as f:
        f.write('''-- User Session Analysis
-- Runs against: analytics-db.local (PostgreSQL)

SELECT
    us.user_id,
    u.username,
    us.session_start,
    us.session_end,
    EXTRACT(EPOCH FROM (us.session_end - us.session_start)) / 60 AS duration_minutes,
    us.page_views,
    us.events_count
FROM user_sessions us
JOIN users u ON us.user_id = u.id
WHERE us.session_start >= NOW() - INTERVAL '7 days'
ORDER BY us.session_start DESC
LIMIT 500;
''')

    with open(f'{PROJECT_DIR}/queries/warehouse_summary.sql', 'w') as f:
        f.write('''-- Warehouse Summary Report
-- Runs against: ./data/warehouse.db (SQLite)

SELECT
    summary_date,
    total_users,
    active_sessions,
    avg_session_duration_min,
    total_page_views,
    total_events
FROM daily_summary
WHERE summary_date >= date('now', '-30 days')
ORDER BY summary_date DESC;
''')

    # Configuration script
    with open(f'{PROJECT_DIR}/scripts/setup_warehouse.py', 'w') as f:
        f.write('''"""Initialize the local SQLite warehouse database schema."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "warehouse.db")


def init_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary_date DATE NOT NULL UNIQUE,
            total_users INTEGER DEFAULT 0,
            active_sessions INTEGER DEFAULT 0,
            avg_session_duration_min REAL DEFAULT 0.0,
            total_page_views INTEGER DEFAULT 0,
            total_events INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metric_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            snapshot_date DATE NOT NULL,
            source TEXT DEFAULT 'analytics_db',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Warehouse schema initialized at {DB_PATH}")


if __name__ == "__main__":
    init_schema()
''')

    # Project README-like config
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[project]
name = "data-platform"
version = "0.4.2"
description = "Internal data platform ETL and analytics tooling"
requires-python = ">=3.10"

[project.dependencies]
psycopg2-binary = ">=2.9.9"
redis = ">=5.0.0"
sqlalchemy = ">=2.0.0"

[tool.ruff]
line-length = 120
target-version = "py311"
''')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.pyc
.env
data/warehouse.db
*.log
.venv/
''')

    # Create an empty placeholder for the warehouse db location
    with open(f'{PROJECT_DIR}/data/.gitkeep', 'w') as f:
        f.write('')

    print(f'Project structure created at {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
