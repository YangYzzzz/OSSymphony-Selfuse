"""
Initial Setup: Manage multiple stashes - create three stashes from different working states
Task ID: vscode_git_062
Domain: vs_code (git)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_062'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return stdout+stderr."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        print(f'CMD FAILED: {cmd}')
        print(f'  STDOUT: {result.stdout}')
        print(f'  STDERR: {result.stderr}')
    return result


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
    # Set up git environment variables
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # Remove existing project dir if present (idempotency)
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    run_cmd('git init', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)

    # Create initial Python files with realistic content
    file_a_content = """\
# file_a.py - Authentication utilities
import hashlib
import hmac


def hash_password(password: str, salt: str) -> str:
    \"\"\"Hash a password using SHA-256 with a salt.\"\"\"
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return dk.hex()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    \"\"\"Verify a password against its hash.\"\"\"
    return hmac.compare_digest(hash_password(password, salt), hashed)


class AuthManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id: str, token: str):
        self.sessions[user_id] = token

    def validate_session(self, user_id: str, token: str) -> bool:
        return self.sessions.get(user_id) == token
"""

    file_b_content = """\
# file_b.py - Database connection utilities
import sqlite3
from contextlib import contextmanager


DB_PATH = '/home/user/project/data/app.db'


@contextmanager
def get_connection():
    \"\"\"Context manager for database connections.\"\"\"
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


def create_tables():
    \"\"\"Create database tables if they do not exist.\"\"\"
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
"""

    file_c_content = """\
# file_c.py - API request handlers
from typing import Optional, Dict, Any


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def validate_request(data: Dict[str, Any], required_fields: list) -> bool:
    \"\"\"Validate that required fields are present in request data.\"\"\"
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise APIError(f'Missing required fields: {missing}', status_code=422)
    return True


def paginate(items: list, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    \"\"\"Paginate a list of items.\"\"\"
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
    }
"""

    # Write initial files
    with open(f'{PROJECT_DIR}/file_a.py', 'w') as f:
        f.write(file_a_content)
    with open(f'{PROJECT_DIR}/file_b.py', 'w') as f:
        f.write(file_b_content)
    with open(f'{PROJECT_DIR}/file_c.py', 'w') as f:
        f.write(file_c_content)

    # Also create a README
    readme_content = """\
# Project

A Python web application with authentication, database, and API utilities.

## Structure

- `file_a.py` - Authentication utilities
- `file_b.py` - Database connection utilities
- `file_c.py` - API request handlers
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Initial commit
    run_cmd('git add .', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git commit -m "Initial commit: add project files"', cwd=PROJECT_DIR, env=git_env)
    print('Initial commit created.')

    # --- Create Stash 1: Modify file_a.py and stash as "WIP: file A" ---
    file_a_modified = file_a_content + """\

    def logout(self, user_id: str):
        \"\"\"Remove a session for a user.\"\"\"
        self.sessions.pop(user_id, None)
"""
    with open(f'{PROJECT_DIR}/file_a.py', 'w') as f:
        f.write(file_a_modified)
    run_cmd('git add file_a.py', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git stash push -m "WIP: file A"', cwd=PROJECT_DIR, env=git_env)
    print('Stash 1 created: WIP: file A')

    # --- Create Stash 2: Modify file_b.py and stash as "WIP: file B" ---
    file_b_modified = file_b_content + """\

def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    \"\"\"Fetch a user record by email address.\"\"\"
    with get_connection() as conn:
        return conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
"""
    with open(f'{PROJECT_DIR}/file_b.py', 'w') as f:
        f.write(file_b_modified)
    run_cmd('git add file_b.py', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git stash push -m "WIP: file B"', cwd=PROJECT_DIR, env=git_env)
    print('Stash 2 created: WIP: file B')

    # --- Create Stash 3: Modify file_c.py and stash as "WIP: file C" ---
    file_c_modified = file_c_content + """\

def format_response(data: Any, message: str = 'success') -> Dict[str, Any]:
    \"\"\"Format a standard API response envelope.\"\"\"
    return {
        'status': 'ok',
        'message': message,
        'data': data,
    }
"""
    with open(f'{PROJECT_DIR}/file_c.py', 'w') as f:
        f.write(file_c_modified)
    run_cmd('git add file_c.py', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git stash push -m "WIP: file C"', cwd=PROJECT_DIR, env=git_env)
    print('Stash 3 created: WIP: file C')

    # Verify stash list
    result = run_cmd('git stash list', cwd=PROJECT_DIR, env=git_env)
    print(f'Stash list:\n{result.stdout}')

    # Verify working tree is clean
    result = run_cmd('git status', cwd=PROJECT_DIR, env=git_env)
    print(f'Git status:\n{result.stdout}')

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project directory (DISPLAY=:0)')


create_initial()
