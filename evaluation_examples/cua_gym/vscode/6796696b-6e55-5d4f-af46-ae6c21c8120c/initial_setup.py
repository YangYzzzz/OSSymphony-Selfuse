"""
Initial Setup: Select Python interpreter from virtual environment
Task ID: vscode_stu_040
Domain: vscode

Creates:
- A Python project at ~/cs101/ with realistic course files
- A virtual environment at ~/cs101/venv/
- Opens VSCode with the project folder (system Python is the default)
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
TASK_ID = 'vscode_stu_040'
PROJECT_DIR = os.path.join(HOME, 'cs101')
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project():
    """Create a realistic CS101 Python project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main assignment file
    main_py = os.path.join(PROJECT_DIR, 'assignment3.py')
    with open(main_py, 'w') as f:
        f.write('''\
#!/usr/bin/env python3
"""
CS101 - Introduction to Computer Science
Assignment 3: Data Analysis with Lists

Author: Student
Date: 2026-03-28
"""

def calculate_average(grades):
    """Calculate the average of a list of grades."""
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def find_highest(grades):
    """Find the highest grade in the list."""
    if not grades:
        return None
    return max(grades)


def find_lowest(grades):
    """Find the lowest grade in the list."""
    if not grades:
        return None
    return min(grades)


def count_passing(grades, threshold=60):
    """Count the number of passing grades."""
    return sum(1 for g in grades if g >= threshold)


def grade_distribution(grades):
    """Return a dictionary with grade distribution."""
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades:
        if g >= 90:
            distribution["A"] += 1
        elif g >= 80:
            distribution["B"] += 1
        elif g >= 70:
            distribution["C"] += 1
        elif g >= 60:
            distribution["D"] += 1
        else:
            distribution["F"] += 1
    return distribution


def main():
    midterm_grades = [85, 92, 78, 64, 95, 88, 72, 56, 91, 83,
                      67, 74, 89, 93, 61, 77, 82, 96, 58, 71]

    print("CS101 - Midterm Grade Analysis")
    print("=" * 40)
    print(f"Number of students: {len(midterm_grades)}")
    print(f"Average grade: {calculate_average(midterm_grades):.1f}")
    print(f"Highest grade: {find_highest(midterm_grades)}")
    print(f"Lowest grade: {find_lowest(midterm_grades)}")
    print(f"Passing students: {count_passing(midterm_grades)}")
    print()

    dist = grade_distribution(midterm_grades)
    print("Grade Distribution:")
    for letter, count in dist.items():
        bar = "#" * count
        print(f"  {letter}: {bar} ({count})")


if __name__ == "__main__":
    main()
''')

    # Helper module
    utils_py = os.path.join(PROJECT_DIR, 'utils.py')
    with open(utils_py, 'w') as f:
        f.write('''\
"""Utility functions for CS101 assignments."""

import csv
import os


def read_grades_csv(filepath):
    """Read grades from a CSV file."""
    grades = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            grades.append({
                'name': row['name'],
                'grade': float(row['grade'])
            })
    return grades


def save_report(filepath, content):
    """Save a text report to file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
''')

    # Requirements file
    req_txt = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(req_txt, 'w') as f:
        f.write('numpy==1.24.0\nmatplotlib==3.7.1\npandas==2.0.0\n')

    # README
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''\
# CS101 - Introduction to Computer Science

## Assignment 3: Data Analysis with Lists

### Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

### Running
```
python assignment3.py
```
''')


def create_venv():
    """Create a virtual environment at ~/cs101/venv/."""
    subprocess.run(
        ['python3', '-m', 'venv', '--without-pip', VENV_DIR],
        check=True,
        timeout=60
    )
    print(f'Virtual environment created at {VENV_DIR}')

    # Verify the interpreter exists
    venv_python = os.path.join(VENV_DIR, 'bin', 'python3')
    assert os.path.isfile(venv_python), f'venv python3 not found at {venv_python}'
    print(f'Verified interpreter: {venv_python}')


def setup_vscode_settings():
    """Ensure VSCode settings exist with system Python as default (no venv)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.isfile(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Ensure system Python is the default - explicitly NOT the venv
    settings['python.defaultInterpreterPath'] = '/usr/bin/python3'

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured with system Python')


def main():
    # Install Python extension if not present
    subprocess.run(['code', '--install-extension', 'ms-python.python'],
                   capture_output=True, timeout=60)
    print('Python extension installed/verified')

    create_project()
    print(f'Project created at {PROJECT_DIR}')

    create_venv()
    setup_vscode_settings()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
