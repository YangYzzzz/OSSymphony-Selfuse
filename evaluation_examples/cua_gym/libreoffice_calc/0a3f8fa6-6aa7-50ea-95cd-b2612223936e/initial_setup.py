"""
Initial Setup: VSCode flake8 problem matcher task
Task ID: vscode_td_030
Domain: vscode (libreoffice_calc label but actually vscode)
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-linter-demo')


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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create realistic Python files with some flake8-detectable issues
    # main.py - entry point with a few style issues
    main_py = '''\
"""Python Linter Demo - Main Entry Point"""

import sys
import os
from utils.data_loader import load_dataset
from utils.formatter import format_report


def main():
    """Run the data analysis pipeline."""
    dataset_path = "data/sales_q1_2025.csv"

    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        sys.exit(1)

    data = load_dataset(dataset_path)
    report = format_report(data)
    print(report)


if __name__ == "__main__":
    main()
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # utils/__init__.py
    utils_dir = os.path.join(PROJECT_DIR, 'utils')
    os.makedirs(utils_dir, exist_ok=True)
    with open(os.path.join(utils_dir, '__init__.py'), 'w') as f:
        f.write('"""Utility modules for data processing."""\n')

    # utils/data_loader.py - has some intentional style issues for flake8
    data_loader_py = '''\
"""Data loading utilities for CSV and JSON files."""

import csv
import json
from typing import List, Dict, Any


def load_dataset(filepath: str) -> List[Dict[str, Any]]:
    """Load a CSV dataset and return as list of dictionaries."""
    results = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results


def load_json_config(filepath: str) -> Dict[str, Any]:
    """Load JSON configuration file."""
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config


def validate_dataset(data: List[Dict[str, Any]],required_fields: List[str]) -> bool:
    """Validate that all required fields exist in each record."""
    for record in data:
        for field in required_fields:
            if field not in record:
                return False
    return True
'''
    with open(os.path.join(utils_dir, 'data_loader.py'), 'w') as f:
        f.write(data_loader_py)

    # utils/formatter.py
    formatter_py = '''\
"""Report formatting utilities."""

from typing import List, Dict, Any


def format_report(data: List[Dict[str, Any]]) -> str:
    """Format dataset into a readable report string."""
    if not data:
        return "No data available."

    headers = list(data[0].keys())
    col_widths = {h: max(len(h), max(len(str(row.get(h, ""))) for row in data)) for h in headers}

    lines = []
    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    lines.append(header_line)
    lines.append("-" * len(header_line))

    for row in data:
        line = " | ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers)
        lines.append(line)

    return "\\n".join(lines)


def summarize(data: List[Dict[str,Any]], numeric_field: str) -> Dict[str, float]:
    """Calculate summary statistics for a numeric field."""
    values = []
    for row in data:
        try:
            values.append(float(row[numeric_field]))
        except (KeyError, ValueError):
            continue

    if not values:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}

    return {
        "count": len(values),
        "sum": sum(values),
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }
'''
    with open(os.path.join(utils_dir, 'formatter.py'), 'w') as f:
        f.write(formatter_py)

    # Create a sample data directory
    data_dir = os.path.join(PROJECT_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    sample_csv = '''\
name,department,sales,region,quarter
Sarah Chen,Engineering,45230.50,West,Q1
Marcus Johnson,Marketing,38750.00,East,Q1
Emily Rodriguez,Sales,52100.75,South,Q1
David Kim,Engineering,41890.25,West,Q1
Lisa Thompson,Marketing,35600.00,North,Q1
James Wilson,Sales,48920.50,East,Q1
Anna Martinez,Engineering,43150.75,South,Q1
Robert Brown,Marketing,37200.00,West,Q1
'''
    with open(os.path.join(data_dir, 'sales_q1_2025.csv'), 'w') as f:
        f.write(sample_csv)

    # Create a README
    readme = '''\
# Python Linter Demo

A sample Python project for demonstrating linting with flake8.

## Setup

```bash
pip install flake8
```

## Usage

```bash
python main.py
```
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Install flake8 if not already installed
    subprocess.run(['pip3', 'install', 'flake8'], capture_output=True)

    # Ensure NO .vscode folder exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print('No .vscode folder exists (as required)')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
