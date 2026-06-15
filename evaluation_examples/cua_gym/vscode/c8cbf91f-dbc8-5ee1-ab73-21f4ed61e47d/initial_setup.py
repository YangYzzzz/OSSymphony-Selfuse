"""
Initial Setup: VSCode Git branching workflow - starting state
Task ID: vscode_git_056
Domain: vs_code

Creates /home/user/project as a Git repository with 3 commits on main branch.
No feature or release branches exist yet. The agent must create them.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_056'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


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
    # Remove and recreate project directory for idempotency
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Set up git config for commits
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # Initialize git repository
    run_cmd('git init', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)
    # Force the default branch name to 'main'
    run_cmd('git config init.defaultBranch main', cwd=PROJECT_DIR, env=git_env)

    # Commit 1: Initial project setup with README
    readme_content = """# MyApp Project

A Python web application with user management features.

## Overview

This project provides a backend service for handling user operations
including authentication, profile management, and session control.

## Requirements

- Python 3.8+
- Flask 2.0+
- SQLAlchemy 1.4+

## Getting Started

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
python main.py
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    requirements_content = """flask==2.3.0
sqlalchemy==2.0.0
pydantic==2.0.0
pytest==7.4.0
"""
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    run_cmd('git add README.md requirements.txt', cwd=PROJECT_DIR, env=git_env)
    run_cmd(['git', 'commit', '-m', 'Initial project setup with README and requirements'],
            cwd=PROJECT_DIR, env=git_env)

    # Commit 2: Add main application entry point
    main_content = """#!/usr/bin/env python3
\"\"\"
MyApp - Main Application Entry Point
\"\"\"

from flask import Flask, jsonify
from utils import get_version, setup_logging

app = Flask(__name__)
logger = setup_logging(__name__)


@app.route('/')
def index():
    \"\"\"Health check endpoint.\"\"\"
    return jsonify({
        'status': 'ok',
        'version': get_version(),
        'app': 'MyApp'
    })


@app.route('/health')
def health():
    \"\"\"Detailed health check.\"\"\"
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'cache': 'available'
    })


if __name__ == '__main__':
    logger.info('Starting MyApp server...')
    app.run(host='0.0.0.0', port=8080, debug=False)
"""
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_content)

    run_cmd('git add main.py', cwd=PROJECT_DIR, env=git_env)
    run_cmd(['git', 'commit', '-m', 'Add main application entry point with Flask routes'],
            cwd=PROJECT_DIR, env=git_env)

    # Commit 3: Add utility module
    utils_content = """\"\"\"
Utility functions for MyApp.
\"\"\"

import logging
import os


APP_VERSION = '1.0.0'


def get_version() -> str:
    \"\"\"Return current application version.\"\"\"
    return APP_VERSION


def setup_logging(name: str) -> logging.Logger:
    \"\"\"Configure and return a logger instance.\"\"\"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(name)


def validate_email(email: str) -> bool:
    \"\"\"Basic email format validation.\"\"\"
    return '@' in email and '.' in email.split('@')[-1]


def sanitize_username(username: str) -> str:
    \"\"\"Remove special characters from username, allow alphanumeric and underscore.\"\"\"
    return ''.join(c for c in username if c.isalnum() or c == '_')


def paginate(items: list, page: int = 1, per_page: int = 20) -> dict:
    \"\"\"Paginate a list of items.\"\"\"
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }
"""
    with open(f'{PROJECT_DIR}/utils.py', 'w') as f:
        f.write(utils_content)

    run_cmd('git add utils.py', cwd=PROJECT_DIR, env=git_env)
    run_cmd(['git', 'commit', '-m', 'Add utility module with logging, validation and pagination'],
            cwd=PROJECT_DIR, env=git_env)

    # Ensure branch is named 'main' (some git versions default to 'master')
    run_cmd('git branch -m master main', cwd=PROJECT_DIR, env=git_env)

    # Verify: main branch should have exactly 3 commits, no other branches
    rc, out, err = run_cmd('git log --oneline', cwd=PROJECT_DIR, env=git_env)
    print(f'Git log on main:\n{out}')

    rc, out, err = run_cmd('git branch', cwd=PROJECT_DIR, env=git_env)
    print(f'Branches: {out}')

    print(f'Initial project created: {PROJECT_DIR}')
    print('Branches: only main (no feature or release branches)')
    print('Files: README.md, requirements.txt, main.py, utils.py')
    print('NO auth.py, NO version.py (those will be created by the agent)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder on DISPLAY=:0')


create_initial()
