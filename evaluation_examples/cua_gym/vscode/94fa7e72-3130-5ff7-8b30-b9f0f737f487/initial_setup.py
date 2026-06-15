"""
Initial Setup: Set VSCode editor.lineNumbers to 'off' and open VSCode with a sample workspace.
Task ID: vscode_stu_021
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_021'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(WORKDIR, "cs101_project")


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
            content = f.read()
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_workspace():
    """Create a realistic student project workspace."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file - a simple student assignment
    main_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''\
#!/usr/bin/env python3
"""CS101 Assignment 3: Grade Calculator
Author: Student
Date: 2026-03-28
"""


def calculate_average(grades):
    """Calculate the average of a list of grades."""
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def letter_grade(score):
    """Convert a numeric score to a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def process_student_grades(students):
    """Process a dictionary of student grades and return results."""
    results = {}
    for name, grades in students.items():
        avg = calculate_average(grades)
        results[name] = {
            "grades": grades,
            "average": round(avg, 2),
            "letter": letter_grade(avg),
        }
    return results


def main():
    students = {
        "Alice Wang": [92, 88, 95, 91],
        "Bob Martinez": [78, 82, 75, 80],
        "Carol Singh": [65, 70, 68, 72],
        "David Kim": [95, 98, 92, 97],
        "Emma Thompson": [58, 62, 55, 60],
    }

    results = process_student_grades(students)

    print("=" * 50)
    print("CS101 Grade Report")
    print("=" * 50)
    for name, data in results.items():
        print(f"{name}: Average = {data['average']}, Grade = {data['letter']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
''')

    # A helper module
    utils_py = os.path.join(WORKSPACE_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write('''\
"""Utility functions for CS101 assignments."""


def validate_grade(grade):
    """Check if a grade is within valid range (0-100)."""
    return isinstance(grade, (int, float)) and 0 <= grade <= 100


def format_percentage(value):
    """Format a float as a percentage string."""
    return f"{value:.1f}%"
''')

    print(f"Workspace created: {WORKSPACE_DIR}")


def setup_initial():
    # 1. Create student project workspace
    create_workspace()

    # 2. Set editor.lineNumbers to 'off' (the initial state)
    update_settings({
        "editor.lineNumbers": "off",
    })
    print(f"Settings updated: editor.lineNumbers = 'off'")

    # 3. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


setup_initial()
