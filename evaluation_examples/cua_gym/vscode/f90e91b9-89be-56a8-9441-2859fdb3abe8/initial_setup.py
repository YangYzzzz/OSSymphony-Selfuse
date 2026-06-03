"""
Initial Setup: Enable word wrap in VSCode
Task ID: vscode_stu_006
Domain: vscode

Sets editor.wordWrap to 'off' in VSCode settings, creates a sample workspace
with a long-line file so the user can see the effect, and opens VSCode.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")
TASK_ID = "vscode_stu_006"


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_workspace():
    """Create a realistic workspace with files containing long lines."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a Python file with intentionally long lines to demonstrate word wrap need
    main_py = os.path.join(WORKSPACE_DIR, "data_analysis.py")
    with open(main_py, "w") as f:
        f.write('''"""
Data Analysis Pipeline for Q1 2025 Sales Report
Department: Business Intelligence
Author: Sarah Chen
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Configuration constants for the quarterly sales analysis pipeline - these settings control data filtering, aggregation windows, and output formatting preferences
ANALYSIS_CONFIG = {"start_date": "2025-01-01", "end_date": "2025-03-31", "departments": ["Engineering", "Marketing", "Sales", "Operations", "Finance"], "metrics": ["revenue", "cost", "margin", "headcount"]}

DEPARTMENT_BUDGETS = {"Engineering": 2_450_000, "Marketing": 1_875_000, "Sales": 3_200_000, "Operations": 950_000, "Finance": 780_000, "Human Resources": 620_000, "Legal": 540_000, "Customer Support": 1_100_000}


def calculate_quarterly_revenue_by_department(transactions_df, department_column="dept_name", revenue_column="amount", date_column="transaction_date", include_pending=False):
    """Calculate the total quarterly revenue grouped by department, with optional inclusion of pending transactions that have not yet been finalized in the accounting system."""
    filtered = transactions_df[(transactions_df[date_column] >= ANALYSIS_CONFIG["start_date"]) & (transactions_df[date_column] <= ANALYSIS_CONFIG["end_date"])]
    if not include_pending:
        filtered = filtered[filtered["status"] != "pending"]
    return filtered.groupby(department_column)[revenue_column].sum().reset_index().rename(columns={revenue_column: "total_revenue"}).sort_values("total_revenue", ascending=False)


def generate_performance_summary(department_name, actual_revenue, budget, headcount, previous_quarter_revenue, target_growth_rate=0.15):
    """Generate a comprehensive performance summary string for a single department including budget utilization, per-capita revenue, quarter-over-quarter growth, and target achievement status."""
    utilization = (actual_revenue / budget) * 100 if budget > 0 else 0
    per_capita = actual_revenue / headcount if headcount > 0 else 0
    growth = ((actual_revenue - previous_quarter_revenue) / previous_quarter_revenue) * 100 if previous_quarter_revenue > 0 else 0
    target_met = "ACHIEVED" if growth >= target_growth_rate * 100 else "BELOW TARGET"
    return f"{department_name}: Revenue ${actual_revenue:,.2f} | Budget Utilization {utilization:.1f}% | Per Capita ${per_capita:,.2f} | QoQ Growth {growth:+.1f}% | Status: {target_met}"


def validate_transaction_records(records, required_fields=None, max_amount_threshold=500000, flag_duplicates=True, duplicate_window_hours=24):
    """Validate a list of transaction records checking for required fields, amount thresholds, duplicate detection within a configurable time window, and data type consistency across all entries."""
    if required_fields is None:
        required_fields = ["transaction_id", "amount", "date", "department", "category", "approved_by", "cost_center"]
    validation_results = []
    for record in records:
        missing = [f for f in required_fields if f not in record or record[f] is None]
        if missing:
            validation_results.append({"id": record.get("transaction_id", "UNKNOWN"), "status": "INVALID", "reason": f"Missing fields: {', '.join(missing)}"})
    return validation_results


if __name__ == "__main__":
    print("Data Analysis Pipeline - Q1 2025")
    print("=" * 80)
    print(f"Analysis period: {ANALYSIS_CONFIG['start_date']} to {ANALYSIS_CONFIG['end_date']}")
    print(f"Departments under review: {', '.join(ANALYSIS_CONFIG['departments'])}")
    print(f"Metrics tracked: {', '.join(ANALYSIS_CONFIG['metrics'])}")
''')

    # Create a README with long lines
    readme = os.path.join(WORKSPACE_DIR, "README.md")
    with open(readme, "w") as f:
        f.write('''# Q1 2025 Sales Analysis Pipeline

## Overview

This project contains the data analysis pipeline used by the Business Intelligence team to generate quarterly sales performance reports. The pipeline processes raw transaction data from multiple departments and produces comprehensive summaries including revenue breakdowns, budget utilization metrics, per-capita productivity scores, and quarter-over-quarter growth comparisons.

## Requirements

- Python 3.9 or higher with pandas, numpy, and matplotlib installed via pip. The pipeline also requires access to the internal PostgreSQL database server at db.internal.company.com:5432 with read-only credentials stored in the environment variable DATABASE_URL.
- At least 4GB of available RAM for processing the full quarterly dataset, which typically contains between 500,000 and 2,000,000 individual transaction records depending on the business volume during the analysis period.

## Usage

Run the main analysis script from the project root directory. The script accepts several command-line arguments including --start-date, --end-date, --departments (comma-separated list), --output-format (csv, xlsx, or json), and --include-pending (boolean flag to include unfinalized transactions in the calculations).
''')

    print(f"Workspace created at {WORKSPACE_DIR}")


def main():
    # Step 1: Set word wrap to OFF (initial state)
    update_settings({
        "editor.wordWrap": "off"
    })
    print(f"Settings updated: editor.wordWrap = 'off'")

    # Step 2: Create workspace with files that have long lines
    create_workspace()

    # Step 3: Launch VSCode with the workspace folder and open the long-line file
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{WORKSPACE_DIR}/data_analysis.py"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


main()
