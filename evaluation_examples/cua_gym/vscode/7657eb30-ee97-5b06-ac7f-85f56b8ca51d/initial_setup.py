"""
Initial Setup: Open VSCode with database.py that has local history entries.
Task ID: vscode_rf_005
Domain: vscode

Creates ~/projects/api/ with database.py (broken version) and 5 local history
entries. The version from 2 edits ago has the correct DB connection string.
"""

import json
import os
import random
import shlex
import string
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_005'
PROJECT_DIR = f'{WORKDIR}/projects/api'
DB_FILE = f'{PROJECT_DIR}/database.py'
HISTORY_BASE = f'{WORKDIR}/.config/Code/User/History'

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

def random_id(length=4):
    return ''.join(random.choices(string.ascii_letters, k=length))

# ── Version content for database.py ──
# Version 1 (oldest): initial skeleton
VERSION_1 = '''\
"""Database connection and query utilities for the API service."""

import os
import logging
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "db-prod-replica-01.internal.acme.io")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "acme_api_production")
DB_USER = os.getenv("DB_USER", "api_service")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

connection_pool = None


def init_pool(min_conn=2, max_conn=10):
    """Initialize the connection pool."""
    global connection_pool
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        min_conn,
        max_conn,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    logger.info("Connection pool initialized (%d-%d connections)", min_conn, max_conn)


@contextmanager
def get_connection():
    """Yield a connection from the pool, returning it on exit."""
    conn = connection_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)
'''

# Version 2: added query helpers
VERSION_2 = VERSION_1 + '''

def fetch_all(query: str, params=None):
    """Execute a SELECT and return all rows."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def fetch_one(query: str, params=None):
    """Execute a SELECT and return the first row."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
'''

# Version 3 (correct version — 2 edits ago): added execute_mutation + health_check
VERSION_3 = VERSION_2 + '''

def execute_mutation(query: str, params=None):
    """Execute an INSERT / UPDATE / DELETE and return affected row count."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount


def health_check() -> bool:
    """Return True if the database is reachable."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone()[0] == 1
    except Exception as exc:
        logger.error("Health check failed: %s", exc)
        return False
'''

# Version 4: refactored connection string format but still correct
VERSION_4 = VERSION_3.replace(
    'DB_HOST = os.getenv("DB_HOST", "db-prod-replica-01.internal.acme.io")',
    'DB_HOST = os.getenv("DB_HOST", "db-prod-replica-01.internal.acme.io")  # primary read replica'
).replace(
    'DB_NAME = os.getenv("DB_NAME", "acme_api_production")',
    'DB_NAME = os.getenv("DB_NAME", "acme_api_production")  # do not change without DBA approval'
)

# Version 5 (current — BROKEN): someone overwrote the connection string
VERSION_5_BROKEN = VERSION_4.replace(
    'DB_HOST = os.getenv("DB_HOST", "db-prod-replica-01.internal.acme.io")  # primary read replica',
    'DB_HOST = os.getenv("DB_HOST", "localhost")  # FIXME: accidentally changed during local testing'
).replace(
    'DB_PORT = int(os.getenv("DB_PORT", "5432"))',
    'DB_PORT = int(os.getenv("DB_PORT", "3306"))  # wrong port from local MySQL testing'
).replace(
    'DB_NAME = os.getenv("DB_NAME", "acme_api_production")  # do not change without DBA approval',
    'DB_NAME = os.getenv("DB_NAME", "test_db")  # oops, still pointed at test'
).replace(
    'DB_USER = os.getenv("DB_USER", "api_service")',
    'DB_USER = os.getenv("DB_USER", "root")  # local dev creds left in'
)

VERSIONS = [VERSION_1, VERSION_2, VERSION_3, VERSION_4, VERSION_5_BROKEN]

def create_project():
    """Create the project directory with supporting files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main file — current (broken) version
    with open(DB_FILE, 'w') as f:
        f.write(VERSION_5_BROKEN)

    # Supporting files for realism
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write('''\
"""FastAPI application entry point."""

from fastapi import FastAPI
from database import init_pool, health_check

app = FastAPI(title="Acme API", version="2.4.1")


@app.on_event("startup")
async def startup():
    init_pool()


@app.get("/health")
async def health():
    db_ok = health_check()
    return {"status": "healthy" if db_ok else "degraded", "database": db_ok}
''')

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''\
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
''')

    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write('''\
DB_HOST=db-prod-replica-01.internal.acme.io
DB_PORT=5432
DB_NAME=acme_api_production
DB_USER=api_service
DB_PASSWORD=s3cret-prod-2025
''')

    with open(f'{PROJECT_DIR}/models.py', 'w') as f:
        f.write('''\
"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserOut(BaseModel):
    id: int
    email: str
    display_name: str
    created_at: datetime


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_cents: int
    status: str
    placed_at: datetime
    shipped_at: Optional[datetime] = None
''')

    print(f'Project created at {PROJECT_DIR}')


def create_local_history():
    """Create VSCode local history entries for database.py."""
    # The resource URI that VSCode uses
    resource_uri = f'file://{DB_FILE}'

    # Create a history directory for this file
    # Use a deterministic-looking hash prefix
    hist_dir_name = '5a3c7f2e'
    hist_dir = f'{HISTORY_BASE}/{hist_dir_name}'
    os.makedirs(hist_dir, exist_ok=True)

    # Base timestamp: ~2 hours ago
    now_ms = int(time.time() * 1000)
    base_ts = now_ms - (2 * 60 * 60 * 1000)  # 2 hours ago

    entries = []
    for i, version_content in enumerate(VERSIONS):
        entry_id = random_id() + '.py'
        # Space entries ~25 minutes apart
        ts = base_ts + (i * 25 * 60 * 1000)

        # Write the snapshot file
        with open(f'{hist_dir}/{entry_id}', 'w') as f:
            f.write(version_content)

        entries.append({
            "id": entry_id,
            "timestamp": ts,
        })

    # Write entries.json
    entries_json = {
        "version": 1,
        "resource": resource_uri,
        "entries": entries,
    }
    with open(f'{hist_dir}/entries.json', 'w') as f:
        json.dump(entries_json, f)

    print(f'Local history created with {len(entries)} entries in {hist_dir}')


def setup_vscode_workspace():
    """Configure VSCode to have the project as recent workspace."""
    vscode_user = f'{WORKDIR}/.config/Code/User'
    os.makedirs(vscode_user, exist_ok=True)

    # Ensure settings exist with timeline enabled
    settings_path = f'{vscode_user}/settings.json'
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    settings.update({
        "timeline.showLocalHistory": True,
        "workbench.localHistory.enabled": True,
        "workbench.localHistory.maxFileEntries": 50,
    })

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

    print('VSCode settings updated for local history')


def main():
    create_project()
    create_local_history()
    setup_vscode_workspace()

    # Launch VSCode with the project folder and open database.py
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{DB_FILE}"', delay_sec=2.0)
    print('GUI_READY: VSCode launched with DISPLAY=:0')


main()
