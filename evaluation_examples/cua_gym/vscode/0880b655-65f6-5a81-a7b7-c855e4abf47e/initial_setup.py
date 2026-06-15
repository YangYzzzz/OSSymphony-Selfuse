"""
Initial Setup: Configure a complex multi-root workspace with three folders
Task ID: vscode_we_033
Domain: vscode

Creates:
- ~/projects/ directory with frontend, backend, shared subfolders
- platform.code-workspace file pointing to all three
- Realistic project files in each folder
- NO .vscode/settings.json in any folder
- Opens VSCode with the workspace
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, "projects")

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

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def create_initial():
    # ---- Frontend folder (React/JS project) ----
    frontend = os.path.join(PROJECTS, "frontend")

    create_file(os.path.join(frontend, "package.json"), json.dumps({
        "name": "platform-frontend",
        "version": "2.1.0",
        "description": "Platform web frontend built with React",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "axios": "^1.6.2",
            "@mui/material": "^5.15.0"
        },
        "devDependencies": {
            "prettier": "^3.1.0",
            "eslint": "^8.55.0"
        }
    }, indent=2))

    create_file(os.path.join(frontend, "src", "App.js"), """\
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import SettingsPage from './components/SettingsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/profile/:userId" element={<UserProfile />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""")

    create_file(os.path.join(frontend, "src", "components", "Dashboard.js"), """\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get('/api/metrics');
        setMetrics(response.data);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="dashboard-container">
      <h1>Platform Analytics</h1>
      <div className="metrics-grid">
        <div className="metric-card">
          <span className="label">Active Users</span>
          <span className="value">{metrics?.activeUsers || 0}</span>
        </div>
        <div className="metric-card">
          <span className="label">Revenue MTD</span>
          <span className="value">${metrics?.revenueMTD || '0.00'}</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
""")

    # ---- Backend folder (Python Flask project) ----
    backend = os.path.join(PROJECTS, "backend")

    create_file(os.path.join(backend, "requirements.txt"), """\
flask==3.0.0
flask-cors==4.0.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
celery==5.3.6
redis==5.0.1
black==23.12.0
pytest==7.4.3
""")

    create_file(os.path.join(backend, "app", "__init__.py"), """\
from flask import Flask
from flask_cors import CORS

def create_app(config_name="development"):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(f"config.{config_name}")

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
""")

    create_file(os.path.join(backend, "app", "routes.py"), """\
from flask import Blueprint, jsonify, request
from app.models import User, Transaction

api_bp = Blueprint("api", __name__)


@api_bp.route("/metrics", methods=["GET"])
def get_metrics():
    active_users = User.query.filter_by(is_active=True).count()
    total_revenue = Transaction.query.with_entities(
        Transaction.amount
    ).filter(
        Transaction.status == "completed"
    ).all()

    return jsonify({
        "activeUsers": active_users,
        "revenueMTD": sum(t.amount for t in total_revenue),
        "conversionRate": 0.034,
    })


@api_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
""")

    create_file(os.path.join(backend, "app", "models.py"), """\
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullName": self.full_name,
            "department": self.department,
            "isActive": self.is_active,
        }


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
""")

    # ---- Shared library folder ----
    shared = os.path.join(PROJECTS, "shared")

    create_file(os.path.join(shared, "setup.py"), """\
from setuptools import setup, find_packages

setup(
    name="platform-shared",
    version="1.3.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0",
        "python-dateutil>=2.8",
    ],
    author="Platform Team",
    description="Shared utilities and data models for the Platform project",
)
""")

    create_file(os.path.join(shared, "platform_shared", "__init__.py"), """\
from .validators import validate_email, validate_currency
from .constants import DEPARTMENTS, STATUS_CODES

__version__ = "1.3.0"
""")

    create_file(os.path.join(shared, "platform_shared", "validators.py"), """\
import re
from datetime import datetime

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')


def validate_email(email: str) -> bool:
    \"\"\"Validate email format.\"\"\"
    return bool(EMAIL_PATTERN.match(email))


def validate_currency(amount: float, min_val: float = 0.0, max_val: float = 1_000_000.0) -> bool:
    \"\"\"Validate currency amount is within acceptable range.\"\"\"
    return min_val <= amount <= max_val


def validate_date_range(start: str, end: str, fmt: str = "%Y-%m-%d") -> bool:
    \"\"\"Validate that start date is before end date.\"\"\"
    try:
        start_dt = datetime.strptime(start, fmt)
        end_dt = datetime.strptime(end, fmt)
        return start_dt < end_dt
    except ValueError:
        return False
""")

    create_file(os.path.join(shared, "platform_shared", "constants.py"), """\
DEPARTMENTS = [
    "Engineering",
    "Marketing",
    "Sales",
    "Customer Support",
    "Finance",
    "Human Resources",
    "Product Management",
]

STATUS_CODES = {
    "pending": 100,
    "processing": 200,
    "completed": 300,
    "failed": 400,
    "refunded": 500,
}

CURRENCY_FORMATS = {
    "USD": {"symbol": "$", "decimal_places": 2},
    "EUR": {"symbol": "\\u20ac", "decimal_places": 2},
    "GBP": {"symbol": "\\u00a3", "decimal_places": 2},
    "JPY": {"symbol": "\\u00a5", "decimal_places": 0},
}
""")

    # ---- Workspace file ----
    workspace_path = os.path.join(PROJECTS, "platform.code-workspace")
    workspace = {
        "folders": [
            {"path": "frontend"},
            {"path": "backend"},
            {"path": "shared"}
        ],
        "settings": {}
    }
    with open(workspace_path, "w") as f:
        json.dump(workspace, f, indent=4)

    print(f"Created workspace: {workspace_path}")
    print(f"Created frontend project: {frontend}")
    print(f"Created backend project: {backend}")
    print(f"Created shared library: {shared}")

    # Verify no .vscode/settings.json files exist
    for folder in ["frontend", "backend", "shared"]:
        settings_path = os.path.join(PROJECTS, folder, ".vscode", "settings.json")
        assert not os.path.exists(settings_path), f"ERROR: {settings_path} should not exist!"

    # Launch VSCode with the workspace
    launch_gui(f'code "{workspace_path}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with platform.code-workspace on DISPLAY=:0")

create_initial()
