"""
Initial Setup: Git worktree workflow with Python web application
Task ID: vscode_gf6_017
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_017'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'git-worktree-workflow')


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


def run(cmd, cwd=None):
    """Run a shell command, raising on failure."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout.strip()


def create_initial():
    # ---- Create project directory ----
    os.makedirs(os.path.join(REPO_DIR, 'auth'), exist_ok=True)
    os.makedirs(os.path.join(REPO_DIR, 'dashboard'), exist_ok=True)

    # ---- auth/__init__.py ----
    with open(os.path.join(REPO_DIR, 'auth', '__init__.py'), 'w') as f:
        f.write('"""Authentication module for the web application."""\n')

    # ---- auth/tokens.py (with the bug: time.time() instead of time.time_ns()) ----
    with open(os.path.join(REPO_DIR, 'auth', 'tokens.py'), 'w') as f:
        f.write('''\
"""Token generation and validation utilities."""

import hashlib
import os
import time


def generate_token(user_id: str, scope: str = "default") -> str:
    """Generate a unique authentication token for the given user.

    Args:
        user_id: The user's unique identifier.
        scope: The token scope (default, admin, readonly).

    Returns:
        A hex-encoded token string.
    """
    # TODO: use ns precision
    timestamp = str(time.time())
    random_bytes = os.urandom(16).hex()
    raw = f"{user_id}:{scope}:{timestamp}:{random_bytes}"
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_token(token: str) -> bool:
    """Basic token format validation."""
    if not token or len(token) != 64:
        return False
    try:
        int(token, 16)
        return True
    except ValueError:
        return False


def revoke_token(token: str, revocation_list: set) -> None:
    """Add a token to the revocation list."""
    if validate_token(token):
        revocation_list.add(token)
''')

    # ---- dashboard/__init__.py (empty package) ----
    with open(os.path.join(REPO_DIR, 'dashboard', '__init__.py'), 'w') as f:
        f.write('"""Dashboard module - views coming soon."""\n')

    # ---- app.py (main entry point) ----
    with open(os.path.join(REPO_DIR, 'app.py'), 'w') as f:
        f.write('''\
"""Flask web application entry point."""

from flask import Flask, jsonify

from auth.tokens import generate_token, validate_token

app = Flask(__name__)


@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "version": "1.2.0"})


@app.route("/api/token/<user_id>")
def get_token(user_id):
    token = generate_token(user_id)
    return jsonify({"token": token, "user_id": user_id})


@app.route("/api/validate/<token>")
def check_token(token):
    valid = validate_token(token)
    return jsonify({"token": token, "valid": valid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
''')

    # ---- requirements.txt ----
    with open(os.path.join(REPO_DIR, 'requirements.txt'), 'w') as f:
        f.write('''\
flask==3.0.2
gunicorn==21.2.0
pytest==8.0.1
requests==2.31.0
''')

    # ---- .gitignore ----
    with open(os.path.join(REPO_DIR, '.gitignore'), 'w') as f:
        f.write('''\
__pycache__/
*.pyc
.env
*.egg-info/
dist/
build/
.venv/
''')

    # ---- README.md ----
    with open(os.path.join(REPO_DIR, 'README.md'), 'w') as f:
        f.write('''\
# Git Worktree Workflow Demo

A Python web application used to demonstrate git worktree workflows.

## Structure

- `app.py` — Flask application entry point
- `auth/` — Authentication and token management
- `dashboard/` — Dashboard views (in development)

## Running

```bash
pip install -r requirements.txt
python app.py
```
''')

    # ---- Initialize git repo ----
    run('git init', cwd=REPO_DIR)
    run('git config user.email "developer@example.com"', cwd=REPO_DIR)
    run('git config user.name "Developer"', cwd=REPO_DIR)
    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Initial commit: Flask web app with auth module"', cwd=REPO_DIR)

    # Verify clean state
    status = run('git status --porcelain', cwd=REPO_DIR)
    assert status == '', f"Dirty working tree: {status}"
    worktrees = run('git worktree list', cwd=REPO_DIR)
    print(f"Worktrees: {worktrees}")

    print(f'Initial repository created: {REPO_DIR}')

    # ---- GUI-ready startup: open VSCode with the repo ----
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
