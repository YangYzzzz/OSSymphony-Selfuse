"""
Initial Setup: Set the default terminal shell in VSCode to /bin/zsh on Linux.
Task ID: vscode_we_007
Domain: vscode

Creates an empty VSCode user settings.json (no terminal config),
a sample workspace with a Python file, and launches VSCode.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
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
    # --- Ensure VSCode user config directory exists ---
    os.makedirs(VSCODE_USER, exist_ok=True)

    # --- Write empty settings (no terminal configuration) ---
    settings = {}
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings written: {SETTINGS_PATH}")

    # --- Create a sample workspace with a Python file ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    sample_file = os.path.join(WORKSPACE_DIR, "main.py")
    with open(sample_file, "w") as f:
        f.write(
            '"""Data processing pipeline for quarterly sales reports."""\n'
            "\n"
            "import csv\n"
            "import os\n"
            "from datetime import datetime\n"
            "\n"
            "\n"
            "def load_sales_data(filepath):\n"
            '    """Load sales data from a CSV file."""\n'
            "    records = []\n"
            '    with open(filepath, "r") as f:\n'
            "        reader = csv.DictReader(f)\n"
            "        for row in reader:\n"
            "            records.append({\n"
            '                "date": datetime.strptime(row["date"], "%Y-%m-%d"),\n'
            '                "product": row["product"],\n'
            '                "revenue": float(row["revenue"]),\n'
            '                "units": int(row["units"]),\n'
            "            })\n"
            "    return records\n"
            "\n"
            "\n"
            "def summarize_by_product(records):\n"
            '    """Aggregate revenue and units by product."""\n'
            "    summary = {}\n"
            "    for r in records:\n"
            '        product = r["product"]\n'
            "        if product not in summary:\n"
            '            summary[product] = {"revenue": 0.0, "units": 0}\n'
            '        summary[product]["revenue"] += r["revenue"]\n'
            '        summary[product]["units"] += r["units"]\n'
            "    return summary\n"
            "\n"
            "\n"
            'if __name__ == "__main__":\n'
            '    data = load_sales_data("sales_q1_2025.csv")\n'
            "    report = summarize_by_product(data)\n"
            "    for product, stats in sorted(report.items()):\n"
            "        print(f\"{product}: ${stats['revenue']:,.2f} ({stats['units']} units)\")\n"
        )
    print(f"Sample workspace created: {WORKSPACE_DIR}")

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
