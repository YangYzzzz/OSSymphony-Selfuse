"""
Initial Setup: Create a Python project with main.py that accepts CLI arguments.
Task ID: vscode_py_007
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_007'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create main.py — a realistic Python script that accepts CLI arguments
    main_py_content = '''#!/usr/bin/env python3
"""
Data Processing Pipeline
========================
Processes input CSV files and generates analysis reports.

Usage:
    python main.py [options]

Options:
    --verbose           Enable detailed logging output
    --output FILE       Specify output file path (default: output.csv)
    --input FILE        Specify input data file
    --format FORMAT     Output format: csv, json, or xlsx
"""

import argparse
import csv
import os
import sys
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline - Analyze and transform datasets"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable detailed logging output"
    )
    parser.add_argument(
        "--output", type=str, default="output.csv",
        help="Path to the output file (default: output.csv)"
    )
    parser.add_argument(
        "--input", type=str, default="data/sample_input.csv",
        help="Path to the input data file"
    )
    parser.add_argument(
        "--format", type=str, choices=["csv", "json", "xlsx"],
        default="csv", help="Output format"
    )
    return parser.parse_args()


def load_data(filepath, verbose=False):
    """Load and validate input data from CSV file."""
    if verbose:
        print(f"[{datetime.now().isoformat()}] Loading data from {filepath}")

    if not os.path.exists(filepath):
        print(f"Warning: Input file {filepath} not found. Using sample data.")
        return [
            {"name": "Alice Wang", "department": "Engineering", "salary": 95000},
            {"name": "Bob Martinez", "department": "Marketing", "salary": 78000},
            {"name": "Carol Thompson", "department": "Engineering", "salary": 102000},
            {"name": "David Kim", "department": "Sales", "salary": 67000},
            {"name": "Eva Johansson", "department": "Engineering", "salary": 88000},
        ]

    data = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    if verbose:
        print(f"[{datetime.now().isoformat()}] Loaded {len(data)} records")
    return data


def process_data(data, verbose=False):
    """Run analysis computations on the dataset."""
    if verbose:
        print(f"[{datetime.now().isoformat()}] Processing {len(data)} records...")

    results = []
    for record in data:
        processed = {
            "name": record["name"],
            "department": record["department"],
            "salary": float(record["salary"]),
            "tax_bracket": "high" if float(record["salary"]) > 90000 else "standard",
        }
        results.append(processed)

    if verbose:
        high_earners = sum(1 for r in results if r["tax_bracket"] == "high")
        print(f"[{datetime.now().isoformat()}] Found {high_earners} high-bracket employees")

    return results


def write_output(results, output_path, verbose=False):
    """Write processed results to the output file."""
    if verbose:
        print(f"[{datetime.now().isoformat()}] Writing {len(results)} records to {output_path}")

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    with open(output_path, "w", newline="") as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    if verbose:
        print(f"[{datetime.now().isoformat()}] Output written successfully")


def main():
    args = parse_arguments()

    if args.verbose:
        print("=" * 60)
        print("Data Processing Pipeline - Starting")
        print(f"Input:  {args.input}")
        print(f"Output: {args.output}")
        print(f"Format: {args.format}")
        print("=" * 60)

    data = load_data(args.input, verbose=args.verbose)
    results = process_data(data, verbose=args.verbose)
    write_output(results, args.output, verbose=args.verbose)

    print(f"Processing complete. {len(results)} records written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_py_content)

    # Create a helper module
    utils_content = '''"""Utility functions for the data processing pipeline."""

import logging
from datetime import datetime


def setup_logger(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def format_currency(amount):
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"


def timestamp():
    """Return current ISO-format timestamp."""
    return datetime.now().isoformat()
'''
    with open(f'{PROJECT_DIR}/utils.py', 'w') as f:
        f.write(utils_content)

    # Create sample data directory and file
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    sample_csv = '''name,department,salary
Alice Wang,Engineering,95000
Bob Martinez,Marketing,78000
Carol Thompson,Engineering,102000
David Kim,Sales,67000
Eva Johansson,Engineering,88000
Frank Liu,Marketing,72000
Grace Okonkwo,Sales,81000
Henry Patel,Engineering,97000
'''
    with open(f'{PROJECT_DIR}/data/sample_input.csv', 'w') as f:
        f.write(sample_csv)

    # Create a README
    readme = '''# Data Processing Pipeline

A simple data processing tool that reads CSV input, applies transformations,
and outputs analysis results.

## Usage

```bash
python main.py --verbose --output results.csv
python main.py --input data/sample_input.csv --format json
```

## Requirements

- Python 3.8+
- No external dependencies
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Ensure NO .vscode directory exists (task requires creating it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: main.py, utils.py, data/sample_input.csv, README.md')
    print(f'No .vscode/launch.json exists (task requires creating it)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
