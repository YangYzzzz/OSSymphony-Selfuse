"""
Initial Setup: Database schema management workflow in ~/project
Task ID: vscode_wf_064
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import sqlite3
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_064'
PROJECT_DIR = f'{WORKDIR}/project'

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
    # Ensure project directory exists
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create empty SQLite database
    db_path = f'{PROJECT_DIR}/database.db'
    conn = sqlite3.connect(db_path)
    conn.close()
    print(f'Created empty database: {db_path}')

    # Create main.py - a simple Python app that uses SQLite
    main_py = f'{PROJECT_DIR}/main.py'
    with open(main_py, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Simple blog application using SQLite database.
Manages users and their posts.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def list_users(conn):
    """List all registered users."""
    cursor = conn.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
    return [dict(row) for row in cursor.fetchall()]


def create_user(conn, username, email):
    """Register a new user."""
    conn.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email),
    )
    conn.commit()
    print(f"User '{username}' created successfully.")


def list_posts(conn, user_id=None):
    """List posts, optionally filtered by user."""
    if user_id:
        cursor = conn.execute(
            "SELECT p.id, p.title, u.username, p.created_at "
            "FROM posts p JOIN users u ON p.user_id = u.id "
            "WHERE p.user_id = ? ORDER BY p.created_at DESC",
            (user_id,),
        )
    else:
        cursor = conn.execute(
            "SELECT p.id, p.title, u.username, p.created_at "
            "FROM posts p JOIN users u ON p.user_id = u.id "
            "ORDER BY p.created_at DESC"
        )
    return [dict(row) for row in cursor.fetchall()]


def create_post(conn, user_id, title, body):
    """Create a new blog post."""
    conn.execute(
        "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)",
        (user_id, title, body),
    )
    conn.commit()
    print(f"Post '{title}' created successfully.")


if __name__ == "__main__":
    conn = get_connection()
    print("Blog Application - Database CLI")
    print("================================")
    print("Database:", DB_PATH)
    print()
    try:
        users = list_users(conn)
        print(f"Users: {len(users)}")
        posts = list_posts(conn)
        print(f"Posts: {len(posts)}")
    except sqlite3.OperationalError as e:
        print(f"Database not initialized: {e}")
        print("Please run migrations first.")
    finally:
        conn.close()
''')
    print(f'Created main.py: {main_py}')

    # Create requirements.txt
    req_path = f'{PROJECT_DIR}/requirements.txt'
    with open(req_path, 'w') as f:
        f.write('''# Blog Application Dependencies
# Python 3.8+

# SQLite3 is included in Python stdlib
# No additional packages required for core functionality

# Development dependencies
pytest>=7.4.0
black>=23.7.0
flake8>=6.1.0
''')
    print(f'Created requirements.txt: {req_path}')

    # Create a README
    readme_path = f'{PROJECT_DIR}/README.md'
    with open(readme_path, 'w') as f:
        f.write('''# Blog Application

A simple blog platform built with Python and SQLite.

## Project Structure

```
project/
  main.py          - Application entry point
  database.db      - SQLite database
  requirements.txt - Python dependencies
```

## Setup

1. Initialize the database by running migrations
2. Seed test data (optional)
3. Run the application: `python main.py`

## TODO

- [ ] Set up database migrations
- [ ] Add SQL tooling and linting
- [ ] Create seed data for testing
''')
    print(f'Created README.md: {readme_path}')

    # Create a simple .gitignore
    gitignore_path = f'{PROJECT_DIR}/.gitignore'
    with open(gitignore_path, 'w') as f:
        f.write('''__pycache__/
*.pyc
.env
*.db-journal
.vscode/
''')
    print(f'Created .gitignore: {gitignore_path}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
