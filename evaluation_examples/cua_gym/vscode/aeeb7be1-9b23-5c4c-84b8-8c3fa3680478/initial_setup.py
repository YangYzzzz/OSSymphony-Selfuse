"""
Initial Setup: Override workspace settings for secure-app project
Task ID: vscode_we_037
Domain: vscode

Creates a realistic project folder ~/projects/secure-app/ with source files.
Ensures NO .vscode/settings.json exists. Opens VSCode with the folder.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME, "projects", "secure-app")
VSCODE_DIR = os.path.join(PROJECT_DIR, ".vscode")
VSCODE_USER_SETTINGS = os.path.join(HOME, ".config", "Code", "User", "settings.json")


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "tests"), exist_ok=True)

    # Ensure NO .vscode/settings.json exists
    if os.path.exists(VSCODE_DIR):
        import shutil
        shutil.rmtree(VSCODE_DIR)

    # Create realistic source files
    # Main application file
    with open(os.path.join(PROJECT_DIR, "src", "app.py"), "w") as f:
        f.write('''"""Secure App - Authentication and Authorization Service."""

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta


class AuthService:
    """Handles user authentication and token management."""

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self._sessions = {}

    def hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash a password with a random salt using SHA-256."""
        if salt is None:
            salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000
        )
        return hashed.hex(), salt

    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """Verify a password against its hash."""
        check_hash, _ = self.hash_password(password, salt)
        return hmac.compare_digest(check_hash, hashed)

    def create_session(self, user_id: str) -> str:
        """Create a new session token for a user."""
        token = secrets.token_urlsafe(32)
        self._sessions[token] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24),
        }
        return token

    def validate_session(self, token: str) -> dict:
        """Validate a session token and return session data."""
        session = self._sessions.get(token)
        if not session:
            return None
        if datetime.utcnow() > session["expires_at"]:
            del self._sessions[token]
            return None
        return session
''')

    # Database module
    with open(os.path.join(PROJECT_DIR, "src", "database.py"), "w") as f:
        f.write('''"""Database connection and query management."""

import sqlite3
import os
from contextlib import contextmanager


DB_PATH = os.environ.get("SECURE_APP_DB", "secure_app.db")


@contextmanager
def get_connection():
    """Get a database connection with automatic cleanup."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database tables."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
''')

    # Config file
    with open(os.path.join(PROJECT_DIR, "src", "config.py"), "w") as f:
        f.write('''"""Application configuration settings."""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///secure_app.db")
    SESSION_TIMEOUT = int(os.environ.get("SESSION_TIMEOUT", "3600"))
    MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION = int(os.environ.get("LOCKOUT_DURATION", "900"))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
''')

    # Test file
    with open(os.path.join(PROJECT_DIR, "tests", "test_auth.py"), "w") as f:
        f.write('''"""Tests for AuthService."""

import unittest
from src.app import AuthService


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.auth = AuthService(secret_key="test-secret")

    def test_hash_password(self):
        hashed, salt = self.auth.hash_password("securePassword123")
        self.assertIsNotNone(hashed)
        self.assertIsNotNone(salt)

    def test_verify_password_correct(self):
        hashed, salt = self.auth.hash_password("myPassword")
        self.assertTrue(self.auth.verify_password("myPassword", hashed, salt))

    def test_verify_password_incorrect(self):
        hashed, salt = self.auth.hash_password("myPassword")
        self.assertFalse(self.auth.verify_password("wrongPassword", hashed, salt))

    def test_create_session(self):
        token = self.auth.create_session("user_42")
        self.assertIsNotNone(token)

    def test_validate_session(self):
        token = self.auth.create_session("user_42")
        session = self.auth.validate_session(token)
        self.assertIsNotNone(session)
        self.assertEqual(session["user_id"], "user_42")

    def test_validate_invalid_session(self):
        session = self.auth.validate_session("nonexistent-token")
        self.assertIsNone(session)


if __name__ == "__main__":
    unittest.main()
''')

    # Requirements file
    with open(os.path.join(PROJECT_DIR, "requirements.txt"), "w") as f:
        f.write('''flask==3.0.2
gunicorn==21.2.0
python-dotenv==1.0.1
cryptography==42.0.5
pyjwt==2.8.0
''')

    # README
    with open(os.path.join(PROJECT_DIR, "README.md"), "w") as f:
        f.write('''# Secure App

Authentication and authorization service built with Python.

## Setup

```bash
pip install -r requirements.txt
python -m src.database  # Initialize DB
```

## Running Tests

```bash
python -m pytest tests/
```
''')

    # .gitignore
    with open(os.path.join(PROJECT_DIR, ".gitignore"), "w") as f:
        f.write('''__pycache__/
*.pyc
.env
*.db
.vscode/
venv/
''')

    # Ensure user-level settings have telemetry enabled and sidebar on left
    os.makedirs(os.path.dirname(VSCODE_USER_SETTINGS), exist_ok=True)
    user_settings = {}
    if os.path.exists(VSCODE_USER_SETTINGS):
        try:
            with open(VSCODE_USER_SETTINGS, "r") as f:
                import re
                content = f.read()
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                user_settings = json.loads(content)
        except (json.JSONDecodeError, Exception):
            user_settings = {}

    # Set telemetry enabled and sidebar left (defaults that task should override)
    user_settings["telemetry.telemetryLevel"] = "all"
    user_settings["workbench.sideBar.location"] = "left"
    # Make sure activityBar is visible (not hidden)
    if "workbench.activityBar.location" in user_settings:
        del user_settings["workbench.activityBar.location"]

    with open(VSCODE_USER_SETTINGS, "w") as f:
        json.dump(user_settings, f, indent=4)

    print(f"Project created at: {PROJECT_DIR}")
    print(f"User settings updated at: {VSCODE_USER_SETTINGS}")
    print(f".vscode/settings.json does NOT exist: {not os.path.exists(os.path.join(VSCODE_DIR, 'settings.json'))}")

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
