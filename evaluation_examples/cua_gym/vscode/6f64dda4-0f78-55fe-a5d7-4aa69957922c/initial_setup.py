"""
Initial Setup: Configure VSCode with autoSave set to afterDelay
Task ID: vscode_we_026
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_026'
VSCODE_USER = os.path.join(os.path.expanduser("~"), ".config", "Code", "User")
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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # Set up VSCode settings with autoSave afterDelay
    update_settings({
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })
    print(f"Settings written to: {SETTINGS_PATH}")

    # Verify
    with open(SETTINGS_PATH, "r") as f:
        content = json.load(f)
    print(f"Settings content: {json.dumps(content, indent=2)}")

    # Create a simple workspace file so VSCode has something to open
    workspace_dir = os.path.join(WORKDIR, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    sample_file = os.path.join(workspace_dir, "main.py")
    with open(sample_file, "w") as f:
        f.write('"""Project main module."""\n\n\ndef calculate_revenue(units_sold, price_per_unit, discount=0.0):\n    """Calculate total revenue with optional discount."""\n    gross = units_sold * price_per_unit\n    return gross * (1 - discount)\n\n\ndef format_report(title, data):\n    """Format a simple text report."""\n    lines = [f"=== {title} ===", ""]\n    for key, value in data.items():\n        lines.append(f"  {key}: {value}")\n    lines.append("")\n    return "\\n".join(lines)\n\n\nif __name__ == "__main__":\n    revenue = calculate_revenue(150, 29.99, discount=0.1)\n    report = format_report("Q1 Sales Summary", {\n        "Total Units": 150,\n        "Price per Unit": "$29.99",\n        "Discount": "10%",\n        "Net Revenue": f"${revenue:.2f}",\n    })\n    print(report)\n')
    print(f"Workspace file created: {sample_file}")

    # Launch VSCode with the workspace folder
    launch_gui('code "/home/user/workspace"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
