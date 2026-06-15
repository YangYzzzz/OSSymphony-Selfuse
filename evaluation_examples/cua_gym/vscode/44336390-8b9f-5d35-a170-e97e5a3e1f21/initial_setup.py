"""
Initial Setup: Create Python monorepo workspace for VSCode tasks.json task
Task ID: vscode_td_045
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_045'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-monorepo')


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
    # Create project directory structure
    dirs = [
        os.path.join(PROJECT_DIR, 'packages', 'core', 'src'),
        os.path.join(PROJECT_DIR, 'packages', 'core', 'tests'),
        os.path.join(PROJECT_DIR, 'packages', 'api', 'src'),
        os.path.join(PROJECT_DIR, 'packages', 'api', 'tests'),
        os.path.join(PROJECT_DIR, 'packages', 'cli', 'src'),
        os.path.join(PROJECT_DIR, 'packages', 'cli', 'tests'),
        os.path.join(PROJECT_DIR, 'docs'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- packages/core ---
    with open(os.path.join(PROJECT_DIR, 'packages', 'core', 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'packages', 'core', 'src', 'models.py'), 'w') as f:
        f.write('''"""Core data models for the analytics platform."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: str
    email: str
    display_name: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True


@dataclass
class Event:
    event_id: str
    user_id: str
    event_type: str
    timestamp: datetime
    properties: dict = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class Metric:
    name: str
    value: float
    unit: str
    recorded_at: datetime
    tags: dict = None
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'core', 'tests', 'test_models.py'), 'w') as f:
        f.write('''"""Tests for core data models."""

import pytest
from datetime import datetime
from src.models import User, Event, Metric


class TestUser:
    def test_create_user(self):
        user = User(
            user_id="usr_001",
            email="sarah.chen@example.com",
            display_name="Sarah Chen",
            created_at=datetime(2024, 1, 15, 9, 30),
        )
        assert user.is_active is True
        assert user.last_login is None

    def test_user_inactive(self):
        user = User(
            user_id="usr_002",
            email="marcus.johnson@example.com",
            display_name="Marcus Johnson",
            created_at=datetime(2023, 6, 1),
            is_active=False,
        )
        assert user.is_active is False


class TestEvent:
    def test_event_default_properties(self):
        event = Event(
            event_id="evt_100",
            user_id="usr_001",
            event_type="page_view",
            timestamp=datetime(2025, 3, 15, 14, 22),
        )
        assert event.properties == {}
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'core', 'setup.py'), 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="monorepo-core",
    version="0.4.2",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0",
    ],
)
''')

    # --- packages/api ---
    with open(os.path.join(PROJECT_DIR, 'packages', 'api', 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'packages', 'api', 'src', 'routes.py'), 'w') as f:
        f.write('''"""API route handlers for the analytics service."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/v1/users", methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    return jsonify({"users": [], "page": page, "per_page": per_page})


@app.route("/api/v1/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "event_type" not in data:
        return jsonify({"error": "event_type is required"}), 400
    return jsonify({"status": "accepted", "event_id": "evt_new"}), 202


@app.route("/api/v1/metrics/summary", methods=["GET"])
def metrics_summary():
    return jsonify({
        "total_users": 1247,
        "active_sessions": 89,
        "events_today": 15432,
    })
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'api', 'tests', 'test_routes.py'), 'w') as f:
        f.write('''"""Tests for API route handlers."""

import pytest
from src.routes import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestUsersEndpoint:
    def test_list_users_default(self, client):
        resp = client.get("/api/v1/users")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["page"] == 1

    def test_list_users_pagination(self, client):
        resp = client.get("/api/v1/users?page=3&per_page=10")
        data = resp.get_json()
        assert data["page"] == 3
        assert data["per_page"] == 10


class TestEventsEndpoint:
    def test_create_event_missing_type(self, client):
        resp = client.post("/api/v1/events", json={"user_id": "usr_001"})
        assert resp.status_code == 400
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'api', 'setup.py'), 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="monorepo-api",
    version="0.4.2",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0",
        "monorepo-core",
    ],
)
''')

    # --- packages/cli ---
    with open(os.path.join(PROJECT_DIR, 'packages', 'cli', 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'packages', 'cli', 'src', 'main.py'), 'w') as f:
        f.write('''"""CLI entry point for the analytics toolkit."""

import argparse
import sys


def build_parser():
    parser = argparse.ArgumentParser(
        prog="analytics",
        description="Analytics platform CLI toolkit",
    )
    sub = parser.add_subparsers(dest="command")

    # Export command
    export_p = sub.add_parser("export", help="Export analytics data")
    export_p.add_argument("--format", choices=["csv", "json", "parquet"], default="csv")
    export_p.add_argument("--start-date", required=True)
    export_p.add_argument("--end-date", required=True)

    # Report command
    report_p = sub.add_parser("report", help="Generate summary report")
    report_p.add_argument("--period", choices=["daily", "weekly", "monthly"], default="weekly")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    print(f"Running {args.command}...")


if __name__ == "__main__":
    main()
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'cli', 'tests', 'test_main.py'), 'w') as f:
        f.write('''"""Tests for CLI entry point."""

import pytest
from src.main import build_parser


class TestParser:
    def test_export_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["export", "--start-date", "2025-01-01", "--end-date", "2025-03-31"])
        assert args.format == "csv"
        assert args.command == "export"

    def test_report_period(self):
        parser = build_parser()
        args = parser.parse_args(["report", "--period", "monthly"])
        assert args.period == "monthly"
''')

    with open(os.path.join(PROJECT_DIR, 'packages', 'cli', 'setup.py'), 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="monorepo-cli",
    version="0.4.2",
    packages=find_packages(),
    install_requires=[
        "monorepo-core",
    ],
    entry_points={
        "console_scripts": [
            "analytics=src.main:main",
        ],
    },
)
''')

    # --- docs ---
    with open(os.path.join(PROJECT_DIR, 'docs', 'conf.py'), 'w') as f:
        f.write('''"""Sphinx configuration for Python Monorepo documentation."""

project = "Python Monorepo"
copyright = "2025, Analytics Team"
author = "Analytics Team"
release = "0.4.2"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]
''')

    with open(os.path.join(PROJECT_DIR, 'docs', 'index.rst'), 'w') as f:
        f.write('''Python Monorepo Documentation
=============================

Welcome to the Python Monorepo project documentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   api-reference
   cli-usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
''')

    # --- Root files ---
    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.flake8]
max-line-length = 120
exclude = [".git", "__pycache__", "docs/_build", "*.egg-info"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
''')

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# Python Monorepo

A modular analytics platform built as a Python monorepo.

## Packages

- **core** — Shared data models and utilities
- **api** — REST API service (Flask)
- **cli** — Command-line toolkit

## Development

```bash
# Lint all packages
flake8 packages/

# Run tests for a specific package
pytest packages/core/tests

# Build documentation
sphinx-build docs/ docs/_build
```
''')

    # Ensure NO .vscode folder exists (negative constraint)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  packages/core/ packages/api/ packages/cli/ docs/')
    print(f'  No .vscode folder present')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
