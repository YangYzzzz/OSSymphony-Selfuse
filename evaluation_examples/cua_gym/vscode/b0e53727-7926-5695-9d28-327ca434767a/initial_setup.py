"""
Initial Setup: Set VSCode color theme to Solarized Dark and icon theme to vs-seti
Task ID: vscode_gf2_008
Domain: vscode

Creates a realistic developer workspace with project files and opens VSCode.
Settings are left at defaults (no Solarized Dark theme, no vs-seti icon theme).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_008'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'workspace')


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


def create_workspace_files():
    """Create a realistic developer project workspace."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main Python application file
    main_py = '''\
"""
Inventory Management System - Main Entry Point
Author: Sarah Chen
Created: 2025-11-02
"""

import argparse
from pathlib import Path

from inventory.database import InventoryDB
from inventory.reports import generate_monthly_report
from inventory.utils import setup_logging


def main():
    parser = argparse.ArgumentParser(description="Inventory Management CLI")
    parser.add_argument("--db", default="inventory.db", help="Database path")
    parser.add_argument("--report", action="store_true", help="Generate monthly report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logger = setup_logging(verbose=args.verbose)
    db = InventoryDB(Path(args.db))

    if args.report:
        report = generate_monthly_report(db)
        logger.info(f"Report generated: {report.output_path}")
    else:
        logger.info("Starting inventory management system...")
        db.connect()
        print(f"Connected to database: {args.db}")
        print(f"Total items: {db.count_items()}")


if __name__ == "__main__":
    main()
'''

    # Inventory module
    os.makedirs(os.path.join(PROJECT_DIR, 'inventory'), exist_ok=True)

    init_py = '''\
"""Inventory Management Package"""

__version__ = "1.3.2"
__author__ = "Sarah Chen"
'''

    database_py = '''\
"""
Database abstraction layer for inventory management.
Supports SQLite and PostgreSQL backends.
"""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class InventoryItem:
    item_id: int
    name: str
    category: str
    quantity: int
    unit_price: float
    supplier: str
    last_updated: datetime
    warehouse_location: str


class InventoryDB:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._conn = None

    def connect(self):
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                unit_price REAL NOT NULL,
                supplier TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                warehouse_location TEXT
            )
        """)
        self._conn.commit()

    def count_items(self) -> int:
        cursor = self._conn.execute("SELECT COUNT(*) FROM items")
        return cursor.fetchone()[0]

    def add_item(self, item: InventoryItem) -> int:
        cursor = self._conn.execute(
            """INSERT INTO items (name, category, quantity, unit_price, supplier, warehouse_location)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (item.name, item.category, item.quantity,
             item.unit_price, item.supplier, item.warehouse_location)
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_items_by_category(self, category: str) -> List[InventoryItem]:
        cursor = self._conn.execute(
            "SELECT * FROM items WHERE category = ? ORDER BY name", (category,)
        )
        return [self._row_to_item(row) for row in cursor.fetchall()]

    def get_low_stock(self, threshold: int = 10) -> List[InventoryItem]:
        cursor = self._conn.execute(
            "SELECT * FROM items WHERE quantity < ? ORDER BY quantity", (threshold,)
        )
        return [self._row_to_item(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_item(row) -> InventoryItem:
        return InventoryItem(
            item_id=row["item_id"],
            name=row["name"],
            category=row["category"],
            quantity=row["quantity"],
            unit_price=row["unit_price"],
            supplier=row["supplier"],
            last_updated=datetime.fromisoformat(row["last_updated"]),
            warehouse_location=row["warehouse_location"],
        )
'''

    utils_py = '''\
"""Utility functions for the inventory management system."""

import logging
from pathlib import Path


def setup_logging(verbose: bool = False, log_file: str = "inventory.log") -> logging.Logger:
    logger = logging.getLogger("inventory")
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def validate_quantity(quantity: int) -> bool:
    return isinstance(quantity, int) and quantity >= 0
'''

    reports_py = '''\
"""Report generation module for inventory analytics."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class MonthlyReport:
    output_path: Path
    total_items: int
    total_value: float
    categories: Dict[str, int]
    low_stock_items: List[str]
    generated_at: datetime


def generate_monthly_report(db) -> MonthlyReport:
    """Generate a comprehensive monthly inventory report."""
    items = db.get_all_items() if hasattr(db, 'get_all_items') else []
    total_value = sum(item.quantity * item.unit_price for item in items)

    categories = {}
    for item in items:
        categories[item.category] = categories.get(item.category, 0) + 1

    low_stock = [item.name for item in db.get_low_stock(threshold=10)]

    report_path = Path(f"reports/monthly_{datetime.now().strftime('%Y_%m')}.txt")
    report_path.parent.mkdir(exist_ok=True)

    return MonthlyReport(
        output_path=report_path,
        total_items=len(items),
        total_value=total_value,
        categories=categories,
        low_stock_items=low_stock,
        generated_at=datetime.now(),
    )
'''

    # Config file
    config_json = '''\
{
    "database": {
        "backend": "sqlite",
        "path": "inventory.db",
        "pool_size": 5
    },
    "logging": {
        "level": "INFO",
        "file": "inventory.log",
        "rotation": "daily"
    },
    "warehouse": {
        "locations": ["A1", "A2", "B1", "B2", "C1"],
        "default_location": "A1"
    },
    "notifications": {
        "low_stock_threshold": 10,
        "email_alerts": true,
        "recipients": ["sarah.chen@company.com", "ops-team@company.com"]
    }
}
'''

    # README
    readme = '''\
# Inventory Management System

A command-line inventory management tool built with Python.

## Features

- SQLite/PostgreSQL database backend
- Monthly report generation
- Low stock alerts
- Multi-warehouse support

## Usage

```bash
python main.py --db inventory.db
python main.py --report --verbose
```

## Project Structure

```
workspace/
├── main.py
├── config.json
├── inventory/
│   ├── __init__.py
│   ├── database.py
│   ├── reports.py
│   └── utils.py
└── tests/
    └── test_database.py
```
'''

    # Test file
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    test_database_py = '''\
"""Unit tests for the inventory database module."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from inventory.database import InventoryDB, InventoryItem


class TestInventoryDB(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db = InventoryDB(Path(self.temp_db.name))
        self.db.connect()

    def test_count_items_empty(self):
        self.assertEqual(self.db.count_items(), 0)

    def test_add_and_count(self):
        from datetime import datetime
        item = InventoryItem(
            item_id=0, name="Widget A", category="Hardware",
            quantity=50, unit_price=12.99, supplier="Acme Corp",
            last_updated=datetime.now(), warehouse_location="A1"
        )
        self.db.add_item(item)
        self.assertEqual(self.db.count_items(), 1)

    def test_get_low_stock(self):
        from datetime import datetime
        for i, qty in enumerate([5, 15, 3, 20], start=1):
            item = InventoryItem(
                item_id=0, name=f"Item {i}", category="Parts",
                quantity=qty, unit_price=9.99, supplier="SupplierX",
                last_updated=datetime.now(), warehouse_location="B1"
            )
            self.db.add_item(item)
        low = self.db.get_low_stock(threshold=10)
        self.assertEqual(len(low), 2)


if __name__ == "__main__":
    unittest.main()
'''

    # Write all files
    files = {
        os.path.join(PROJECT_DIR, 'main.py'): main_py,
        os.path.join(PROJECT_DIR, 'inventory', '__init__.py'): init_py,
        os.path.join(PROJECT_DIR, 'inventory', 'database.py'): database_py,
        os.path.join(PROJECT_DIR, 'inventory', 'utils.py'): utils_py,
        os.path.join(PROJECT_DIR, 'inventory', 'reports.py'): reports_py,
        os.path.join(PROJECT_DIR, 'config.json'): config_json,
        os.path.join(PROJECT_DIR, 'README.md'): readme,
        os.path.join(PROJECT_DIR, 'tests', 'test_database.py'): test_database_py,
    }

    for filepath, content in files.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  Created: {filepath}')


def setup_vscode_settings():
    """Set up VSCode with default settings (NO Solarized Dark, NO vs-seti)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Default settings — explicitly using Default Dark Modern (the VSCode default)
    # The task requires the agent to change these to Solarized Dark and vs-seti
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'  VSCode settings written: {SETTINGS_PATH}')


def main():
    print('Creating workspace files...')
    create_workspace_files()

    print('Setting up VSCode configuration...')
    setup_vscode_settings()

    # Open VSCode with the workspace directory
    print('Launching VSCode...')
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')
    print(f'Initial setup complete for {TASK_ID}')


main()
