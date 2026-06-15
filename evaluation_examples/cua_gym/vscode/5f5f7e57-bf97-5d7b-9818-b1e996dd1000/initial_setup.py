"""
Initial Setup: Set up Python test explorer in VSCode
Task ID: vscode_we_073
Domain: vscode

Creates a realistic Python API service project at ~/projects/api-service/
with src/ and tests/ directories. No .vscode/settings.json exists.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'api-service')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
TESTS_DIR = os.path.join(PROJECT_DIR, 'tests')


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
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # Remove any existing .vscode/settings.json (ensure clean state)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    settings_path = os.path.join(vscode_dir, 'settings.json')
    if os.path.exists(settings_path):
        os.remove(settings_path)
    if os.path.exists(vscode_dir) and not os.listdir(vscode_dir):
        os.rmdir(vscode_dir)

    # --- src/__init__.py ---
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # --- src/app.py ---
    with open(os.path.join(SRC_DIR, 'app.py'), 'w') as f:
        f.write('''"""API Service - Main application module."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: int
    name: str
    email: str
    role: str = "viewer"


class UserService:
    """Manages user operations for the API service."""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, name: str, email: str, role: str = "viewer") -> User:
        user = User(user_id=self._next_id, name=name, email=email, role=role)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def list_users(self) -> list[User]:
        return list(self._users.values())

    def delete_user(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def update_user_role(self, user_id: int, new_role: str) -> Optional[User]:
        user = self._users.get(user_id)
        if user:
            user.role = new_role
        return user
''')

    # --- src/database.py ---
    with open(os.path.join(SRC_DIR, 'database.py'), 'w') as f:
        f.write('''"""Database connection and query utilities."""

import sqlite3
from contextlib import contextmanager
from typing import Any


class DatabaseManager:
    """Lightweight SQLite database manager."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        with self.connection() as conn:
            cursor = conn.execute(query, params)
            if cursor.description:
                return [dict(row) for row in cursor.fetchall()]
            return []

    def init_schema(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'viewer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
''')

    # --- src/validators.py ---
    with open(os.path.join(SRC_DIR, 'validators.py'), 'w') as f:
        f.write('''"""Input validation utilities."""

import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_role(role: str) -> bool:
    allowed_roles = {"admin", "editor", "viewer", "moderator"}
    return role.lower() in allowed_roles


def validate_username(name: str) -> bool:
    if not name or len(name) < 2 or len(name) > 64:
        return False
    return all(c.isalnum() or c in " ._-" for c in name)
''')

    # --- tests/__init__.py ---
    with open(os.path.join(TESTS_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # --- tests/test_app.py ---
    with open(os.path.join(TESTS_DIR, 'test_app.py'), 'w') as f:
        f.write('''"""Tests for the UserService class."""

import pytest
from src.app import UserService, User


@pytest.fixture
def service():
    return UserService()


class TestUserService:
    def test_create_user(self, service):
        user = service.create_user("Alice Park", "alice@example.com")
        assert user.name == "Alice Park"
        assert user.email == "alice@example.com"
        assert user.role == "viewer"
        assert user.user_id == 1

    def test_get_user(self, service):
        created = service.create_user("Bob Rivera", "bob@example.com", role="admin")
        fetched = service.get_user(created.user_id)
        assert fetched is not None
        assert fetched.name == "Bob Rivera"
        assert fetched.role == "admin"

    def test_get_nonexistent_user(self, service):
        assert service.get_user(999) is None

    def test_list_users(self, service):
        service.create_user("Clara Nguyen", "clara@example.com")
        service.create_user("David Kim", "david@example.com")
        users = service.list_users()
        assert len(users) == 2

    def test_delete_user(self, service):
        user = service.create_user("Eve Torres", "eve@example.com")
        assert service.delete_user(user.user_id) is True
        assert service.get_user(user.user_id) is None

    def test_delete_nonexistent(self, service):
        assert service.delete_user(999) is False

    def test_update_role(self, service):
        user = service.create_user("Frank Liu", "frank@example.com")
        updated = service.update_user_role(user.user_id, "editor")
        assert updated.role == "editor"
''')

    # --- tests/test_validators.py ---
    with open(os.path.join(TESTS_DIR, 'test_validators.py'), 'w') as f:
        f.write('''"""Tests for input validation functions."""

import pytest
from src.validators import validate_email, validate_role, validate_username


class TestEmailValidation:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_no_at(self):
        assert validate_email("userexample.com") is False

    def test_invalid_no_domain(self):
        assert validate_email("user@") is False


class TestRoleValidation:
    @pytest.mark.parametrize("role", ["admin", "editor", "viewer", "moderator"])
    def test_valid_roles(self, role):
        assert validate_role(role) is True

    def test_invalid_role(self):
        assert validate_role("superadmin") is False


class TestUsernameValidation:
    def test_valid_name(self):
        assert validate_username("Alice Park") is True

    def test_too_short(self):
        assert validate_username("A") is False

    def test_empty(self):
        assert validate_username("") is False
''')

    # --- pyproject.toml ---
    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[project]
name = "api-service"
version = "0.4.1"
description = "Internal API service for user management"
requires-python = ">=3.10"

[tool.pytest.ini_options]
testpaths = ["tests"]
''')

    # --- README.md ---
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# API Service

Internal user management API service built with Python.

## Setup

```bash
pip install -e .
```

## Running Tests

```bash
pytest tests/ -v
```
''')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'.vscode/settings.json exists: {os.path.exists(os.path.join(PROJECT_DIR, ".vscode", "settings.json"))}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
