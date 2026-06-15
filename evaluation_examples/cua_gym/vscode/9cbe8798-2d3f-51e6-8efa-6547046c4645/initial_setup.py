"""
Initial Setup: Enable automatic trimming of trailing whitespace when saving files.
Task ID: vscode_code_059
Domain: vs_code

Creates a VSCode environment with a Python workspace file that has trailing
whitespace. The settings.json does NOT have files.trimTrailingWhitespace enabled.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_059'
WORKSPACE_DIR = f'{WORKDIR}/{TASK_ID}_workspace'
VSCODE_USER = os.path.join(os.path.expanduser('~'), '.config', 'Code', 'User')
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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Handle JSONC (strip comments)
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings: dict):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # 1. Set up VSCode settings — ensure files.trimTrailingWhitespace is NOT set (or false)
    settings = load_settings()
    # Remove the key if it exists, so the task is to add it
    settings.pop('files.trimTrailingWhitespace', None)
    save_settings(settings)
    print(f'Settings updated: removed files.trimTrailingWhitespace if present')

    # 2. Create a workspace directory with realistic Python files containing trailing whitespace
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python script with trailing whitespace on multiple lines
    main_py = f"""\
#!/usr/bin/env python3
\"\"\"
Sales data processing script for quarterly reports.
This module handles data aggregation and reporting.
\"\"\"

import csv
import os
from datetime import datetime


class SalesProcessor:
    \"\"\"Processes monthly sales data for Q1 reporting.\"\"\"

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.records = []

    def load_csv(self, filename: str) -> bool:
        \"\"\"Load sales CSV file into memory.\"\"\"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f'File not found: {{filepath}}')
            return False

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append(row)

        print(f'Loaded {{len(self.records)}} records from {{filename}}')
        return True

    def calculate_total(self) -> float:
        \"\"\"Calculate total sales across all records.\"\"\"
        total = 0.0
        for record in self.records:
            try:
                total += float(record.get('amount', 0))
            except ValueError:
                pass
        return total

    def generate_report(self) -> str:
        \"\"\"Generate a summary report string.\"\"\"
        total = self.calculate_total()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        lines = [
            f'Sales Report - Generated: {{now}}',
            f'Total Records: {{len(self.records)}}',
            f'Total Revenue: ${{total:,.2f}}',
            '=' * 40,
        ]

        by_region = {{}}
        for record in self.records:
            region = record.get('region', 'Unknown')
            amount = float(record.get('amount', 0))
            by_region[region] = by_region.get(region, 0) + amount

        for region, amount in sorted(by_region.items()):
            lines.append(f'  {{region}}: ${{amount:,.2f}}')

        return '\\n'.join(lines)


def main():
    processor = SalesProcessor('/home/user/data')
    processor.load_csv('sales_q1_2025.csv')
    report = processor.generate_report()
    print(report)


if __name__ == '__main__':
    main()
"""

    with open(f'{WORKSPACE_DIR}/sales_processor.py', 'w') as f:
        f.write(main_py)
    print(f'Created: {WORKSPACE_DIR}/sales_processor.py')

    # Config file with trailing whitespace
    config_py = f"""\
# Configuration file for sales data processing
# Last updated: 2025-03-01

DATA_DIR = '/home/user/data'
OUTPUT_DIR = '/home/user/reports'

# Database connection settings
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'sales_db'
DB_USER = 'analytics_user'

# Report settings
REPORT_FORMAT = 'pdf'
INCLUDE_CHARTS = True
DECIMAL_PRECISION = 2

# Regional mappings
REGIONS = {{
    'NA': 'North America',
    'EU': 'Europe',
    'APAC': 'Asia Pacific',
    'LATAM': 'Latin America',
}}
"""

    with open(f'{WORKSPACE_DIR}/config.py', 'w') as f:
        f.write(config_py)
    print(f'Created: {WORKSPACE_DIR}/config.py')

    # README with trailing whitespace
    readme = f"""\
# Sales Data Processor

A Python tool for processing quarterly sales reports.

## Features

- Load and parse CSV sales data
- Calculate regional breakdowns
- Generate formatted reports

## Usage

```python
from sales_processor import SalesProcessor

processor = SalesProcessor('/path/to/data')
processor.load_csv('sales_q1_2025.csv')
print(processor.generate_report())
```

## Requirements

- Python 3.8+
- Standard library only (no external dependencies)

## Notes

Files may contain trailing whitespace that needs to be cleaned up.
Enable 'files.trimTrailingWhitespace' in VSCode settings to auto-trim on save.
"""

    with open(f'{WORKSPACE_DIR}/README.md', 'w') as f:
        f.write(readme)
    print(f'Created: {WORKSPACE_DIR}/README.md')

    print(f'Workspace created at: {WORKSPACE_DIR}')

    # 3. GUI-ready startup: open VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace on DISPLAY=:0')


create_initial()
