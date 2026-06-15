"""
Initial Setup: Configure VSCode with default Dark+ theme and a realistic workspace
Task ID: vscode_gf5_010
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_010'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = os.path.join(WORKDIR, "webapp-project")


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


def create_project_files():
    """Create a realistic project workspace for the developer."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application file
    with open(os.path.join(PROJECT_DIR, "app.py"), "w") as f:
        f.write('''"""
Flask web application for employee management portal.
Handles user authentication, dashboard views, and API endpoints.
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

EMPLOYEES = [
    {"id": 1, "name": "Sarah Chen", "department": "Engineering", "role": "Senior Developer"},
    {"id": 2, "name": "Marcus Johnson", "department": "Marketing", "role": "Campaign Manager"},
    {"id": 3, "name": "Aisha Patel", "department": "Finance", "role": "Financial Analyst"},
    {"id": 4, "name": "Diego Rivera", "department": "Engineering", "role": "DevOps Engineer"},
    {"id": 5, "name": "Emma Larsson", "department": "Design", "role": "UX Lead"},
]


@app.route("/")
def dashboard():
    """Render the main dashboard with employee overview."""
    return render_template("dashboard.html", employees=EMPLOYEES,
                         timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))


@app.route("/api/employees")
def get_employees():
    """REST API endpoint for employee data."""
    dept = request.args.get("department")
    if dept:
        filtered = [e for e in EMPLOYEES if e["department"].lower() == dept.lower()]
        return jsonify(filtered)
    return jsonify(EMPLOYEES)


@app.route("/api/stats")
def get_stats():
    """Return department statistics."""
    dept_counts = {}
    for emp in EMPLOYEES:
        dept = emp["department"]
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return jsonify({"total": len(EMPLOYEES), "by_department": dept_counts})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
''')

    # Config file
    with open(os.path.join(PROJECT_DIR, "config.py"), "w") as f:
        f.write('''"""Application configuration settings."""

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///employees.db")
    LOG_LEVEL = "INFO"
    ITEMS_PER_PAGE = 25
    SESSION_TIMEOUT = 3600
    ALLOWED_ORIGINS = ["http://localhost:3000", "https://portal.company.com"]

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"
''')

    # Requirements file
    with open(os.path.join(PROJECT_DIR, "requirements.txt"), "w") as f:
        f.write('''flask==3.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
requests==2.31.0
pytest==7.4.3
''')

    # README
    with open(os.path.join(PROJECT_DIR, "README.md"), "w") as f:
        f.write('''# Employee Management Portal

A Flask-based web application for managing employee data and generating department reports.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints

- `GET /api/employees` - List all employees (filter by `?department=`)
- `GET /api/stats` - Department statistics
''')

    print(f"Project files created in {PROJECT_DIR}")


def setup_vscode_settings():
    """Ensure VSCode has default Dark+ theme (no Dracula, no color overrides)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings and ensure no Dracula or color customizations
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure default theme; remove any Dracula or colorCustomizations if present
    settings.pop("workbench.colorTheme", None)
    settings.pop("workbench.colorCustomizations", None)

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings configured at {SETTINGS_PATH}")


def ensure_no_dracula():
    """Ensure Dracula theme extension is NOT installed."""
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    if "dracula-theme.theme-dracula" in result.stdout.lower():
        subprocess.run(
            ["code", "--uninstall-extension", "dracula-theme.theme-dracula"],
            capture_output=True, text=True
        )
        print("Removed pre-existing Dracula extension")
    else:
        print("Dracula extension not installed (expected)")


def main():
    create_project_files()
    setup_vscode_settings()
    ensure_no_dracula()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


main()
