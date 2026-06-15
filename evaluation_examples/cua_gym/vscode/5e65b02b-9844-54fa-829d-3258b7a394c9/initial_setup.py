"""
Initial Setup: Configure Python PYTHONPATH for src/ and lib/ directories
Task ID: vscode_py_074
Domain: vscode

Creates a workspace with src/ and lib/ directories containing Python modules,
and a main.py that imports from both. No PYTHONPATH configuration is applied yet
(that's the agent's task).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_074'
WORKSPACE = f'{WORKDIR}/workspace'

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
    # ---- Create workspace directory structure ----
    os.makedirs(f'{WORKSPACE}/src/utils', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/src/models', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/lib/database', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/lib/cache', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/.vscode', exist_ok=True)

    # ---- src/utils/__init__.py ----
    with open(f'{WORKSPACE}/src/utils/__init__.py', 'w') as f:
        f.write('')

    # ---- src/utils/helpers.py ----
    with open(f'{WORKSPACE}/src/utils/helpers.py', 'w') as f:
        f.write('''"""Utility helper functions for the analytics pipeline."""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a numeric amount as currency string."""
    symbols = {"USD": "$", "EUR": "\\u20ac", "GBP": "\\u00a3", "JPY": "\\u00a5"}
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{amount:,.2f}"


def calculate_growth_rate(current: float, previous: float) -> Optional[float]:
    """Calculate percentage growth rate between two periods."""
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100


def date_range(start_date: str, days: int) -> List[str]:
    """Generate a list of date strings starting from start_date."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]


def aggregate_metrics(records: List[Dict]) -> Dict:
    """Aggregate numeric fields across a list of record dicts."""
    if not records:
        return {}
    result = {}
    for key in records[0]:
        values = [r[key] for r in records if isinstance(r.get(key), (int, float))]
        if values:
            result[key] = {
                "sum": sum(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            }
    return result
''')

    # ---- src/models/__init__.py ----
    with open(f'{WORKSPACE}/src/models/__init__.py', 'w') as f:
        f.write('')

    # ---- src/models/report.py ----
    with open(f'{WORKSPACE}/src/models/report.py', 'w') as f:
        f.write('''"""Data models for quarterly business reports."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class SalesRecord:
    """Individual sales transaction record."""
    transaction_id: str
    product_name: str
    quantity: int
    unit_price: float
    sale_date: date
    region: str
    sales_rep: str

    @property
    def total_amount(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class QuarterlyReport:
    """Aggregated quarterly business report."""
    quarter: str
    year: int
    records: List[SalesRecord] = field(default_factory=list)
    notes: Optional[str] = None

    @property
    def total_revenue(self) -> float:
        return sum(r.total_amount for r in self.records)

    @property
    def transaction_count(self) -> int:
        return len(self.records)

    def top_products(self, n: int = 5) -> List[str]:
        product_totals = {}
        for r in self.records:
            product_totals[r.product_name] = (
                product_totals.get(r.product_name, 0) + r.total_amount
            )
        sorted_products = sorted(
            product_totals.items(), key=lambda x: x[1], reverse=True
        )
        return [name for name, _ in sorted_products[:n]]
''')

    # ---- src/__init__.py ----
    with open(f'{WORKSPACE}/src/__init__.py', 'w') as f:
        f.write('')

    # ---- lib/database/__init__.py ----
    with open(f'{WORKSPACE}/lib/database/__init__.py', 'w') as f:
        f.write('')

    # ---- lib/database/connector.py ----
    with open(f'{WORKSPACE}/lib/database/connector.py', 'w') as f:
        f.write('''"""Database connection management for the analytics platform."""

import sqlite3
import os
from typing import List, Dict, Any, Optional


class DatabaseConnector:
    """Manages SQLite database connections and queries."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._connection = None

    def connect(self) -> None:
        """Establish database connection."""
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row

    def disconnect(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts."""
        if not self._connection:
            self.connect()
        cursor = self._connection.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT query and return the last row id."""
        if not self._connection:
            self.connect()
        cursor = self._connection.execute(query, params)
        self._connection.commit()
        return cursor.lastrowid

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        result = self.execute_query(
            "SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?",
            (table_name,),
        )
        return len(result) > 0


def get_default_connector(data_dir: str = "/home/user/data") -> DatabaseConnector:
    """Create a connector pointing to the default analytics database."""
    db_path = os.path.join(data_dir, "analytics.db")
    connector = DatabaseConnector(db_path)
    connector.connect()
    return connector
''')

    # ---- lib/cache/__init__.py ----
    with open(f'{WORKSPACE}/lib/cache/__init__.py', 'w') as f:
        f.write('')

    # ---- lib/cache/manager.py ----
    with open(f'{WORKSPACE}/lib/cache/manager.py', 'w') as f:
        f.write('''"""Simple in-memory cache manager with TTL support."""

import time
from typing import Any, Optional, Dict


class CacheManager:
    """Thread-safe cache with time-to-live expiration."""

    def __init__(self, default_ttl: int = 300):
        self._store: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache. Returns None if expired or missing."""
        entry = self._store.get(key)
        if entry is None:
            return None
        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store a value with optional custom TTL (seconds)."""
        ttl = ttl if ttl is not None else self.default_ttl
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }

    def delete(self, key: str) -> bool:
        """Remove an entry from cache. Returns True if key existed."""
        return self._store.pop(key, None) is not None

    def clear(self) -> int:
        """Remove all entries. Returns count of removed entries."""
        count = len(self._store)
        self._store.clear()
        return count

    def stats(self) -> Dict[str, int]:
        """Return cache statistics."""
        now = time.time()
        active = sum(1 for e in self._store.values() if now <= e["expires_at"])
        return {"total_keys": len(self._store), "active_keys": active}
''')

    # ---- lib/__init__.py ----
    with open(f'{WORKSPACE}/lib/__init__.py', 'w') as f:
        f.write('')

    # ---- main.py (imports from src and lib) ----
    with open(f'{WORKSPACE}/main.py', 'w') as f:
        f.write('''"""
Main entry point for the analytics pipeline.
Imports modules from src/ and lib/ directories.
"""

from utils.helpers import format_currency, calculate_growth_rate
from models.report import SalesRecord, QuarterlyReport
from database.connector import DatabaseConnector
from cache.manager import CacheManager


def run_pipeline():
    """Execute the main analytics pipeline."""
    # Initialize cache
    cache = CacheManager(default_ttl=600)

    # Create sample records
    from datetime import date
    records = [
        SalesRecord("TXN-001", "Widget Pro", 50, 29.99, date(2025, 1, 15), "West", "Alice Park"),
        SalesRecord("TXN-002", "Gadget Plus", 30, 49.99, date(2025, 1, 22), "East", "Bob Martinez"),
        SalesRecord("TXN-003", "Widget Pro", 75, 29.99, date(2025, 2, 3), "West", "Alice Park"),
        SalesRecord("TXN-004", "Sensor Kit", 20, 89.50, date(2025, 2, 14), "North", "Carol Davis"),
        SalesRecord("TXN-005", "Gadget Plus", 45, 49.99, date(2025, 3, 1), "East", "Bob Martinez"),
    ]

    # Build report
    report = QuarterlyReport(quarter="Q1", year=2025, records=records)
    print(f"Q1 2025 Revenue: {format_currency(report.total_revenue)}")
    print(f"Transactions: {report.transaction_count}")
    print(f"Top products: {report.top_products(3)}")

    # Calculate growth vs hypothetical previous quarter
    prev_revenue = 7500.00
    growth = calculate_growth_rate(report.total_revenue, prev_revenue)
    if growth is not None:
        print(f"Growth rate: {growth:.1f}%")

    # Cache the report summary
    cache.set("q1_2025_revenue", report.total_revenue)
    print(f"Cached revenue: {format_currency(cache.get('q1_2025_revenue'))}")


if __name__ == "__main__":
    run_pipeline()
''')

    # ---- .vscode/settings.json (empty / minimal - NO python path config) ----
    vscode_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.autoSave": "afterDelay"
    }
    with open(f'{WORKSPACE}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # ---- NO .env file (agent must create it) ----
    # ---- NO python.envFile setting (agent must add it) ----
    # ---- NO python.analysis.extraPaths (agent must add it) ----

    print(f'Workspace created at: {WORKSPACE}')
    print(f'Structure:')
    for root, dirs, files in os.walk(WORKSPACE):
        level = root.replace(WORKSPACE, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # ---- Launch VSCode with workspace folder ----
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace at DISPLAY=:0')

create_initial()
