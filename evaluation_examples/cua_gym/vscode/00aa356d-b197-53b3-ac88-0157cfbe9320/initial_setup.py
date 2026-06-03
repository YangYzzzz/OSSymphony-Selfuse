"""
Initial Setup: Enable Git auto-fetch in VSCode
Task ID: vscode_we_010
Domain: vscode

Creates a Git repository workspace and opens VSCode with empty user settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_010'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # 1. Create a realistic Git repository workspace
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create some realistic project files
    with open(os.path.join(WORKSPACE, 'main.py'), 'w') as f:
        f.write('''\
"""
Inventory Management System - Main Entry Point
"""

from inventory.database import InventoryDB
from inventory.reports import generate_monthly_report


def main():
    db = InventoryDB("warehouse_data.db")
    db.connect()

    print("=== Warehouse Inventory System v2.4 ===")
    print(f"Total items tracked: {db.get_item_count()}")
    print(f"Low stock alerts: {db.get_low_stock_count()}")

    report = generate_monthly_report(db, month=3, year=2026)
    report.export_csv("reports/march_2026.csv")

    db.close()


if __name__ == "__main__":
    main()
''')

    os.makedirs(os.path.join(WORKSPACE, 'inventory'), exist_ok=True)
    with open(os.path.join(WORKSPACE, 'inventory', '__init__.py'), 'w') as f:
        f.write('"""Inventory management package."""\n')

    with open(os.path.join(WORKSPACE, 'inventory', 'database.py'), 'w') as f:
        f.write('''\
"""Database interface for inventory tracking."""

import sqlite3
from typing import List, Optional


class InventoryDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def get_item_count(self) -> int:
        cursor = self.conn.execute("SELECT COUNT(*) FROM items")
        return cursor.fetchone()[0]

    def get_low_stock_count(self) -> int:
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM items WHERE quantity < min_threshold"
        )
        return cursor.fetchone()[0]

    def close(self):
        if self.conn:
            self.conn.close()
''')

    with open(os.path.join(WORKSPACE, 'README.md'), 'w') as f:
        f.write('''\
# Warehouse Inventory System

A Python-based inventory management tool for tracking warehouse stock levels,
generating reports, and sending low-stock alerts.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Team

- Lead Developer: Priya Sharma
- Backend: David Kim, Elena Rodriguez
- QA: James O'Brien
''')

    with open(os.path.join(WORKSPACE, 'requirements.txt'), 'w') as f:
        f.write('sqlite3\npandas>=2.0\nmatplotlib>=3.7\n')

    # Initialize git repository
    subprocess.run(['git', 'init'], cwd=WORKSPACE, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'priya.sharma@example.com'], cwd=WORKSPACE, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Priya Sharma'], cwd=WORKSPACE, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=WORKSPACE, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit: inventory management system'], cwd=WORKSPACE, capture_output=True)
    # Add a remote so git fetch context makes sense
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/example-org/warehouse-inventory.git'], cwd=WORKSPACE, capture_output=True)

    print(f'Git repository created at: {WORKSPACE}')

    # 2. Ensure VSCode user settings is empty {}
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json created at: {SETTINGS_PATH}')

    # 3. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
