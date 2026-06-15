"""
Initial Setup: Configure multi-root workspace in VSCode
Task ID: vscode_py_022
Domain: vs_code

Creates:
- /home/user/backend/ — Flask project with .venv
- /home/user/shared-lib/ — Python package with .venv
- Opens VSCode with /home/user/backend folder
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_022'


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
    # ── Backend Flask Project ──
    backend_dir = os.path.join(WORKDIR, 'backend')
    os.makedirs(backend_dir, exist_ok=True)

    # Create a realistic Flask app structure
    # app.py
    with open(os.path.join(backend_dir, 'app.py'), 'w') as f:
        f.write('''\
from flask import Flask, jsonify, request
from shared_utils import validate_payload

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "version": "1.4.2"})

@app.route('/api/users', methods=['GET'])
def list_users():
    """Return paginated user list from the database."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    # Placeholder — actual DB query would go here
    return jsonify({"page": page, "per_page": per_page, "users": []})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    errors = validate_payload(data, required_fields=['name', 'email'])
    if errors:
        return jsonify({"errors": errors}), 400
    return jsonify({"id": 42, **data}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
''')

    # config.py
    with open(os.path.join(backend_dir, 'config.py'), 'w') as f:
        f.write('''\
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    CORS_ORIGINS = ['http://localhost:3000']

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
''')

    # requirements.txt
    with open(os.path.join(backend_dir, 'requirements.txt'), 'w') as f:
        f.write('''\
flask==3.0.2
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
gunicorn==21.2.0
shared-lib @ file:///home/user/shared-lib
''')

    # Create virtual environment structure (fake but realistic)
    venv_dir = os.path.join(backend_dir, '.venv')
    venv_bin = os.path.join(venv_dir, 'bin')
    os.makedirs(venv_bin, exist_ok=True)

    # Create a python symlink in the venv
    python_real = '/usr/bin/python3'
    python_link = os.path.join(venv_bin, 'python')
    if not os.path.exists(python_link):
        os.symlink(python_real, python_link)

    # pyvenv.cfg
    with open(os.path.join(venv_dir, 'pyvenv.cfg'), 'w') as f:
        f.write('''\
home = /usr/bin
include-system-site-packages = false
version = 3.11.6
''')

    # ── Shared Library Project ──
    shared_dir = os.path.join(WORKDIR, 'shared-lib')
    os.makedirs(shared_dir, exist_ok=True)

    # Package directory
    pkg_dir = os.path.join(shared_dir, 'shared_utils')
    os.makedirs(pkg_dir, exist_ok=True)

    # __init__.py
    with open(os.path.join(pkg_dir, '__init__.py'), 'w') as f:
        f.write('''\
from .validation import validate_payload
from .formatting import format_currency, format_date
from .logging_config import setup_logger

__version__ = "0.3.1"
__all__ = ['validate_payload', 'format_currency', 'format_date', 'setup_logger']
''')

    # validation.py
    with open(os.path.join(pkg_dir, 'validation.py'), 'w') as f:
        f.write('''\
import re
from typing import Any, Dict, List, Optional

def validate_payload(data: Dict[str, Any],
                     required_fields: Optional[List[str]] = None) -> List[str]:
    """Validate an incoming JSON payload against required fields."""
    errors = []
    if not isinstance(data, dict):
        return ["Payload must be a JSON object"]

    for field in (required_fields or []):
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")
        elif isinstance(data[field], str) and not data[field].strip():
            errors.append(f"Field '{field}' must not be blank")

    if 'email' in data and data['email']:
        if not re.match(r'^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$', data['email']):
            errors.append("Invalid email format")

    return errors
''')

    # formatting.py
    with open(os.path.join(pkg_dir, 'formatting.py'), 'w') as f:
        f.write('''\
from datetime import datetime
from typing import Optional

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format a numeric amount as currency string."""
    symbols = {'USD': '$', 'EUR': '\\u20ac', 'GBP': '\\u00a3', 'JPY': '\\u00a5'}
    symbol = symbols.get(currency, currency + ' ')
    if currency == 'JPY':
        return f"{symbol}{amount:,.0f}"
    return f"{symbol}{amount:,.2f}"

def format_date(dt: Optional[datetime] = None, fmt: str = '%Y-%m-%d') -> str:
    """Format a datetime object to string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)
''')

    # logging_config.py
    with open(os.path.join(pkg_dir, 'logging_config.py'), 'w') as f:
        f.write('''\
import logging
import sys

def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """Configure and return a named logger with stdout handler."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(handler)

    return logger
''')

    # pyproject.toml for shared-lib
    with open(os.path.join(shared_dir, 'pyproject.toml'), 'w') as f:
        f.write('''\
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "shared-utils"
version = "0.3.1"
description = "Common utilities shared across backend services"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov"]
''')

    # Create virtual environment for shared-lib
    shared_venv = os.path.join(shared_dir, '.venv')
    shared_venv_bin = os.path.join(shared_venv, 'bin')
    os.makedirs(shared_venv_bin, exist_ok=True)

    shared_python_link = os.path.join(shared_venv_bin, 'python')
    if not os.path.exists(shared_python_link):
        os.symlink(python_real, shared_python_link)

    with open(os.path.join(shared_venv, 'pyvenv.cfg'), 'w') as f:
        f.write('''\
home = /usr/bin
include-system-site-packages = false
version = 3.11.6
''')

    # tests directory
    test_dir = os.path.join(shared_dir, 'tests')
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, 'test_validation.py'), 'w') as f:
        f.write('''\
import pytest
from shared_utils.validation import validate_payload

def test_valid_payload():
    errors = validate_payload({"name": "Alice", "email": "alice@example.com"},
                               required_fields=["name", "email"])
    assert errors == []

def test_missing_required():
    errors = validate_payload({"name": "Bob"},
                               required_fields=["name", "email"])
    assert any("email" in e for e in errors)

def test_invalid_email():
    errors = validate_payload({"name": "Carol", "email": "not-an-email"},
                               required_fields=["name", "email"])
    assert any("email" in e.lower() for e in errors)
''')

    print(f'Initial project files created at {backend_dir} and {shared_dir}')

    # ── GUI Startup ──
    # Open VSCode with the backend folder (initial state per task)
    launch_gui(f'code "{backend_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with /home/user/backend via DISPLAY=:0')


create_initial()
