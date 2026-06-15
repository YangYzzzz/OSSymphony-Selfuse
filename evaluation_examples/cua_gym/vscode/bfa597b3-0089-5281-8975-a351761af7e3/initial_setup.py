"""
Initial Setup: Open VSCode with Explorer sidebar visible
Task ID: vscode_stu_009
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_009'
WORKSPACE_DIR = f'{WORKDIR}/project'

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


def create_workspace_files():
    """Create a realistic project workspace for the agent to see in Explorer."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file
    with open(os.path.join(WORKSPACE_DIR, "main.py"), "w") as f:
        f.write('''"""
Student Grade Management System
Handles grade calculations and report generation.
"""

from statistics import mean, median
from dataclasses import dataclass


@dataclass
class Student:
    name: str
    student_id: str
    grades: list

    @property
    def average(self):
        return mean(self.grades) if self.grades else 0.0

    @property
    def letter_grade(self):
        avg = self.average
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"


def generate_class_report(students):
    """Generate a summary report for all students."""
    all_averages = [s.average for s in students]
    report = {
        "total_students": len(students),
        "class_average": round(mean(all_averages), 2),
        "class_median": round(median(all_averages), 2),
        "grade_distribution": {},
    }
    for s in students:
        grade = s.letter_grade
        report["grade_distribution"][grade] = report["grade_distribution"].get(grade, 0) + 1
    return report


if __name__ == "__main__":
    students = [
        Student("Alice Wang", "STU001", [92, 88, 95, 91]),
        Student("Bob Martinez", "STU002", [78, 82, 75, 80]),
        Student("Carol Liu", "STU003", [95, 97, 93, 98]),
        Student("David Kim", "STU004", [65, 70, 68, 72]),
        Student("Eva Johnson", "STU005", [88, 85, 90, 87]),
    ]
    report = generate_class_report(students)
    for key, value in report.items():
        print(f"{key}: {value}")
''')

    # Config file
    with open(os.path.join(WORKSPACE_DIR, "config.json"), "w") as f:
        json.dump({
            "database": "grades.db",
            "semester": "Fall 2025",
            "max_students": 200,
            "grading_scale": "standard"
        }, f, indent=4)

    # README
    with open(os.path.join(WORKSPACE_DIR, "README.md"), "w") as f:
        f.write("# Student Grade Management System\n\n"
                "A Python tool for tracking and analyzing student grades.\n\n"
                "## Usage\n\n"
                "```bash\npython main.py\n```\n")

    print(f"Workspace created: {WORKSPACE_DIR}")


def setup_initial_state():
    """Ensure VSCode opens with Explorer sidebar visible (default)."""
    # Make sure sidebar is explicitly visible in settings
    update_settings({
        "workbench.sideBar.visible": True,
        "workbench.activityBar.visible": True,
    })
    print(f"VSCode settings updated: sidebar visible = true")


def main():
    create_workspace_files()
    setup_initial_state()

    # Launch VSCode with the workspace folder so Explorer shows content
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0, Explorer sidebar visible")


main()
