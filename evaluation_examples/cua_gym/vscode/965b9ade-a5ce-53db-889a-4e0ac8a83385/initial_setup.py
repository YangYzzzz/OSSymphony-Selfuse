"""
Initial Setup: Configure VSCode to use Python black formatter with custom config
Task ID: vscode_py_094
Domain: vscode

Creates a Python project with:
- Multiple .py files using single quotes
- pyproject.toml WITHOUT [tool.black] section
- VSCode settings with basic Python config (no Black formatter set)
- Opens VSCode with the workspace
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_094'
PROJECT_DIR = f'{WORKDIR}/workspace'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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


def create_project_files():
    """Create a realistic Python project with single-quoted strings."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # main.py - entry point using single quotes
    main_py = """\
#!/usr/bin/env python3
'''Main entry point for the inventory management system.'''

import sys
from pathlib import Path

from inventory.database import InventoryDatabase
from inventory.reports import generate_monthly_report
from inventory.utils import setup_logging


def main():
    '''Initialize and run the inventory management application.'''
    logger = setup_logging('inventory_app')
    logger.info('Starting Inventory Management System v2.1.0')

    db_path = Path.home() / '.inventory' / 'warehouse.db'
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info('Created database directory at %s', str(db_path.parent))

    db = InventoryDatabase(str(db_path))
    db.initialize_tables()

    categories = ['electronics', 'furniture', 'office_supplies', 'raw_materials']
    for category in categories:
        count = db.get_item_count(category)
        logger.info('Category %s: %d items in stock', category, count)

    if '--report' in sys.argv:
        report_path = generate_monthly_report(db, output_dir='/tmp/reports')
        logger.info('Monthly report generated: %s', report_path)

    logger.info('Application shutdown complete')
    return 0


if __name__ == '__main__':
    sys.exit(main())
"""

    # inventory/__init__.py
    inventory_init = """\
'''Inventory management package for warehouse operations.'''

__version__ = '2.1.0'
__author__ = 'Sarah Chen'
"""

    # inventory/database.py
    database_py = """\
'''Database abstraction layer for inventory management.'''

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class InventoryDatabase:
    '''Manages connections and queries to the inventory SQLite database.'''

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def initialize_tables(self) -> None:
        '''Create required tables if they do not exist.'''
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                unit_price REAL NOT NULL,
                supplier_id INTEGER,
                last_updated TEXT NOT NULL,
                warehouse_location TEXT DEFAULT 'A-01'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                txn_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                performed_by TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')
        conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        '''Return existing connection or create a new one.'''
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def get_item_count(self, category: str) -> int:
        '''Return the number of items in a given category.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM items WHERE category = ?',
            (category,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def add_item(self, name: str, category: str, quantity: int,
                 unit_price: float, supplier_id: int = None) -> int:
        '''Insert a new item and return its ID.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO items (name, category, quantity, unit_price, supplier_id, last_updated) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (name, category, quantity, unit_price, supplier_id, now)
        )
        conn.commit()
        return cursor.lastrowid

    def get_low_stock_items(self, threshold: int = 10) -> List[Tuple]:
        '''Fetch items whose quantity is below the given threshold.'''
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT item_id, name, category, quantity FROM items WHERE quantity < ?',
            (threshold,)
        )
        return cursor.fetchall()

    def close(self) -> None:
        '''Close the database connection.'''
        if self.connection:
            self.connection.close()
            self.connection = None
"""

    # inventory/reports.py
    reports_py = """\
'''Report generation utilities for inventory data.'''

import csv
import os
from datetime import datetime
from typing import Optional


def generate_monthly_report(db, output_dir: str = '/tmp/reports') -> str:
    '''Generate a CSV report of current inventory levels.'''
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_name = f'inventory_report_{timestamp}.csv'
    report_path = os.path.join(output_dir, report_name)

    conn = db._get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, category, quantity, unit_price FROM items ORDER BY category')
    rows = cursor.fetchall()

    headers = ['Item Name', 'Category', 'Quantity', 'Unit Price', 'Total Value']
    with open(report_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for name, category, quantity, price in rows:
            total = quantity * price
            writer.writerow([name, category, quantity, f'{price:.2f}', f'{total:.2f}'])

    return report_path


def generate_low_stock_alert(db, threshold: int = 10) -> Optional[str]:
    '''Generate an alert file listing items below stock threshold.'''
    low_items = db.get_low_stock_items(threshold)
    if not low_items:
        return None

    alert_path = '/tmp/low_stock_alert.txt'
    with open(alert_path, 'w') as f:
        f.write(f'Low Stock Alert - {datetime.now().strftime("%Y-%m-%d %H:%M")}\\n')
        f.write('=' * 60 + '\\n\\n')
        for item_id, name, category, quantity in low_items:
            f.write(f'  [{category}] {name} (ID: {item_id}) - Only {quantity} remaining\\n')
    return alert_path
"""

    # inventory/utils.py
    utils_py = """\
'''Utility functions for the inventory management system.'''

import logging
import os
from typing import Optional


def setup_logging(name: str, level: str = 'INFO') -> logging.Logger:
    '''Configure and return a logger with console and file handlers.'''
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_dir = os.path.join(os.path.expanduser('~'), '.inventory', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f'{name}.log')
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def format_currency(amount: float, currency: str = 'USD') -> str:
    '''Format a numeric amount as a currency string.'''
    symbols = {'USD': '$', 'EUR': '\\u20ac', 'GBP': '\\u00a3', 'JPY': '\\u00a5'}
    symbol = symbols.get(currency, currency + ' ')
    return f'{symbol}{amount:,.2f}'


def validate_quantity(value) -> Optional[int]:
    '''Parse and validate a quantity value; return None if invalid.'''
    try:
        qty = int(value)
        if qty < 0:
            return None
        return qty
    except (ValueError, TypeError):
        return None
"""

    # Write all project files
    files = {
        f'{PROJECT_DIR}/main.py': main_py,
        f'{PROJECT_DIR}/inventory/__init__.py': inventory_init,
        f'{PROJECT_DIR}/inventory/database.py': database_py,
        f'{PROJECT_DIR}/inventory/reports.py': reports_py,
        f'{PROJECT_DIR}/inventory/utils.py': utils_py,
    }

    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f'Created: {path}')


def create_pyproject_toml():
    """Create pyproject.toml WITHOUT [tool.black] section."""
    content = """\
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "inventory-manager"
version = "2.1.0"
description = "Warehouse inventory management system"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Sarah Chen", email = "sarah.chen@techcorp.io"},
]
dependencies = [
    "click>=8.0",
    "rich>=13.0",
]

[project.scripts]
inventory = "main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
"""
    path = f'{PROJECT_DIR}/pyproject.toml'
    with open(path, 'w') as f:
        f.write(content)
    print(f'Created: {path}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT Black as default formatter."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Merge basic Python settings - no formatter configured
    settings.update({
        'security.workspace.trust.enabled': False,
        'security.workspace.trust.startupPrompt': 'never',
        'security.workspace.trust.emptyWindow': False,
        'python.defaultInterpreterPath': '/usr/bin/python3',
        'editor.fontSize': 14,
        'editor.tabSize': 4,
        'editor.insertSpaces': True,
        'files.autoSave': 'afterDelay',
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written: {SETTINGS_PATH}')


def main():
    create_project_files()
    create_pyproject_toml()
    setup_vscode_settings()

    # Launch VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
