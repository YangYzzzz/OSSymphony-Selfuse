"""
Initial Setup: Set up a keybinding conflict in VSCode
Task ID: vscode_rrt_073
Domain: vscode (keybindings)

Creates a keybindings.json with a conflicting Ctrl+Shift+P binding
for the custom extension command 'myext.quickAction', then opens VSCode.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')

# Also create a small workspace so VSCode has something to open
WORKSPACE_DIR = os.path.join(HOME, 'workspace')


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
    # Ensure directories exist
    os.makedirs(VSCODE_USER, exist_ok=True)
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a conflicting keybinding: Ctrl+Shift+P bound to myext.quickAction
    # This conflicts with the default command palette shortcut
    keybindings = [
        {
            "key": "ctrl+shift+p",
            "command": "myext.quickAction"
        }
    ]
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump(keybindings, f, indent=4)
    print(f'Keybindings created: {KEYBINDINGS_PATH}')

    # Load and update settings (merge, don't overwrite)
    settings = {}
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    settings.update({
        "workbench.colorTheme": "Visual Studio Dark",
        "editor.fontSize": 14
    })
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings updated: {SETTINGS_PATH}')

    # Create a sample project file so VSCode has content to show
    sample_file = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(sample_file, 'w') as f:
        f.write('''"""
Project: Data Analysis Pipeline
Author: Sarah Chen
Date: 2025-03-15
"""

import csv
import statistics
from pathlib import Path


def load_sales_data(filepath: str) -> list:
    """Load quarterly sales data from CSV file."""
    records = []
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append({
                "region": row["region"],
                "quarter": row["quarter"],
                "revenue": float(row["revenue"]),
                "units_sold": int(row["units_sold"]),
            })
    return records


def calculate_summary(records: list) -> dict:
    """Calculate summary statistics by region."""
    regions = {}
    for rec in records:
        region = rec["region"]
        if region not in regions:
            regions[region] = []
        regions[region].append(rec["revenue"])

    summary = {}
    for region, revenues in regions.items():
        summary[region] = {
            "total_revenue": sum(revenues),
            "avg_revenue": statistics.mean(revenues),
            "max_revenue": max(revenues),
            "min_revenue": min(revenues),
        }
    return summary


if __name__ == "__main__":
    data_path = Path("data/sales_q1_2025.csv")
    if data_path.exists():
        sales = load_sales_data(str(data_path))
        report = calculate_summary(sales)
        for region, stats in report.items():
            print(f"{region}: Total ${stats['total_revenue']:,.2f}")
    else:
        print("Sales data file not found.")
''')
    print(f'Sample file created: {sample_file}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
