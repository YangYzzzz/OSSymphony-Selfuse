"""
Initial Setup: VSCode with security-scanner project containing intentional security issues
Task ID: vscode_gf5_026
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_026'
PROJECT_DIR = f'{WORKDIR}/projects/security-scanner'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # --- src/__init__.py ---
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('"""Security Scanner Project - Source Package"""\n')

    # --- src/auth.py --- (intentional security issues: hardcoded passwords)
    with open(f'{SRC_DIR}/auth.py', 'w') as f:
        f.write('''\
"""Authentication module for the security scanner project."""

import hashlib
import os


# Hardcoded credentials (security issue: B105, B106)
ADMIN_PASSWORD = "SuperSecret123!"
DB_PASSWORD = "postgres_admin_2025"
API_KEY = "sk-proj-a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c5"


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user against hardcoded credentials."""
    valid_users = {
        "admin": ADMIN_PASSWORD,
        "developer": "DevPass456!",
        "readonly": "ReadOnly789#",
    }
    return valid_users.get(username) == password


def generate_token(user_id: int) -> str:
    """Generate an authentication token."""
    secret = "my_jwt_secret_key_do_not_share"
    payload = f"{user_id}:{secret}:{os.urandom(16).hex()}"
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_api_key(key: str) -> bool:
    """Verify the provided API key."""
    return key == API_KEY


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.master_key = "master-key-never-expose-this"

    def create_session(self, user_id: int) -> str:
        token = generate_token(user_id)
        self.sessions[token] = {
            "user_id": user_id,
            "created_at": None,
        }
        return token

    def validate_session(self, token: str) -> bool:
        return token in self.sessions
''')

    # --- src/utils.py --- (intentional security issues: eval, exec)
    with open(f'{SRC_DIR}/utils.py', 'w') as f:
        f.write('''\
"""Utility functions for data processing."""

import os
import pickle
import subprocess
import tempfile


def process_user_input(expression: str):
    """Process a mathematical expression from user input."""
    # Security issue: use of eval (B307)
    result = eval(expression)
    return result


def execute_dynamic_code(code_string: str):
    """Execute dynamically generated code."""
    # Security issue: use of exec (B102)
    exec(code_string)


def run_system_command(cmd: str):
    """Run a system command constructed from user input."""
    # Security issue: shell injection (B602)
    result = subprocess.call(cmd, shell=True)
    return result


def load_data(filepath: str):
    """Load serialized data from a file."""
    # Security issue: insecure deserialization (B301)
    with open(filepath, "rb") as f:
        return pickle.load(f)


def create_temp_file(content: str) -> str:
    """Create a temporary file with the given content."""
    # Security issue: insecure temp file (B108)
    tmp_path = "/tmp/scanner_data.txt"
    with open(tmp_path, "w") as f:
        f.write(content)
    return tmp_path


def format_report(template: str, **kwargs) -> str:
    """Format a report string with provided values."""
    return template.format(**kwargs)
''')

    # --- src/database.py --- (intentional security issues: SQL injection)
    with open(f'{SRC_DIR}/database.py', 'w') as f:
        f.write('''\
"""Database operations module."""

import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "scanner.db")


def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)


def find_user(username: str):
    """Find a user by username."""
    conn = get_connection()
    cursor = conn.cursor()
    # Security issue: SQL injection (B608)
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


def search_logs(keyword: str):
    """Search logs by keyword."""
    conn = get_connection()
    cursor = conn.cursor()
    # Security issue: SQL injection via format string (B608)
    query = f"SELECT * FROM logs WHERE message LIKE '%{keyword}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def delete_old_records(table: str, days: int):
    """Delete records older than specified days."""
    conn = get_connection()
    cursor = conn.cursor()
    # Security issue: SQL injection via string concatenation
    query = "DELETE FROM " + table + " WHERE created_at < datetime('now', '-" + str(days) + " days')"
    cursor.execute(query)
    conn.commit()
    conn.close()


def export_data(table_name: str, output_path: str):
    """Export table data to a file."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    with open(output_path, "w") as f:
        for row in rows:
            f.write(str(row) + "\\n")
    conn.close()
''')

    # --- src/config.py --- (intentional security issues: hardcoded secrets, weak crypto)
    with open(f'{SRC_DIR}/config.py', 'w') as f:
        f.write('''\
"""Application configuration module."""

import hashlib
import random


# Hardcoded configuration with secrets
APP_CONFIG = {
    "app_name": "Security Scanner",
    "version": "2.1.0",
    "debug": True,
    "database": {
        "host": "db.internal.company.com",
        "port": 5432,
        "name": "scanner_prod",
        "user": "admin",
        "password": "Pr0d_DB_Pass!2025",  # B105: hardcoded password
    },
    "redis": {
        "host": "redis.internal.company.com",
        "port": 6379,
        "password": "R3dis_Cache_Key!",
    },
    "smtp": {
        "server": "smtp.company.com",
        "port": 587,
        "username": "alerts@company.com",
        "password": "SmtpAlertPass123",
    },
}

AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"


def hash_password(password: str) -> str:
    """Hash a password using MD5."""
    # Security issue: weak hash (B303)
    return hashlib.md5(password.encode()).hexdigest()


def generate_session_id() -> str:
    """Generate a session ID."""
    # Security issue: insecure random (B311)
    return str(random.randint(100000, 999999))


def get_database_url() -> str:
    """Construct database URL from config."""
    db = APP_CONFIG["database"]
    return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
''')

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''\
# Security Scanner

Internal tool for automated security scanning of Python codebases.

## Project Structure

```
security-scanner/
├── src/
│   ├── __init__.py
│   ├── auth.py        # Authentication module
│   ├── config.py      # Application configuration
│   ├── database.py    # Database operations
│   └── utils.py       # Utility functions
├── README.md
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

The security team needs a scan script integrated into the VSCode workflow.
''')

    # --- requirements.txt ---
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('bandit>=1.7.0\n')

    # Install bandit
    subprocess.run(['pip3', 'install', 'bandit'], capture_output=True, text=True)

    # Remove any pre-existing scan.py or tasks.json (idempotent)
    scan_path = f'{SRC_DIR}/scan.py'
    tasks_path = f'{PROJECT_DIR}/.vscode/tasks.json'
    if os.path.exists(scan_path):
        os.remove(scan_path)
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: {os.listdir(SRC_DIR)}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
