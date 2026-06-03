"""
Initial Setup: Configure VSCode indentation settings
Task ID: vscode_stu_023
Domain: vscode

Initial state: VSCode with default/tab-based indentation settings.
A sample Python project is created so the agent has something to work with.
Settings do NOT include editor.insertSpaces or editor.tabSize (task hasn't been done yet).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_023'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Project directory with sample files
PROJECT_DIR = os.path.join(WORKDIR, "student_project")


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
    # --- Create a sample project for the student ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Sample Python file with tab-based indentation (the "problem")
    main_py = os.path.join(PROJECT_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''#!/usr/bin/env python3
"""Student project: Grade calculator for CS201 course."""


def calculate_average(grades):
\t"""Calculate the average of a list of grades."""
\ttotal = sum(grades)
\tcount = len(grades)
\tif count == 0:
\t\treturn 0.0
\treturn total / count


def letter_grade(score):
\t"""Convert numeric score to letter grade."""
\tif score >= 90:
\t\treturn "A"
\telif score >= 80:
\t\treturn "B"
\telif score >= 70:
\t\treturn "C"
\telif score >= 60:
\t\treturn "D"
\telse:
\t\treturn "F"


def main():
\tgrades = [92, 85, 78, 95, 88, 73, 91, 84]
\tstudent_names = [
\t\t"Alice Wang",
\t\t"Bob Martinez",
\t\t"Carol Johnson",
\t\t"David Park",
\t\t"Eva Novak",
\t\t"Frank Liu",
\t\t"Grace Kim",
\t\t"Henry Brown",
\t]
\tavg = calculate_average(grades)
\tprint(f"Class average: {avg:.1f}")
\tfor name, grade in zip(student_names, grades):
\t\tletter = letter_grade(grade)
\t\tprint(f"  {name}: {grade} ({letter})")


if __name__ == "__main__":
\tmain()
''')

    # Create a utils module
    utils_py = os.path.join(PROJECT_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write('''"""Utility functions for student project."""


def format_percentage(value):
\t"""Format a float as a percentage string."""
\treturn f"{value:.1f}%"


def validate_grade(grade):
\t"""Validate that a grade is between 0 and 100."""
\tif not isinstance(grade, (int, float)):
\t\traise TypeError("Grade must be a number")
\tif grade < 0 or grade > 100:
\t\traise ValueError("Grade must be between 0 and 100")
\treturn True
''')

    print(f"Project created at: {PROJECT_DIR}")

    # --- Set VSCode settings to use tabs (the initial state before task) ---
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set tab-based indentation (the state before the student configures spaces)
    settings["editor.insertSpaces"] = False
    settings["editor.tabSize"] = 8
    # Remove any existing correct values to ensure clean initial state
    # (these are explicitly wrong - tabs, size 8)

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings written to: {SETTINGS_PATH}")
    print(f"  editor.insertSpaces = False (tabs)")
    print(f"  editor.tabSize = 8")

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
