"""
Initial Setup: Enable pylint as the Python linter in VSCode and disable pylance type checking.
Task ID: vscode_lp_002
Domain: vscode

Creates:
- A Python project workspace at /home/user/workspace/
- VSCode settings with python.analysis.typeCheckingMode = "basic" (pre-existing)
- Pylint installed in the system Python
- VSCode opened with the workspace
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_002'
WORKSPACE_DIR = f'{WORKDIR}/workspace'
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


def create_workspace():
    """Create a realistic Python project workspace."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main application file
    main_py = '''\
"""Sales Analytics Dashboard - Main Entry Point"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class SalesRecord:
    """Represents a single sales transaction."""

    def __init__(self, date: str, product: str, quantity: int, unit_price: float, region: str):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.region = region

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

    def __repr__(self) -> str:
        return f"SalesRecord({self.date:%Y-%m-%d}, {self.product}, ${self.total:.2f})"


def load_sales_data(filepath: str) -> List[SalesRecord]:
    """Load sales records from a CSV file."""
    records = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(SalesRecord(
                date=row["date"],
                product=row["product"],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                region=row["region"],
            ))
    return records


def aggregate_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """Aggregate total sales by region."""
    totals: Dict[str, float] = {}
    for rec in records:
        totals[rec.region] = totals.get(rec.region, 0.0) + rec.total
    return totals


def generate_summary(records: List[SalesRecord]) -> str:
    """Generate a text summary of sales performance."""
    if not records:
        return "No sales data available."
    total_revenue = sum(r.total for r in records)
    avg_order = total_revenue / len(records)
    by_region = aggregate_by_region(records)
    top_region = max(by_region, key=by_region.get)

    lines = [
        "=== Sales Performance Summary ===",
        f"Total Records: {len(records)}",
        f"Total Revenue: ${total_revenue:,.2f}",
        f"Average Order Value: ${avg_order:,.2f}",
        f"Top Region: {top_region} (${by_region[top_region]:,.2f})",
        "",
        "Revenue by Region:",
    ]
    for region, amount in sorted(by_region.items(), key=lambda x: -x[1]):
        lines.append(f"  {region}: ${amount:,.2f}")

    return "\\n".join(lines)


if __name__ == "__main__":
    data_file = os.path.join(DATA_DIR, "q1_sales.csv")
    if os.path.exists(data_file):
        sales = load_sales_data(data_file)
        print(generate_summary(sales))
    else:
        print(f"Data file not found: {data_file}")
'''
    with open(f'{WORKSPACE_DIR}/main.py', 'w') as f:
        f.write(main_py)

    # Utils module
    os.makedirs(f'{WORKSPACE_DIR}/utils', exist_ok=True)
    utils_init = '''\
"""Utility functions for the Sales Analytics Dashboard."""

from .formatters import format_currency, format_percentage
from .validators import validate_date_range
'''
    with open(f'{WORKSPACE_DIR}/utils/__init__.py', 'w') as f:
        f.write(utils_init)

    formatters_py = '''\
"""Formatting utilities for display output."""


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a number as currency."""
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a decimal as percentage."""
    return f"{value * 100:.{decimals}f}%"


def format_table_row(columns: list, widths: list) -> str:
    """Format a row with fixed-width columns."""
    parts = []
    for col, width in zip(columns, widths):
        parts.append(str(col).ljust(width))
    return " | ".join(parts)
'''
    with open(f'{WORKSPACE_DIR}/utils/formatters.py', 'w') as f:
        f.write(formatters_py)

    validators_py = '''\
"""Input validation utilities."""

from datetime import datetime


def validate_date_range(start: str, end: str) -> bool:
    """Validate that start date is before end date."""
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        return start_dt < end_dt
    except ValueError:
        return False


def validate_positive_number(value) -> bool:
    """Check that value is a positive number."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False
'''
    with open(f'{WORKSPACE_DIR}/utils/validators.py', 'w') as f:
        f.write(validators_py)

    # Sample data directory
    os.makedirs(f'{WORKSPACE_DIR}/data', exist_ok=True)
    csv_content = '''\
date,product,quantity,unit_price,region
2025-01-05,Widget Pro,12,45.99,North America
2025-01-08,Gadget Plus,8,89.50,Europe
2025-01-12,Widget Pro,20,45.99,Asia Pacific
2025-01-15,Connector X,15,23.75,North America
2025-01-18,Gadget Plus,5,89.50,North America
2025-01-22,Widget Pro,10,45.99,Europe
2025-01-25,Connector X,30,23.75,Asia Pacific
2025-02-01,Gadget Plus,12,89.50,North America
2025-02-05,Widget Pro,18,45.99,Europe
2025-02-10,Connector X,25,23.75,North America
2025-02-14,Widget Pro,7,45.99,Asia Pacific
2025-02-18,Gadget Plus,9,89.50,Europe
'''
    with open(f'{WORKSPACE_DIR}/data/q1_sales.csv', 'w') as f:
        f.write(csv_content)

    # Requirements file
    requirements = '''\
pylint>=3.0.0
pytest>=7.4.0
black>=23.0.0
'''
    with open(f'{WORKSPACE_DIR}/requirements.txt', 'w') as f:
        f.write(requirements)

    print(f'Workspace created: {WORKSPACE_DIR}')


def configure_vscode_settings():
    """Set up VSCode settings with initial state: typeCheckingMode = basic."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Initial settings: only typeCheckingMode is set to basic
    # Do NOT include linting settings - those are what the task asks to add
    settings = {
        "python.analysis.typeCheckingMode": "basic",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.autoSave": "afterDelay",
        "workbench.colorTheme": "Default Dark Modern"
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings created: {SETTINGS_PATH}')


def install_pylint():
    """Ensure pylint is installed."""
    result = subprocess.run(
        ['pip3', 'install', 'pylint'],
        capture_output=True,
        text=True,
    )
    print(f'pip3 install pylint: returncode={result.returncode}')
    if result.stdout:
        # Print last line of output for confirmation
        lines = result.stdout.strip().splitlines()
        if lines:
            print(f'  {lines[-1]}')
    # Verify via python -m pylint (more reliable than bare command)
    result2 = subprocess.run(
        ['python3', '-m', 'pylint', '--version'],
        capture_output=True,
        text=True,
    )
    if result2.returncode == 0:
        print(f'Pylint installed: {result2.stdout.strip().splitlines()[0]}')
    else:
        print('Warning: pylint may not be available via python3 -m pylint')


def main():
    create_workspace()
    configure_vscode_settings()
    install_pylint()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
