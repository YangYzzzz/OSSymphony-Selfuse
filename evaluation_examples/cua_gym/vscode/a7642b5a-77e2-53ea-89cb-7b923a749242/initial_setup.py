"""
Initial Setup: Create project structure for data-tool with src/cli.py and data/input.csv.
Task ID: vscode_td_051
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_051'
PROJECT_DIR = f'{WORKDIR}/projects/data-tool'


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
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/results', exist_ok=True)

    # Create src/cli.py - a realistic CLI data processing tool
    cli_content = '''#!/usr/bin/env python3
"""Command-line interface for data processing tool."""

import argparse
import csv
import json
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process CSV data and output structured JSON results."
    )
    parser.add_argument(
        "--input", required=True, help="Path to input CSV file"
    )
    parser.add_argument(
        "--output", required=True, help="Path to output JSON file"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def process_data(input_path, output_path, verbose=False):
    """Read CSV input, process records, and write JSON output."""
    if verbose:
        print(f"Reading input from: {input_path}")

    records = []
    with open(input_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = {
                "id": row.get("id", ""),
                "name": row.get("name", ""),
                "category": row.get("category", ""),
                "value": float(row.get("value", 0)),
                "status": row.get("status", "pending"),
            }
            records.append(record)

    if verbose:
        print(f"Processed {len(records)} records")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({"results": records, "count": len(records)}, f, indent=2)

    if verbose:
        print(f"Output written to: {output_path}")


def main():
    args = parse_args()
    process_data(args.input, args.output, args.verbose)


if __name__ == "__main__":
    main()
'''
    with open(f'{PROJECT_DIR}/src/cli.py', 'w') as f:
        f.write(cli_content)

    # Create data/input.csv with realistic data
    csv_content = '''id,name,category,value,status
1,Widget Alpha,electronics,149.99,active
2,Sensor Beta,hardware,89.50,active
3,Module Gamma,electronics,234.00,pending
4,Adapter Delta,accessories,45.75,active
5,Cable Epsilon,accessories,12.99,discontinued
6,Board Zeta,hardware,178.00,active
7,Chip Eta,electronics,56.25,pending
8,Relay Theta,hardware,93.40,active
9,Connector Iota,accessories,27.80,active
10,Display Kappa,electronics,310.00,pending
11,Motor Lambda,hardware,425.50,active
12,Switch Mu,accessories,18.60,active
'''
    with open(f'{PROJECT_DIR}/data/input.csv', 'w') as f:
        f.write(csv_content)

    # Create a simple README for the project
    readme_content = '''# Data Processing Tool

A command-line utility for processing CSV data into structured JSON output.

## Usage

```bash
python src/cli.py --input data/input.csv --output results/output.json --verbose
```

## Arguments

- `--input` - Path to input CSV file
- `--output` - Path to output JSON file
- `--verbose` - Enable detailed logging
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Make sure there is NO .vscode directory (task requires creating launch.json)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/cli.py: CLI data processing tool')
    print(f'  data/input.csv: Sample input data')
    print(f'  No .vscode/launch.json (task target)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
