"""
Initial Setup: Create a chord keybinding in VSCode keybindings.json
Task ID: vscode_rrt_067
Domain: vscode

Sets up keybindings.json with one existing keybinding (Ctrl+Shift+L for
selectHighlights). VSCode is opened so the agent can add the chord keybinding.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")

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
    os.makedirs(VSCODE_USER, exist_ok=True)

    # One pre-existing keybinding (unrelated to the task)
    keybindings = [
        {
            "key": "ctrl+shift+l",
            "command": "editor.action.selectHighlights",
            "when": "editorFocus"
        }
    ]

    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump(keybindings, f, indent=4)

    print(f"Initial keybindings.json created at: {KEYBINDINGS_PATH}")

    # Also create a sample workspace file so VSCode has something to open
    workspace_dir = os.path.join(HOME, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    sample_file = os.path.join(workspace_dir, "main.py")
    with open(sample_file, "w") as f:
        f.write("""# Data Processing Pipeline
import csv
import datetime

def load_records(filepath):
    \"\"\"Load employee records from CSV file.\"\"\"
    records = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(row)
    return records

def calculate_averages(records):
    \"\"\"Calculate average salary by department.\"\"\"
    departments = {}
    for record in records:
        dept = record['department']
        salary = float(record['salary'])
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(salary)
    return {dept: sum(vals)/len(vals) for dept, vals in departments.items()}

if __name__ == '__main__':
    data = load_records('employees.csv')
    averages = calculate_averages(data)
    for dept, avg in sorted(averages.items()):
        print(f'{dept}: ${avg:,.2f}')
""")

    print(f"Sample workspace created at: {workspace_dir}")

    # Launch VSCode with the workspace
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")

create_initial()
