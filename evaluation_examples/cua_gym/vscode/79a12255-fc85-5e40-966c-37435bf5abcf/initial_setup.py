"""
Initial Setup: Configure Vim extension settings in VSCode
Task ID: vscode_we_086
Domain: vscode

Creates initial state: VSCode open with empty user settings and
the vscodevim.vim extension installed (default config).
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Also create a small workspace so the agent has something to look at
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (no Vim configuration at all)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)
    print(f"Settings written to {SETTINGS_PATH} (empty)")

    # Create a small workspace with a sample file so VSCode has content
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    sample_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(sample_py, "w") as f:
        f.write('''\
"""
Quarterly Revenue Analysis
Computes year-over-year growth from regional sales data.
"""

import csv
from pathlib import Path


REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America"]

QUARTERLY_DATA = {
    "North America":  [128400, 135200, 142800, 151300],
    "Europe":         [ 98700, 101500, 106200, 112400],
    "Asia Pacific":   [ 76300,  82100,  89400,  97600],
    "Latin America":  [ 34500,  36800,  39200,  41700],
}


def compute_growth(data: dict) -> dict:
    """Return YoY growth percentage per region."""
    growth = {}
    for region, quarters in data.items():
        total_current = sum(quarters)
        # assume previous year was 8% less
        total_previous = total_current / 1.08
        growth[region] = round((total_current - total_previous) / total_previous * 100, 2)
    return growth


def generate_report(output_path: str = "report.csv"):
    growth = compute_growth(QUARTERLY_DATA)
    rows = [["Region", "Q1", "Q2", "Q3", "Q4", "YoY Growth %"]]
    for region in REGIONS:
        q = QUARTERLY_DATA[region]
        rows.append([region, *q, f"{growth[region]:.2f}%"])

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    generate_report()
''')
    print(f"Sample workspace created at {WORKSPACE_DIR}")

    # Ensure vscodevim.vim extension is installed
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=30
        )
        if "vscodevim.vim" not in result.stdout.lower():
            print("Installing vscodevim.vim extension...")
            subprocess.run(
                ["code", "--install-extension", "vscodevim.vim"],
                capture_output=True, text=True, timeout=120
            )
            print("vscodevim.vim installed")
        else:
            print("vscodevim.vim already installed")
    except Exception as e:
        print(f"Extension check/install note: {e}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
