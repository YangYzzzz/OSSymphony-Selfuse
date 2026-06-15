"""
Initial Setup: Code review improvements for Python API endpoints
Task ID: vscode_gf6_029
Domain: vscode

Creates ~/projects/code-review-python with src/api/endpoints.py containing
6 functions with inline SQL, bare except clauses, no type hints, no docstrings,
and duplicated manual pagination logic.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_029'
PROJECT_DIR = f'{WORKDIR}/projects/code-review-python'

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
    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/src/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/db', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)

    # Create __init__.py files
    for d in ['src', 'src/api', 'src/db', 'src/utils']:
        init_path = f'{PROJECT_DIR}/{d}/__init__.py'
        with open(init_path, 'w') as f:
            f.write('')

    # Create the main endpoints.py with intentional code review issues
    endpoints_content = '''import sqlite3
import json
from typing import Optional

# Database connection helper
def get_db():
    conn = sqlite3.connect("/home/user/projects/code-review-python/data/app.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_users(page, per_page):
    db = get_db()
    try:
        # Manual pagination
        skip = (page - 1) * per_page
        limit = per_page
        cursor = db.execute(
            "SELECT id, username, email, full_name, department, created_at FROM users ORDER BY id LIMIT ? OFFSET ?",
            (limit, skip)
        )
        rows = cursor.fetchall()
        count_cursor = db.execute("SELECT COUNT(*) as total FROM users")
        total = count_cursor.fetchone()["total"]
        total_pages = (total + per_page - 1) // per_page
        return {
            "users": [dict(r) for r in rows],
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }
    except:
        return {"error": "Failed to fetch users"}
    finally:
        db.close()


def get_user(user_id):
    db = get_db()
    try:
        cursor = db.execute(
            "SELECT id, username, email, full_name, department, created_at, last_login FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return {"error": "User not found"}
        return dict(row)
    except:
        return {"error": "Failed to fetch user"}
    finally:
        db.close()


def create_user(data):
    db = get_db()
    try:
        if not data.get("username") or not data.get("email"):
            raise ValueError("Username and email are required")
        cursor = db.execute(
            "INSERT INTO users (username, email, full_name, department) VALUES (?, ?, ?, ?)",
            (data["username"], data["email"], data.get("full_name", ""), data.get("department", ""))
        )
        db.commit()
        new_id = cursor.lastrowid
        return {"id": new_id, "message": "User created successfully"}
    except:
        db.rollback()
        return {"error": "Failed to create user"}
    finally:
        db.close()


def update_user(user_id, data):
    db = get_db()
    try:
        fields = []
        values = []
        for key in ["username", "email", "full_name", "department"]:
            if key in data:
                fields.append(f"{key} = ?")
                values.append(data[key])
        if not fields:
            raise ValueError("No fields to update")
        values.append(user_id)
        query = "UPDATE users SET " + ", ".join(fields) + " WHERE id = ?"
        db.execute(query, values)
        db.commit()
        return {"message": "User updated successfully"}
    except:
        db.rollback()
        return {"error": "Failed to update user"}
    finally:
        db.close()


def delete_user(user_id):
    db = get_db()
    try:
        cursor = db.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        db.commit()
        if cursor.rowcount == 0:
            return {"error": "User not found"}
        return {"message": "User deleted successfully"}
    except:
        db.rollback()
        return {"error": "Failed to delete user"}
    finally:
        db.close()


def list_orders(page, per_page, user_id=None):
    db = get_db()
    try:
        # Manual pagination (duplicated logic)
        skip = (page - 1) * per_page
        limit = per_page
        if user_id:
            cursor = db.execute(
                "SELECT o.id, o.user_id, o.product_name, o.quantity, o.unit_price, o.total_price, o.status, o.created_at FROM orders o WHERE o.user_id = ? ORDER BY o.created_at DESC LIMIT ? OFFSET ?",
                (user_id, limit, skip)
            )
            count_cursor = db.execute(
                "SELECT COUNT(*) as total FROM orders WHERE user_id = ?",
                (user_id,)
            )
        else:
            cursor = db.execute(
                "SELECT o.id, o.user_id, o.product_name, o.quantity, o.unit_price, o.total_price, o.status, o.created_at FROM orders o ORDER BY o.created_at DESC LIMIT ? OFFSET ?",
                (limit, skip)
            )
            count_cursor = db.execute(
                "SELECT COUNT(*) as total FROM orders"
            )
        rows = cursor.fetchall()
        total = count_cursor.fetchone()["total"]
        total_pages = (total + per_page - 1) // per_page
        return {
            "orders": [dict(r) for r in rows],
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }
    except:
        return {"error": "Failed to fetch orders"}
    finally:
        db.close()
'''

    with open(f'{PROJECT_DIR}/src/api/endpoints.py', 'w') as f:
        f.write(endpoints_content)

    # Create a simple requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('flask>=2.3.0\nflask-cors>=4.0.0\npytest>=7.4.0\n')

    # Create a basic README for the project
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('# Code Review Python\n\nA REST API for user and order management.\n\n## Setup\n\n```bash\npip install -r requirements.txt\n```\n\n## Running\n\n```bash\npython -m src.api.endpoints\n```\n')

    # Create data directory with placeholder db note
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    with open(f'{PROJECT_DIR}/data/.gitkeep', 'w') as f:
        f.write('')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Endpoints file: {PROJECT_DIR}/src/api/endpoints.py')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
