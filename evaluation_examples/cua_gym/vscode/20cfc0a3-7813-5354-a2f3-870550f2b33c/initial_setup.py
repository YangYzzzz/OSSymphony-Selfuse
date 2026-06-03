"""
Initial Setup: Set up a Python project for type-safe development
Task ID: vscode_py_079
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_079'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
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


def create_workspace_files():
    """Create a realistic Python project with third-party library usage."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # Main application file
    with open(os.path.join(WORKSPACE, 'app.py'), 'w') as f:
        f.write('''\
"""Main application entry point for the analytics dashboard."""

from typing import Optional
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request

from models import UserProfile, AnalyticsEvent
from database import DatabaseConnection
from utils import format_currency, parse_date_range

app = Flask(__name__)
db = DatabaseConnection(host="localhost", port=5432, database="analytics")


@app.route("/api/users/<int:user_id>")
def get_user(user_id: int):
    profile = db.get_user_profile(user_id)
    if profile is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(profile.to_dict())


@app.route("/api/analytics/summary")
def analytics_summary():
    start_date, end_date = parse_date_range(request.args)
    events = db.query_events(start_date, end_date)

    df = pd.DataFrame([e.to_dict() for e in events])
    summary = {
        "total_events": len(events),
        "unique_users": df["user_id"].nunique(),
        "avg_duration": float(np.mean(df["duration_ms"])),
        "revenue": format_currency(df["revenue"].sum()),
    }
    return jsonify(summary)


@app.route("/api/analytics/export")
def export_report():
    data = db.get_monthly_report()
    df = pd.DataFrame(data)
    output_path = "/tmp/report.csv"
    df.to_csv(output_path, index=False)
    return jsonify({"status": "exported", "path": output_path})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
''')

    # Models file
    with open(os.path.join(WORKSPACE, 'models.py'), 'w') as f:
        f.write('''\
"""Data models for the analytics platform."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class UserProfile:
    user_id: int
    username: str
    email: str
    created_at: datetime
    subscription_tier: str = "free"
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "subscription_tier": self.subscription_tier,
        }


@dataclass
class AnalyticsEvent:
    event_id: str
    user_id: int
    event_type: str
    timestamp: datetime
    duration_ms: float
    revenue: float = 0.0
    properties: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "revenue": self.revenue,
        }


@dataclass
class MonthlyReport:
    month: str
    total_users: int
    active_users: int
    total_revenue: float
    events_count: int
    top_events: List[str] = field(default_factory=list)
''')

    # Database connection module
    with open(os.path.join(WORKSPACE, 'database.py'), 'w') as f:
        f.write('''\
"""Database connection and query utilities."""

from typing import List, Optional, Tuple
from datetime import datetime

from models import UserProfile, AnalyticsEvent


class DatabaseConnection:
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self._connected = False

    def connect(self) -> bool:
        """Establish connection to the PostgreSQL database."""
        self._connected = True
        return True

    def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        """Fetch a user profile by ID."""
        # Placeholder implementation
        return None

    def query_events(
        self, start_date: datetime, end_date: datetime
    ) -> List[AnalyticsEvent]:
        """Query analytics events within a date range."""
        return []

    def get_monthly_report(self) -> List[dict]:
        """Generate monthly report data."""
        return []

    def close(self):
        """Close the database connection."""
        self._connected = False
''')

    # Utility functions
    with open(os.path.join(WORKSPACE, 'utils.py'), 'w') as f:
        f.write('''\
"""Utility functions for data formatting and parsing."""

from datetime import datetime
from typing import Tuple, Optional


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a numeric amount as a currency string."""
    symbols = {"USD": "$", "EUR": "\\u20ac", "GBP": "\\u00a3"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def parse_date_range(args) -> Tuple[datetime, datetime]:
    """Parse start_date and end_date from request arguments."""
    start = args.get("start_date", "2025-01-01")
    end = args.get("end_date", "2025-12-31")
    return datetime.fromisoformat(start), datetime.fromisoformat(end)


def calculate_growth_rate(
    current: float, previous: float
) -> Optional[float]:
    """Calculate percentage growth rate between two values."""
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate a string to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
''')

    # requirements.txt
    with open(os.path.join(WORKSPACE, 'requirements.txt'), 'w') as f:
        f.write('''\
flask==3.0.0
pandas==2.1.4
numpy==1.26.2
requests==2.31.0
sqlalchemy==2.0.23
pydantic==2.5.3
''')

    print(f'Workspace created at: {WORKSPACE}')


def configure_vscode_settings():
    """Set initial VSCode settings with type checking OFF."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings if any
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set initial state: type checking is OFF
    settings.update({
        "python.analysis.typeCheckingMode": "off",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured at: {SETTINGS_PATH}')


def main():
    create_workspace_files()
    configure_vscode_settings()

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
