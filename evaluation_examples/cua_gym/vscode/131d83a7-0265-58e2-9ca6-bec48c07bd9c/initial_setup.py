"""
Initial Setup: Open VSCode with default settings (Dark+ theme, default icon theme)
Task ID: vscode_wf_002
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
    # Ensure VSCode config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings (preserve any existing config)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set default theme explicitly (Dark+ is the VSCode default)
    # Remove any Monokai or vs-seti settings that might already be present
    settings["workbench.colorTheme"] = "Default Dark+"
    # Remove icon theme if set to vs-seti, or leave default
    if settings.get("workbench.iconTheme") == "vs-seti":
        del settings["workbench.iconTheme"]

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings written to: {SETTINGS_PATH}")
    print(f"Settings content: {json.dumps(settings, indent=2)}")

    # Create a sample workspace with some files for a realistic environment
    workspace_dir = os.path.join(HOME, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a sample Python file
    sample_py = os.path.join(workspace_dir, "main.py")
    with open(sample_py, "w") as f:
        f.write('''"""
Sales Report Generator
Generates monthly sales reports from transaction data.
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


def load_transactions(filepath: str) -> list:
    """Load transaction records from a CSV file."""
    transactions = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                "product": row["product"],
                "quantity": int(row["quantity"]),
                "price": float(row["price"]),
                "region": row["region"],
            })
    return transactions


def aggregate_by_region(transactions: list) -> dict:
    """Aggregate total sales by region."""
    region_totals = defaultdict(float)
    for t in transactions:
        total = t["quantity"] * t["price"]
        region_totals[t["region"]] += total
    return dict(region_totals)


def generate_report(region_totals: dict, output_path: str):
    """Write a summary report to a text file."""
    with open(output_path, "w") as f:
        f.write("Monthly Sales Report\\n")
        f.write("=" * 40 + "\\n\\n")
        for region, total in sorted(region_totals.items()):
            f.write(f"  {region:.<25} ${total:,.2f}\\n")
        f.write("\\n" + "-" * 40 + "\\n")
        grand_total = sum(region_totals.values())
        f.write(f"  {'Grand Total':.<25} ${grand_total:,.2f}\\n")


if __name__ == "__main__":
    data_file = "transactions.csv"
    if os.path.exists(data_file):
        txns = load_transactions(data_file)
        totals = aggregate_by_region(txns)
        generate_report(totals, "report.txt")
        print("Report generated successfully.")
    else:
        print(f"Data file not found: {data_file}")
''')

    # Create a README
    readme = os.path.join(workspace_dir, "README.md")
    with open(readme, "w") as f:
        f.write("""# Sales Report Generator

A Python tool for generating monthly sales reports from transaction data.

## Usage

```bash
python main.py
```

## Features

- Loads transaction data from CSV files
- Aggregates sales by region
- Generates formatted text reports
""")

    print(f"Workspace created at: {workspace_dir}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
