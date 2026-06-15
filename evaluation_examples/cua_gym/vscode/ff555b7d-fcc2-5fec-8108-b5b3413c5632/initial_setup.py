"""
Initial Setup: Configure Python debugger to auto-open Debug Console and break on first line
Task ID: vscode_py_090
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_090'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_DIR = f'{WORKSPACE}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'
MAIN_PY = f'{WORKSPACE}/main.py'
UTILS_PY = f'{WORKSPACE}/utils.py'

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
    # Create workspace directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create a realistic Python project file - main.py
    main_content = '''#!/usr/bin/env python3
"""
Sales Report Generator
Processes quarterly sales data and generates summary statistics.
"""

import os
import csv
from datetime import datetime
from utils import calculate_statistics, format_currency


DATA_FILE = "sales_q1_2025.csv"
OUTPUT_FILE = "report_summary.txt"


def load_sales_data(filepath):
    """Load sales records from a CSV file."""
    records = []
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Using sample data.")
        return get_sample_data()

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "date": row["date"],
                "product": row["product"],
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "region": row["region"],
            })
    return records


def get_sample_data():
    """Return sample sales data for testing."""
    return [
        {"date": "2025-01-05", "product": "Widget A", "quantity": 150, "unit_price": 29.99, "region": "North"},
        {"date": "2025-01-12", "product": "Widget B", "quantity": 85, "unit_price": 49.99, "region": "South"},
        {"date": "2025-01-20", "product": "Widget A", "quantity": 200, "unit_price": 29.99, "region": "East"},
        {"date": "2025-02-03", "product": "Widget C", "quantity": 60, "unit_price": 99.99, "region": "West"},
        {"date": "2025-02-14", "product": "Widget B", "quantity": 120, "unit_price": 49.99, "region": "North"},
        {"date": "2025-02-28", "product": "Widget A", "quantity": 175, "unit_price": 29.99, "region": "South"},
        {"date": "2025-03-10", "product": "Widget C", "quantity": 90, "unit_price": 99.99, "region": "East"},
        {"date": "2025-03-22", "product": "Widget B", "quantity": 110, "unit_price": 49.99, "region": "West"},
    ]


def generate_report(records):
    """Generate a summary report from sales records."""
    total_revenue = sum(r["quantity"] * r["unit_price"] for r in records)
    total_units = sum(r["quantity"] for r in records)

    # Revenue by product
    product_revenue = {}
    for r in records:
        rev = r["quantity"] * r["unit_price"]
        product_revenue[r["product"]] = product_revenue.get(r["product"], 0) + rev

    # Revenue by region
    region_revenue = {}
    for r in records:
        rev = r["quantity"] * r["unit_price"]
        region_revenue[r["region"]] = region_revenue.get(r["region"], 0) + rev

    stats = calculate_statistics([r["quantity"] * r["unit_price"] for r in records])

    report_lines = [
        "=" * 50,
        "QUARTERLY SALES REPORT - Q1 2025",
        "=" * 50,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Total Revenue: {format_currency(total_revenue)}",
        f"Total Units Sold: {total_units:,}",
        f"Average Transaction: {format_currency(stats['mean'])}",
        f"Median Transaction: {format_currency(stats['median'])}",
        "",
        "--- Revenue by Product ---",
    ]

    for product, rev in sorted(product_revenue.items()):
        report_lines.append(f"  {product}: {format_currency(rev)}")

    report_lines.append("")
    report_lines.append("--- Revenue by Region ---")

    for region, rev in sorted(region_revenue.items()):
        report_lines.append(f"  {region}: {format_currency(rev)}")

    return "\\n".join(report_lines)


def main():
    print("Loading sales data...")
    records = load_sales_data(DATA_FILE)
    print(f"Loaded {len(records)} records.")

    report = generate_report(records)
    print(report)

    with open(OUTPUT_FILE, "w") as f:
        f.write(report)
    print(f"\\nReport saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
'''
    with open(MAIN_PY, 'w') as f:
        f.write(main_content)

    # Create utils.py
    utils_content = '''"""Utility functions for the sales report generator."""

import statistics


def calculate_statistics(values):
    """Calculate basic statistics for a list of numeric values."""
    if not values:
        return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0,
        "min": min(values),
        "max": max(values),
    }


def format_currency(amount):
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"
'''
    with open(UTILS_PY, 'w') as f:
        f.write(utils_content)

    # Create basic launch.json WITHOUT stopOnEntry and without console set to internalConsole
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "cwd": "${workspaceFolder}",
                "env": {},
                "justMyCode": True
            }
        ]
    }

    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)

    print(f'Initial workspace created: {WORKSPACE}')
    print(f'  main.py: {MAIN_PY}')
    print(f'  utils.py: {UTILS_PY}')
    print(f'  launch.json: {LAUNCH_JSON}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
