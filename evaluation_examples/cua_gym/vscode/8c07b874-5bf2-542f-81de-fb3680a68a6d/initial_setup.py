"""
Initial Setup: Open VSCode with cs101/project workspace, no files open as tabs.
Task ID: vscode_stu_085
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_085'
PROJECT_DIR = os.path.join(WORKDIR, 'cs101', 'project')


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- main.py: A small Flask web application ---
    main_py = '''\
"""CS101 Project - Student Grade Portal"""

from flask import Flask, render_template, jsonify
from utils import calculate_gpa, validate_student_id
from config import DATABASE_URI, SECRET_KEY, MAX_RETRIES

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    """Render the main dashboard page."""
    return render_template("index.html", title="Grade Portal")


@app.route("/api/students/<student_id>/gpa")
def get_student_gpa(student_id):
    """Return GPA for a given student."""
    if not validate_student_id(student_id):
        return jsonify({"error": "Invalid student ID format"}), 400

    gpa = calculate_gpa(student_id)
    return jsonify({"student_id": student_id, "gpa": gpa})


@app.route("/api/courses")
def list_courses():
    """List all available courses for the current semester."""
    courses = [
        {"code": "CS101", "name": "Intro to Computer Science", "credits": 3},
        {"code": "CS201", "name": "Data Structures", "credits": 4},
        {"code": "MATH150", "name": "Discrete Mathematics", "credits": 3},
        {"code": "CS301", "name": "Algorithms", "credits": 4},
    ]
    return jsonify(courses)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # --- utils.py: Helper functions ---
    utils_py = '''\
"""Utility functions for the Grade Portal application."""

import re
import statistics
from typing import Optional

# In-memory grade store (would be database in production)
_grade_store = {
    "STU-2024-001": {"CS101": 92, "MATH150": 88, "CS201": 95},
    "STU-2024-002": {"CS101": 78, "CS201": 82, "CS301": 71},
    "STU-2024-003": {"CS101": 95, "MATH150": 97, "CS201": 93, "CS301": 91},
}

STUDENT_ID_PATTERN = re.compile(r"^STU-\\d{4}-\\d{3}$")


def validate_student_id(student_id: str) -> bool:
    """Validate that a student ID matches the expected format."""
    return bool(STUDENT_ID_PATTERN.match(student_id))


def calculate_gpa(student_id: str) -> Optional[float]:
    """Calculate GPA on a 4.0 scale for the given student."""
    grades = _grade_store.get(student_id)
    if not grades:
        return None

    gpa_points = []
    for course, score in grades.items():
        if score >= 90:
            gpa_points.append(4.0)
        elif score >= 80:
            gpa_points.append(3.0)
        elif score >= 70:
            gpa_points.append(2.0)
        elif score >= 60:
            gpa_points.append(1.0)
        else:
            gpa_points.append(0.0)

    return round(statistics.mean(gpa_points), 2)


def format_percentage(value: float) -> str:
    """Format a numeric value as a percentage string."""
    return f"{value:.1f}%"


def get_class_average(course_code: str) -> Optional[float]:
    """Calculate the class average for a specific course."""
    scores = []
    for grades in _grade_store.values():
        if course_code in grades:
            scores.append(grades[course_code])
    return round(statistics.mean(scores), 2) if scores else None
'''
    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py)

    # --- config.py: Application configuration ---
    config_py = '''\
"""Configuration settings for the Grade Portal application."""

import os

# Database configuration
DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    "postgresql://gradeportal:securepass@localhost:5432/grades_db"
)

# Application settings
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # seconds
ITEMS_PER_PAGE = 25

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature flags
ENABLE_NOTIFICATIONS = True
ENABLE_GRADE_EXPORT = False
MAINTENANCE_MODE = False

# Semester configuration
CURRENT_SEMESTER = "Fall 2025"
REGISTRATION_OPEN = True
MAX_COURSES_PER_STUDENT = 6
'''
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write(config_py)

    print(f"Project files created in {PROJECT_DIR}")
    print(f"  - main.py")
    print(f"  - utils.py")
    print(f"  - config.py")

    # Kill any existing VSCode instances to start fresh (ignore if none running)
    subprocess.run(["pkill", "-f", "^/usr/share/code"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    # Launch VSCode with the project folder (no files open)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with project workspace, no files open")


create_initial()
