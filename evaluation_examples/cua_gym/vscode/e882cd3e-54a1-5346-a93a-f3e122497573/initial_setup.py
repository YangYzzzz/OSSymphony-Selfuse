"""
Initial Setup: Configure autopep8 as the Python formatter with custom settings
Task ID: vscode_py_050
Domain: vscode

Creates a Python project workspace with a sample file. VSCode settings have
NO python formatter configured and NO autopep8.args. Opens VSCode with the project.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
WORKSPACE = os.path.join(HOME, 'workspace')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
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
    # 1. Create workspace directory with a sample Python project
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a sample Python file with some code that could use formatting
    sample_py = os.path.join(WORKSPACE, 'data_processor.py')
    with open(sample_py, 'w') as f:
        f.write('''\
import os
import sys
from collections import defaultdict


class DataProcessor:
    """Processes sales data from CSV files and generates summary reports."""

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.records = []
        self.summary = defaultdict(float)

    def load_records(self, filename):
        """Load records from a CSV file into memory."""
        filepath = os.path.join(self.input_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, skipping.")
            return 0
        count = 0
        with open(filepath, 'r') as f:
            headers = f.readline().strip().split(',')
            for line in f:
                values = line.strip().split(',')
                record = dict(zip(headers, values))
                self.records.append(record)
                count += 1
        return count

    def compute_summary(self):
        """Compute total sales by region."""
        for record in self.records:
            region = record.get('region', 'Unknown')
            amount = float(record.get('amount', 0))
            self.summary[region] += amount

    def generate_report(self, output_filename='summary_report.txt'):
        """Write summary report to output directory."""
        os.makedirs(self.output_dir, exist_ok=True)
        outpath = os.path.join(self.output_dir, output_filename)
        with open(outpath, 'w') as f:
            f.write("Sales Summary Report\\n")
            f.write("=" * 40 + "\\n")
            for region, total in sorted(self.summary.items()):
                f.write(f"  {region:<20s}  ${total:>12,.2f}\\n")
            f.write("=" * 40 + "\\n")
            grand_total = sum(self.summary.values())
            f.write(f"  {'GRAND TOTAL':<20s}  ${grand_total:>12,.2f}\\n")
        print(f"Report written to {outpath}")


def main():
    processor = DataProcessor('/home/user/data/input', '/home/user/data/output')
    files_loaded = processor.load_records('q1_sales.csv')
    print(f"Loaded {files_loaded} records")
    processor.compute_summary()
    processor.generate_report()


if __name__ == '__main__':
    main()
''')

    # Create a second Python file
    utils_py = os.path.join(WORKSPACE, 'utils.py')
    with open(utils_py, 'w') as f:
        f.write('''\
"""Utility functions for data processing pipeline."""

import re
from datetime import datetime, timedelta


def parse_date(date_str, fmt='%Y-%m-%d'):
    """Parse a date string into a datetime object."""
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        return None


def date_range(start, end, step_days=1):
    """Generate dates from start to end (inclusive)."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=step_days)


def sanitize_filename(name):
    """Remove or replace characters that are invalid in filenames."""
    name = re.sub(r'[<>:"/\\\\|?*]', '_', name)
    name = name.strip('. ')
    return name if name else 'unnamed'


def format_currency(amount, currency='USD'):
    """Format a number as currency string."""
    symbols = {'USD': '$', 'EUR': '\\u20ac', 'GBP': '\\u00a3', 'JPY': '\\u00a5'}
    symbol = symbols.get(currency, currency + ' ')
    return f"{symbol}{amount:,.2f}"
''')

    # 2. Set up VSCode settings WITHOUT any python formatter config
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Ensure NO python formatter or autopep8 settings exist
    settings.pop('[python]', None)
    settings.pop('autopep8.args', None)
    settings.pop('python.formatting.autopep8Args', None)
    settings.pop('python.formatting.provider', None)

    # Add some baseline settings (realistic, non-formatter related)
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "python.analysis.typeCheckingMode": "basic"
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"Settings written to {SETTINGS_PATH}")
    print(f"Workspace created at {WORKSPACE}")

    # 3. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
