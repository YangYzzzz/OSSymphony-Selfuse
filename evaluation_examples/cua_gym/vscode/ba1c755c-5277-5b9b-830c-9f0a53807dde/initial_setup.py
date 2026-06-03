"""
Initial Setup: Create a Python project with database migration script and .env file.
Task ID: vscode_py_066
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_066'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'

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
    os.makedirs(f'{PROJECT_DIR}/database', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- .env file ---
    env_content = """# Database configuration
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=dev-secret-key-abc123
DEBUG=true
LOG_LEVEL=INFO
"""
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # --- database/migrate.py ---
    migrate_content = '''#!/usr/bin/env python3
"""Database migration runner for the application."""

import os
import sys
from datetime import datetime


def get_database_url():
    """Get database URL from environment."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL environment variable is not set.")
        sys.exit(1)
    return db_url


def run_migration(mode="upgrade"):
    """Run database migration in the specified mode."""
    db_url = get_database_url()
    migration_mode = os.environ.get("MIGRATION_MODE", mode)

    print(f"[{datetime.now().isoformat()}] Starting migration...")
    print(f"  Database: {db_url}")
    print(f"  Mode: {migration_mode}")

    if migration_mode == "upgrade":
        print("  Applying pending migrations...")
        # Migration logic would go here
        apply_upgrade_migrations()
    elif migration_mode == "downgrade":
        print("  Rolling back last migration...")
        apply_downgrade_migrations()
    else:
        print(f"  Unknown migration mode: {migration_mode}")
        sys.exit(1)

    print("Migration completed successfully.")


def apply_upgrade_migrations():
    """Apply all pending upgrade migrations."""
    migrations = [
        "001_create_users_table",
        "002_add_email_index",
        "003_create_orders_table",
        "004_add_status_column",
        "005_create_inventory_table",
    ]
    for migration in migrations:
        print(f"    Applying: {migration}")


def apply_downgrade_migrations():
    """Roll back the most recent migration."""
    print("    Rolling back: 005_create_inventory_table")


if __name__ == "__main__":
    run_migration()
'''
    with open(f'{PROJECT_DIR}/database/migrate.py', 'w') as f:
        f.write(migrate_content)

    # --- database/__init__.py ---
    with open(f'{PROJECT_DIR}/database/__init__.py', 'w') as f:
        f.write('"""Database package for migration and connection management."""\n')

    # --- database/connection.py ---
    connection_content = '''"""Database connection manager."""

import os


class DatabaseConnection:
    """Manages PostgreSQL database connections."""

    def __init__(self):
        self.url = os.environ.get("DATABASE_URL", "")
        self.connected = False

    def connect(self):
        """Establish connection to the database."""
        if not self.url:
            raise ValueError("DATABASE_URL is not configured")
        self.connected = True
        return self

    def disconnect(self):
        """Close the database connection."""
        self.connected = False

    def execute(self, query, params=None):
        """Execute a SQL query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        return []
'''
    with open(f'{PROJECT_DIR}/database/connection.py', 'w') as f:
        f.write(connection_content)

    # --- models/__init__.py ---
    with open(f'{PROJECT_DIR}/models/__init__.py', 'w') as f:
        f.write('"""Data models package."""\n')

    # --- models/user.py ---
    user_model_content = '''"""User model definition."""


class User:
    """Represents an application user."""

    def __init__(self, user_id, name, email, role="member"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.is_active = True

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name!r}, role={self.role})"

    def deactivate(self):
        """Mark user as inactive."""
        self.is_active = False

    def promote(self, new_role):
        """Change user role."""
        valid_roles = ["member", "admin", "moderator"]
        if new_role not in valid_roles:
            raise ValueError(f"Invalid role: {new_role}")
        self.role = new_role
'''
    with open(f'{PROJECT_DIR}/models/user.py', 'w') as f:
        f.write(user_model_content)

    # --- main.py ---
    main_content = '''#!/usr/bin/env python3
"""Main application entry point."""

from database.connection import DatabaseConnection
from models.user import User


def main():
    """Initialize and run the application."""
    db = DatabaseConnection()
    db.connect()

    print("Application started successfully.")
    print(f"Database: {db.url}")

    # Example usage
    admin = User(1, "Sarah Chen", "sarah@example.com", role="admin")
    print(f"Admin user: {admin}")

    db.disconnect()


if __name__ == "__main__":
    main()
'''
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_content)

    # --- requirements.txt ---
    requirements_content = """psycopg2-binary==2.9.9
python-dotenv==1.0.1
alembic==1.13.1
sqlalchemy==2.0.25
"""
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # --- tests/__init__.py ---
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_migrate.py ---
    test_content = '''"""Tests for database migration runner."""

import os
import unittest


class TestMigration(unittest.TestCase):
    """Test migration functionality."""

    def test_database_url_required(self):
        """Verify DATABASE_URL must be set."""
        old_val = os.environ.pop("DATABASE_URL", None)
        try:
            from database.migrate import get_database_url
            with self.assertRaises(SystemExit):
                get_database_url()
        finally:
            if old_val:
                os.environ["DATABASE_URL"] = old_val

    def test_upgrade_mode(self):
        """Verify upgrade mode runs without error."""
        os.environ["DATABASE_URL"] = "postgresql://localhost/testdb"
        os.environ["MIGRATION_MODE"] = "upgrade"
        from database.migrate import run_migration
        # Should complete without raising
        run_migration()


if __name__ == "__main__":
    unittest.main()
'''
    with open(f'{PROJECT_DIR}/tests/test_migrate.py', 'w') as f:
        f.write(test_content)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  .env file: {PROJECT_DIR}/.env')
    print(f'  Migration script: {PROJECT_DIR}/database/migrate.py')
    print(f'  No .vscode/tasks.json (task requires creating it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
