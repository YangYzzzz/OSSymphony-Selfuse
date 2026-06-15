"""
Initial Setup: Create VSCode environment with Python workspace, no custom snippets.
Task ID: vscode_stu_064
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_064'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SNIPPETS_DIR = os.path.join(VSCODE_USER, "snippets")
PYTHON_SNIPPETS = os.path.join(SNIPPETS_DIR, "python.json")

# Project directory for the student workspace
PROJECT_DIR = os.path.join(WORKDIR, "python_project")


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
    # Ensure no custom Python snippets exist
    if os.path.exists(PYTHON_SNIPPETS):
        os.remove(PYTHON_SNIPPETS)
        print(f"Removed existing python.json snippets file")

    # Create a realistic Python project workspace
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a main.py with realistic student code
    main_py = os.path.join(PROJECT_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''\
# Student Project: Course Registration System
# TODO: Create a Student class using the 'myclass' snippet

def calculate_gpa(grades):
    """Calculate GPA from a list of grade points."""
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def format_transcript(student_name, courses):
    """Format a student transcript for printing."""
    header = f"=== Transcript for {student_name} ==="
    lines = [header]
    for course in courses:
        lines.append(f"  {course['name']}: {course['grade']}")
    return "\\n".join(lines)


if __name__ == "__main__":
    sample_grades = [3.7, 3.3, 4.0, 3.0, 3.7]
    gpa = calculate_gpa(sample_grades)
    print(f"Sample GPA: {gpa:.2f}")
''')
    print(f"Created {main_py}")

    # Create a utils.py helper file
    utils_py = os.path.join(PROJECT_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write('''\
# Utility functions for the course registration system

import datetime


def get_current_semester():
    """Return the current semester string based on today's date."""
    month = datetime.date.today().month
    year = datetime.date.today().year
    if month <= 5:
        return f"Spring {year}"
    elif month <= 8:
        return f"Summer {year}"
    else:
        return f"Fall {year}"


def validate_student_id(student_id):
    """Validate that a student ID follows the format: 2 letters + 6 digits."""
    if len(student_id) != 8:
        return False
    return student_id[:2].isalpha() and student_id[2:].isdigit()
''')
    print(f"Created {utils_py}")

    # Create a requirements.txt
    req_txt = os.path.join(PROJECT_DIR, "requirements.txt")
    with open(req_txt, "w") as f:
        f.write("pytest>=7.0\nblack>=23.0\n")
    print(f"Created {req_txt}")

    # Ensure VSCode User config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Launch VSCode with the project folder open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
