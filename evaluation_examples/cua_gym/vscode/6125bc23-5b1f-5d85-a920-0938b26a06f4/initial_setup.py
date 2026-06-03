"""
Initial Setup: Configure editor rulers and render whitespace
Task ID: vscode_we_025
Domain: vscode

Creates a workspace with sample files and ensures VSCode settings.json
is empty (no rulers, no renderWhitespace). Opens VSCode with the workspace.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
TASK_ID = 'vscode_we_025'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')


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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings.json (no rulers, no renderWhitespace)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Settings file created: {SETTINGS_PATH} (empty)')

    # Create a workspace directory with sample files for context
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample Python file
    sample_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(sample_py, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""Sales report generator for Q1 2025."""

import csv
from datetime import datetime


def load_sales_data(filepath: str) -> list:
    """Load sales records from a CSV file and return as list of dicts."""
    records = []
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append({
                "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                "product": row["product"],
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "region": row["region"],
            })
    return records


def calculate_revenue(records: list) -> dict:
    """Calculate total revenue by region."""
    revenue_by_region = {}
    for record in records:
        region = record["region"]
        total = record["quantity"] * record["unit_price"]
        revenue_by_region[region] = revenue_by_region.get(region, 0.0) + total
    return revenue_by_region


def generate_report(revenue_data: dict, output_path: str):
    """Generate a formatted text report of regional revenue."""
    with open(output_path, "w") as f:
        f.write("=" * 50 + "\\n")
        f.write("  Q1 2025 Regional Sales Report\\n")
        f.write("=" * 50 + "\\n\\n")
        grand_total = 0.0
        for region, amount in sorted(revenue_data.items()):
            f.write(f"  {region:<20} ${amount:>12,.2f}\\n")
            grand_total += amount
        f.write("\\n" + "-" * 50 + "\\n")
        f.write(f"  {'GRAND TOTAL':<20} ${grand_total:>12,.2f}\\n")


if __name__ == "__main__":
    data = load_sales_data("sales_q1_2025.csv")
    revenue = calculate_revenue(data)
    generate_report(revenue, "report_q1_2025.txt")
    print("Report generated successfully.")
''')

    # Create a sample README
    readme = os.path.join(WORKSPACE_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''# Sales Report Generator

A Python utility for generating quarterly sales reports from CSV data.

## Usage

```bash
python main.py
```

## Input Format

The input CSV file should have the following columns:
- date (YYYY-MM-DD)
- product
- quantity
- unit_price
- region

## Output

Generates a formatted text report showing revenue by region.
''')

    print(f'Workspace created: {WORKSPACE_DIR}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
