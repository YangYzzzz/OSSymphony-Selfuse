"""
Initial Setup: Create python-startup.py and open VSCode with no custom terminal profiles.
Task ID: vscode_gf5_042
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_042'

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
    # 1. Create ~/python-startup.py with common library imports
    startup_path = os.path.join(HOME, "python-startup.py")
    startup_content = """\
# Python REPL startup file - imports common libraries
import json
import sys
import os
import datetime
"""
    with open(startup_path, "w") as f:
        f.write(startup_content)
    print(f"Created: {startup_path}")

    # 2. Ensure VSCode settings exist but do NOT contain any custom terminal profiles
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any existing terminal profile config to ensure clean initial state
    for key in list(settings.keys()):
        if key.startswith("terminal.integrated.profiles."):
            del settings[key]

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings cleaned (no custom terminal profiles): {SETTINGS_PATH}")

    # 3. Create a small workspace directory with a sample file so VSCode has something to show
    workspace_dir = os.path.join(HOME, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    sample_file = os.path.join(workspace_dir, "notes.py")
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write("""\
# Quick calculation notes
# Use the terminal to run Python interactively

def calculate_quarterly_revenue(monthly_data):
    \"\"\"Sum monthly revenue figures for quarterly report.\"\"\"
    return sum(monthly_data)

# Q1 2025 revenue by month
q1_revenue = [145230.50, 162845.75, 158920.30]
print(f"Q1 Total: ${calculate_quarterly_revenue(q1_revenue):,.2f}")
""")
    print(f"Created workspace: {workspace_dir}")

    # 4. Open VSCode with the workspace folder (GUI-ready state)
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
