"""
Initial Setup: Configure VSCode to automatically activate Python venv in terminal
Task ID: vscode_py_024
Domain: vscode

Creates a Python project workspace with a .venv virtual environment.
VSCode settings do NOT include python.terminal.activateEnvironment.
Opens VSCode with the workspace folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_024'
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
VENV_DIR = os.path.join(WORKSPACE_DIR, '.venv')
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
    # --- Create workspace directory with a Python project ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a realistic Python project structure
    src_dir = os.path.join(WORKSPACE_DIR, 'src')
    tests_dir = os.path.join(WORKSPACE_DIR, 'tests')
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    # Main application file
    with open(os.path.join(WORKSPACE_DIR, 'main.py'), 'w') as f:
        f.write('''"""Data processing pipeline for quarterly sales reports."""

import os
import sys
from src.processor import SalesProcessor
from src.reporter import ReportGenerator


def main():
    """Run the quarterly sales data processing pipeline."""
    input_dir = os.path.join(os.path.dirname(__file__), 'data', 'raw')
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'processed')

    processor = SalesProcessor(input_dir)
    cleaned_data = processor.clean_and_validate()

    reporter = ReportGenerator(cleaned_data)
    reporter.generate_summary(output_dir)
    reporter.generate_charts(output_dir)

    print(f"Pipeline complete. Reports saved to {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')

    # Source module - processor
    with open(os.path.join(src_dir, '__init__.py'), 'w') as f:
        f.write('"""Sales data processing package."""\n')

    with open(os.path.join(src_dir, 'processor.py'), 'w') as f:
        f.write('''"""Sales data processor module."""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional


class SalesProcessor:
    """Processes raw sales CSV data with validation and cleaning."""

    REQUIRED_COLUMNS = ['date', 'product_id', 'quantity', 'unit_price', 'region']

    def __init__(self, input_dir: str):
        self.input_dir = input_dir
        self.raw_records: List[Dict] = []
        self.cleaned_records: List[Dict] = []

    def load_csv_files(self) -> None:
        """Load all CSV files from the input directory."""
        for filename in sorted(os.listdir(self.input_dir)):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.input_dir, filename)
                with open(filepath, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.raw_records.append(row)

    def validate_record(self, record: Dict) -> bool:
        """Validate a single sales record."""
        for col in self.REQUIRED_COLUMNS:
            if col not in record or not record[col]:
                return False
        try:
            datetime.strptime(record['date'], '%Y-%m-%d')
            float(record['quantity'])
            float(record['unit_price'])
        except (ValueError, TypeError):
            return False
        return True

    def clean_and_validate(self) -> List[Dict]:
        """Clean and validate all loaded records."""
        self.load_csv_files()
        for record in self.raw_records:
            if self.validate_record(record):
                cleaned = {
                    'date': record['date'],
                    'product_id': record['product_id'].strip().upper(),
                    'quantity': int(float(record['quantity'])),
                    'unit_price': round(float(record['unit_price']), 2),
                    'region': record['region'].strip().title(),
                    'total': round(float(record['quantity']) * float(record['unit_price']), 2),
                }
                self.cleaned_records.append(cleaned)
        return self.cleaned_records
''')

    # Source module - reporter
    with open(os.path.join(src_dir, 'reporter.py'), 'w') as f:
        f.write('''"""Report generation module."""

from collections import defaultdict
from typing import List, Dict


class ReportGenerator:
    """Generates summary reports from cleaned sales data."""

    def __init__(self, data: List[Dict]):
        self.data = data

    def generate_summary(self, output_dir: str) -> str:
        """Generate a text summary of sales by region."""
        region_totals = defaultdict(float)
        for record in self.data:
            region_totals[record['region']] += record['total']
        # Write summary
        return "Summary generated"

    def generate_charts(self, output_dir: str) -> str:
        """Generate visualization charts."""
        return "Charts generated"
''')

    # Tests
    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(tests_dir, 'test_processor.py'), 'w') as f:
        f.write('''"""Tests for the SalesProcessor class."""

import unittest
from src.processor import SalesProcessor


class TestSalesProcessor(unittest.TestCase):

    def test_validate_record_valid(self):
        record = {
            'date': '2025-03-15',
            'product_id': 'PROD-001',
            'quantity': '10',
            'unit_price': '29.99',
            'region': 'Northeast',
        }
        processor = SalesProcessor('/tmp')
        self.assertTrue(processor.validate_record(record))

    def test_validate_record_missing_field(self):
        record = {'date': '2025-03-15', 'product_id': 'PROD-001'}
        processor = SalesProcessor('/tmp')
        self.assertFalse(processor.validate_record(record))


if __name__ == "__main__":
    unittest.main()
''')

    # Requirements file
    with open(os.path.join(WORKSPACE_DIR, 'requirements.txt'), 'w') as f:
        f.write('''# Project dependencies
pandas>=2.0.0
matplotlib>=3.7.0
numpy>=1.24.0
pytest>=7.3.0
black>=23.3.0
flake8>=6.0.0
''')

    # README
    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write('''# Sales Data Pipeline

Automated pipeline for processing quarterly sales reports.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
''')

    # .gitignore
    with open(os.path.join(WORKSPACE_DIR, '.gitignore'), 'w') as f:
        f.write('''.venv/
__pycache__/
*.pyc
data/processed/
.env
''')

    # --- Create a virtual environment structure manually ---
    # python3-venv package may not be installed, so create the structure directly
    venv_bin = os.path.join(VENV_DIR, 'bin')
    venv_lib = os.path.join(VENV_DIR, 'lib', 'python3.10', 'site-packages')
    venv_include = os.path.join(VENV_DIR, 'include')
    os.makedirs(venv_bin, exist_ok=True)
    os.makedirs(venv_lib, exist_ok=True)
    os.makedirs(venv_include, exist_ok=True)

    # Create pyvenv.cfg
    with open(os.path.join(VENV_DIR, 'pyvenv.cfg'), 'w') as f:
        f.write('home = /usr/bin\n')
        f.write('include-system-site-packages = false\n')
        f.write('version = 3.10.12\n')

    # Symlink python
    python_link = os.path.join(venv_bin, 'python')
    python3_link = os.path.join(venv_bin, 'python3')
    if not os.path.exists(python_link):
        os.symlink('/usr/bin/python3', python_link)
    if not os.path.exists(python3_link):
        os.symlink('/usr/bin/python3', python3_link)

    # Create activate script
    with open(os.path.join(venv_bin, 'activate'), 'w') as f:
        f.write(f'''# This file must be used with "source bin/activate" *from bash*
deactivate () {{
    if [ -n "${{_OLD_VIRTUAL_PATH:-}}" ] ; then
        PATH="${{_OLD_VIRTUAL_PATH:-}}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${{_OLD_VIRTUAL_PS1:-}}" ] ; then
        PS1="${{_OLD_VIRTUAL_PS1:-}}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi
    unset VIRTUAL_ENV
    if [ ! "${{1:-}}" = "nondestructive" ] ; then
        unset -f deactivate
    fi
}}
deactivate nondestructive
VIRTUAL_ENV="{VENV_DIR}"
export VIRTUAL_ENV
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
_OLD_VIRTUAL_PS1="${{PS1:-}}"
PS1="(.venv) ${{PS1:-}}"
export PS1
''')

    print(f'Virtual environment created at: {VENV_DIR}')

    # --- Configure VSCode user settings ---
    # Load existing settings and ensure python.terminal.activateEnvironment is NOT set
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove the target setting if it exists
    settings.pop('python.terminal.activateEnvironment', None)

    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings configured (no activateEnvironment): {SETTINGS_PATH}')

    # --- Create workspace-level .vscode/settings.json (empty, no activate) ---
    ws_vscode_dir = os.path.join(WORKSPACE_DIR, '.vscode')
    os.makedirs(ws_vscode_dir, exist_ok=True)
    ws_settings_path = os.path.join(ws_vscode_dir, 'settings.json')
    with open(ws_settings_path, 'w') as f:
        json.dump({
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
        }, f, indent=4)
    print(f'Workspace settings created: {ws_settings_path}')

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace at DISPLAY=:0')


create_initial()
