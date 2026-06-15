"""
Initial Setup: Configure VSCode workbench layout settings
Task ID: vscode_we_044
Domain: vscode

Creates a workspace folder and opens VSCode with default/empty user settings.
The settings.json is left empty so the agent must configure the 4 required settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_044'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # Create a workspace directory with some sample project files
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a small sample project so the explorer has something to show
    src_dir = os.path.join(WORKSPACE_DIR, 'src', 'utils')
    os.makedirs(src_dir, exist_ok=True)

    # Main application file
    with open(os.path.join(WORKSPACE_DIR, 'src', 'app.py'), 'w') as f:
        f.write('''\
"""Inventory Management Application"""

from utils.database import connect_db
from utils.helpers import format_currency


def get_inventory_summary():
    """Return summary of current inventory levels."""
    db = connect_db()
    items = db.execute("SELECT name, quantity, price FROM products").fetchall()
    total_value = sum(qty * price for _, qty, price in items)
    return {
        "total_items": len(items),
        "total_value": format_currency(total_value),
        "items": items,
    }


def main():
    summary = get_inventory_summary()
    print(f"Inventory: {summary['total_items']} products")
    print(f"Total value: {summary['total_value']}")


if __name__ == "__main__":
    main()
''')

    with open(os.path.join(src_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(src_dir, 'database.py'), 'w') as f:
        f.write('''\
"""Database connection utilities."""
import sqlite3

DB_PATH = "inventory.db"


def connect_db():
    return sqlite3.connect(DB_PATH)
''')

    with open(os.path.join(src_dir, 'helpers.py'), 'w') as f:
        f.write('''\
"""Utility helper functions."""


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def truncate_string(s: str, max_len: int = 50) -> str:
    if len(s) <= max_len:
        return s
    return s[:max_len - 3] + "..."
''')

    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write('''\
# Inventory Manager

A simple inventory tracking application for small businesses.

## Setup

```bash
pip install -r requirements.txt
python src/app.py
```
''')

    with open(os.path.join(WORKSPACE_DIR, 'requirements.txt'), 'w') as f:
        f.write('sqlite3\nrich>=13.0\n')

    # Ensure VSCode user config directory exists with empty settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Workspace created at: {WORKSPACE_DIR}')
    print(f'Settings file (empty): {SETTINGS_PATH}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
