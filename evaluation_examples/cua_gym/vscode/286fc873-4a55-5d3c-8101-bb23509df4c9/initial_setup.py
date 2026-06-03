"""
Initial Setup: Configure Ruff as linter/formatter - PRE-task state
Task ID: vscode_py_015
Domain: vscode

Initial state: VSCode open with Python project. pylint enabled, Black as formatter.
Ruff extension installed but NOT configured as linter/formatter.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_015'
WORKSPACE = f'{WORKDIR}/workspace'
HOME = os.path.expanduser('~')
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


def create_workspace_files():
    """Create a realistic Python project."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # main.py
    with open(os.path.join(WORKSPACE, 'main.py'), 'w') as f:
        f.write('''\
"""Main entry point for the data processing pipeline."""

import argparse
import sys
from pathlib import Path

from processors.csv_loader import CSVLoader
from processors.transformer import DataTransformer
from utils.logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output", type=str, default="output.csv", help="Output file path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def main():
    args = parse_args()
    logger = setup_logging(verbose=args.verbose)

    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    logger.info(f"Loading data from {input_path}")
    loader = CSVLoader(str(input_path))
    raw_data = loader.load()

    logger.info(f"Transforming {len(raw_data)} records")
    transformer = DataTransformer()
    processed = transformer.transform(raw_data)

    output_path = Path(args.output)
    loader.save(processed, str(output_path))
    logger.info(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
''')

    # processors directory
    proc_dir = os.path.join(WORKSPACE, 'processors')
    os.makedirs(proc_dir, exist_ok=True)

    with open(os.path.join(proc_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(proc_dir, 'csv_loader.py'), 'w') as f:
        f.write('''\
"""CSV file loading and saving utilities."""

import csv
from typing import Any, Dict, List


class CSVLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> List[Dict[str, Any]]:
        """Load CSV file and return list of row dictionaries."""
        records = []
        with open(self.filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        return records

    def save(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """Save processed data back to CSV."""
        if not data:
            return
        fieldnames = list(data[0].keys())
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
''')

    with open(os.path.join(proc_dir, 'transformer.py'), 'w') as f:
        f.write('''\
"""Data transformation logic."""

from typing import Any, Dict, List


class DataTransformer:
    def __init__(self, threshold: float = 100.0):
        self.threshold = threshold

    def transform(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply business rules to each record."""
        transformed = []
        for record in records:
            new_record = self._apply_rules(record)
            transformed.append(new_record)
        return transformed

    def _apply_rules(self, record: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(record)
        if "amount" in result:
            try:
                amount = float(result["amount"])
                result["category"] = "high" if amount > self.threshold else "low"
            except (ValueError, TypeError):
                result["category"] = "unknown"
        return result
''')

    # utils directory
    utils_dir = os.path.join(WORKSPACE, 'utils')
    os.makedirs(utils_dir, exist_ok=True)

    with open(os.path.join(utils_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(utils_dir, 'logger.py'), 'w') as f:
        f.write('''\
"""Logging configuration."""

import logging
import sys


def setup_logging(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger("pipeline")
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
''')

    # requirements.txt
    with open(os.path.join(WORKSPACE, 'requirements.txt'), 'w') as f:
        f.write('''\
pandas>=2.0.0
numpy>=1.24.0
pytest>=7.4.0
ruff>=0.1.0
''')

    print(f'Workspace created: {WORKSPACE}')


def configure_vscode_settings():
    """Set up VSCode with pylint enabled and Black as formatter (pre-task state)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set the initial state: pylint enabled, Black as formatter
    settings["python.linting.pylintEnabled"] = True
    settings["[python]"] = {
        "editor.defaultFormatter": "ms-python.black-formatter"
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured: {SETTINGS_PATH}')
    print(f'  pylint enabled: True')
    print(f'  Python formatter: ms-python.black-formatter')


def install_ruff_extension():
    """Ensure Ruff extension is installed."""
    try:
        result = subprocess.run(
            ['code', '--install-extension', 'charliermarsh.ruff', '--force'],
            capture_output=True, text=True, timeout=60
        )
        print(f'Ruff extension install: {result.stdout.strip()}')
        if result.returncode != 0:
            print(f'Warning: {result.stderr.strip()}')
    except Exception as e:
        print(f'Extension install warning: {e}')


def main():
    create_workspace_files()
    configure_vscode_settings()
    install_ruff_extension()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with workspace and DISPLAY=:0')


main()
