"""
Initial Setup: Cherry-pick commit from feature/utils branch onto hotfix/logging branch
Task ID: vscode_git_028
Domain: vs_code

Creates a git repository at /home/user/project with:
- A 'main' branch with base commits
- A 'feature/utils' branch containing a commit that adds utils/logger.py
- A 'hotfix/logging' branch (currently checked out) that does NOT yet have logger.py
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None, check=True):
    """Run a shell command and return its output."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f'STDERR: {result.stderr}')
        print(f'STDOUT: {result.stdout}')
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def setup_git_identity(cwd):
    """Configure local git identity for the repo."""
    git_env = os.environ.copy()
    run_cmd(['git', 'config', 'user.email', 'dev@example.com'], cwd=cwd)
    run_cmd(['git', 'config', 'user.name', 'Dev User'], cwd=cwd)
    return git_env


def create_initial():
    # Remove existing project dir if present (idempotent)
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    run_cmd(['git', 'init'], cwd=PROJECT_DIR)
    setup_git_identity(PROJECT_DIR)

    # Set default branch name to main
    run_cmd(['git', 'checkout', '-b', 'main'], cwd=PROJECT_DIR)

    # Create initial project structure on main branch
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Create initial files
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Project

A sample application demonstrating logging utilities.

## Structure

- `src/` - Application source code
- `utils/` - Shared utility modules
- `tests/` - Test suite
""")

    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

import sys


def main():
    \"\"\"Run the application.\"\"\"
    print("Application starting...")
    # TODO: Add logging
    return 0


if __name__ == '__main__':
    sys.exit(main())
""")

    with open(f'{PROJECT_DIR}/src/config.py', 'w') as f:
        f.write("""\"\"\"Application configuration module.\"\"\"

import os


class Config:
    \"\"\"Base configuration.\"\"\"
    DEBUG = False
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/app.log'
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MAX_CONNECTIONS = 10
    TIMEOUT = 30
""")

    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_DIR}/tests/test_app.py', 'w') as f:
        f.write("""\"\"\"Tests for main application module.\"\"\"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import main


def test_main_returns_zero():
    \"\"\"Test that main() exits with code 0.\"\"\"
    assert main() == 0


if __name__ == '__main__':
    test_main_returns_zero()
    print("All tests passed.")
""")

    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""__pycache__/
*.pyc
*.pyo
.env
*.log
.DS_Store
venv/
.venv/
dist/
build/
*.egg-info/
""")

    # Commit initial structure to main
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = '2025-01-10T09:00:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-10T09:00:00'
    env['GIT_AUTHOR_NAME'] = 'Dev User'
    env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    env['GIT_COMMITTER_NAME'] = 'Dev User'
    env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'
    run_cmd(['git', 'commit', '-m', 'Initial project structure with app and config modules'],
            cwd=PROJECT_DIR, env=env)

    # Add second commit on main
    with open(f'{PROJECT_DIR}/src/database.py', 'w') as f:
        f.write("""\"\"\"Database connection and query utilities.\"\"\"

import sqlite3
import os


class Database:
    \"\"\"Simple database wrapper.\"\"\"

    def __init__(self, db_path: str = 'app.db'):
        self.db_path = db_path
        self._connection = None

    def connect(self):
        \"\"\"Open database connection.\"\"\"
        self._connection = sqlite3.connect(self.db_path)
        return self._connection

    def disconnect(self):
        \"\"\"Close database connection.\"\"\"
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute(self, query: str, params: tuple = ()):
        \"\"\"Execute a query and return results.\"\"\"
        conn = self._connection or self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
""")

    env['GIT_AUTHOR_DATE'] = '2025-01-12T11:30:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-12T11:30:00'
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    run_cmd(['git', 'commit', '-m', 'Add database connection utility module'],
            cwd=PROJECT_DIR, env=env)

    # Create feature/utils branch from main
    run_cmd(['git', 'checkout', '-b', 'feature/utils'], cwd=PROJECT_DIR)

    # Add utils directory with helper modules on feature/utils
    os.makedirs(f'{PROJECT_DIR}/utils', exist_ok=True)

    with open(f'{PROJECT_DIR}/utils/__init__.py', 'w') as f:
        f.write('"""Shared utility modules."""\n')

    with open(f'{PROJECT_DIR}/utils/helpers.py', 'w') as f:
        f.write("""\"\"\"General helper utilities.\"\"\"

import os
import json
import hashlib
from datetime import datetime


def load_json_file(path: str) -> dict:
    \"\"\"Load and parse a JSON file.\"\"\"
    with open(path, 'r') as f:
        return json.load(f)


def save_json_file(path: str, data: dict, indent: int = 2) -> None:
    \"\"\"Serialize data to JSON file.\"\"\"
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)


def hash_string(value: str, algorithm: str = 'sha256') -> str:
    \"\"\"Compute hash of a string value.\"\"\"
    h = hashlib.new(algorithm)
    h.update(value.encode('utf-8'))
    return h.hexdigest()


def timestamp_now(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    \"\"\"Return current timestamp as formatted string.\"\"\"
    return datetime.now().strftime(fmt)


def ensure_dir(path: str) -> None:
    \"\"\"Create directory if it does not exist.\"\"\"
    os.makedirs(path, exist_ok=True)
""")

    env['GIT_AUTHOR_DATE'] = '2025-01-15T10:00:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-15T10:00:00'
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    run_cmd(['git', 'commit', '-m', 'Add utils package with helper functions'],
            cwd=PROJECT_DIR, env=env)

    # THE KEY COMMIT: add logging utility in utils/logger.py
    with open(f'{PROJECT_DIR}/utils/logger.py', 'w') as f:
        f.write("""\"\"\"Logging utility module providing structured application logging.\"\"\"

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler


DEFAULT_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_DIR = '/var/log/app'
DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
DEFAULT_BACKUP_COUNT = 5


def get_logger(name: str, level: str = 'INFO') -> logging.Logger:
    \"\"\"
    Get or create a named logger with console output.

    Args:
        name: Logger name (typically __name__ of the calling module).
        level: Logging level string ('DEBUG', 'INFO', 'WARNING', 'ERROR').

    Returns:
        Configured Logger instance.
    \"\"\"
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def setup_file_logger(
    name: str,
    log_file: str,
    level: str = 'INFO',
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> logging.Logger:
    \"\"\"
    Configure a logger that writes to a rotating log file.

    Args:
        name: Logger name.
        log_file: Absolute path to the log file.
        level: Logging level string.
        max_bytes: Maximum size per log file before rotation.
        backup_count: Number of rotated backup files to keep.

    Returns:
        Configured Logger instance with file handler.
    \"\"\"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT))
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def log_exception(logger: logging.Logger, exc: Exception, message: str = '') -> None:
    \"\"\"Log an exception with optional context message.\"\"\"
    prefix = f'{message}: ' if message else ''
    logger.error(f'{prefix}{type(exc).__name__}: {exc}', exc_info=True)
""")

    env['GIT_AUTHOR_DATE'] = '2025-01-16T14:20:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-16T14:20:00'
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    run_cmd(['git', 'commit', '-m', 'Add logging utility with rotating file handler support'],
            cwd=PROJECT_DIR, env=env)

    # Get the hash of the logger commit
    result = run_cmd(['git', 'rev-parse', 'HEAD'], cwd=PROJECT_DIR)
    logger_commit_hash = result.stdout.strip()
    short_hash = logger_commit_hash[:7]
    print(f'Logger commit full hash: {logger_commit_hash}')
    print(f'Logger commit short hash: {short_hash}')

    # Add another commit on feature/utils (to ensure cherry-pick is selective)
    with open(f'{PROJECT_DIR}/utils/validators.py', 'w') as f:
        f.write("""\"\"\"Input validation utilities.\"\"\"

import re
from typing import Any


EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
URL_PATTERN = re.compile(
    r'^https?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+[A-Z]{2,6}\\.?|'
    r'localhost|'
    r'\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})'
    r'(?::\\d+)?'
    r'(?:/?|[/?]\\S+)$', re.IGNORECASE
)


def is_valid_email(email: str) -> bool:
    \"\"\"Check if the given string is a valid email address.\"\"\"
    return bool(EMAIL_PATTERN.match(email))


def is_valid_url(url: str) -> bool:
    \"\"\"Check if the given string is a valid HTTP/HTTPS URL.\"\"\"
    return bool(URL_PATTERN.match(url))


def is_non_empty_string(value: Any) -> bool:
    \"\"\"Return True if value is a non-empty string.\"\"\"
    return isinstance(value, str) and len(value.strip()) > 0


def clamp(value: float, minimum: float, maximum: float) -> float:
    \"\"\"Clamp value to [minimum, maximum] range.\"\"\"
    return max(minimum, min(maximum, value))
""")

    env['GIT_AUTHOR_DATE'] = '2025-01-17T09:45:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-17T09:45:00'
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    run_cmd(['git', 'commit', '-m', 'Add input validation utilities'],
            cwd=PROJECT_DIR, env=env)

    # Create hotfix/logging branch from main (NOT from feature/utils)
    run_cmd(['git', 'checkout', 'main'], cwd=PROJECT_DIR)
    run_cmd(['git', 'checkout', '-b', 'hotfix/logging'], cwd=PROJECT_DIR)

    # Add a hotfix commit on hotfix/logging (pre-existing work)
    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

import sys


def main():
    \"\"\"Run the application.\"\"\"
    # Hotfix: add basic startup message to diagnose crash-on-start
    print("Application starting...", flush=True)
    print("Initializing components...", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
""")

    env['GIT_AUTHOR_DATE'] = '2025-01-18T08:00:00'
    env['GIT_COMMITTER_DATE'] = '2025-01-18T08:00:00'
    run_cmd(['git', 'add', '-A'], cwd=PROJECT_DIR)
    run_cmd(['git', 'commit', '-m', 'hotfix: improve startup output for crash diagnosis'],
            cwd=PROJECT_DIR, env=env)

    # Save the logger commit hash for reference (reward-gen can use this)
    ref_file = f'{WORKDIR}/project/.git/refs/cherry_pick_target'
    with open(ref_file, 'w') as f:
        f.write(logger_commit_hash + '\n')
    print(f'Saved cherry-pick target hash to {ref_file}')

    # Verify final state: hotfix/logging is checked out, utils/logger.py does NOT exist
    result = run_cmd(['git', 'status'], cwd=PROJECT_DIR)
    print(result.stdout)

    result = run_cmd(['ls', f'{PROJECT_DIR}'], cwd=PROJECT_DIR)
    print('Project root files:', result.stdout)

    # Confirm utils/logger.py is absent on hotfix/logging
    logger_path = f'{PROJECT_DIR}/utils/logger.py'
    if os.path.exists(logger_path):
        print('WARNING: utils/logger.py should NOT exist on hotfix/logging branch!')
    else:
        print('CONFIRMED: utils/logger.py does not exist on hotfix/logging (correct initial state)')

    print(f'\nInitial git repository created: {PROJECT_DIR}')
    print(f'Current branch: hotfix/logging')
    print(f'feature/utils commit to cherry-pick: {short_hash} ({logger_commit_hash})')
    print('Task: cherry-pick the logging utility commit onto hotfix/logging')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
