"""
Initial Setup: Undo the last commit (soft reset), modify the commit message,
               add an additional file, then recommit.
Task ID: vscode_git_049
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_049'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, capture=False):
    """Run a shell command on the VM."""
    env = os.environ.copy()
    env['HOME'] = WORKDIR
    env['GIT_AUTHOR_NAME'] = 'Alice Dev'
    env['GIT_AUTHOR_EMAIL'] = 'alice@example.com'
    env['GIT_COMMITTER_NAME'] = 'Alice Dev'
    env['GIT_COMMITTER_EMAIL'] = 'alice@example.com'
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        env=env,
        capture_output=capture,
        text=True,
    )
    if check and result.returncode != 0:
        print(f'ERROR running: {cmd}')
        if capture:
            print(result.stderr)
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


def create_initial():
    # Remove any existing project directory to ensure clean state
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    run('git init', cwd=PROJECT_DIR)
    run('git config user.email "alice@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Alice Dev"', cwd=PROJECT_DIR)

    # --- Initial commit: project scaffold ---
    # Create main application files
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(
            '#!/usr/bin/env python3\n'
            '"""Main entry point for the application."""\n\n'
            'from api import get_users, create_user\n\n\n'
            'def main():\n'
            '    users = get_users()\n'
            '    print(f"Found {len(users)} users")\n'
            '    new_user = create_user("Jane Smith", "jane@example.com")\n'
            '    print(f"Created user: {new_user}")\n\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )

    with open(f'{PROJECT_DIR}/config.py', 'w') as f:
        f.write(
            '"""Application configuration settings."""\n\n'
            'DATABASE_URL = "postgresql://localhost:5432/myapp"\n'
            'API_VERSION = "v1"\n'
            'MAX_CONNECTIONS = 10\n'
            'TIMEOUT_SECONDS = 30\n'
            'DEBUG = False\n'
        )

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(
            'requests==2.28.2\n'
            'flask==2.3.0\n'
            'sqlalchemy==2.0.0\n'
            'pydantic==2.0.0\n'
        )

    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(
            '# MyApp Project\n\n'
            'A web application for managing users and resources.\n\n'
            '## Setup\n\n'
            '```bash\n'
            'pip install -r requirements.txt\n'
            'python main.py\n'
            '```\n\n'
            '## Features\n\n'
            '- User management\n'
            '- Resource tracking\n'
            '- RESTful API\n'
        )

    run('git add .', cwd=PROJECT_DIR)
    run('git commit -m "Initial project setup"', cwd=PROJECT_DIR)

    # --- Second commit: add api.py (the "Update API" commit, WITHOUT api_docs.md) ---
    with open(f'{PROJECT_DIR}/api.py', 'w') as f:
        f.write(
            '"""REST API module for user and resource management.\n\n'
            'Provides endpoints for CRUD operations on users.\n'
            '"""\n\n'
            'import json\n'
            'import datetime\n'
            'from typing import List, Dict, Optional\n\n\n'
            'BASE_URL = "https://api.example.com/v2"\n'
            'API_KEY = "sk_live_abc123xyz789"\n\n\n'
            'def get_users(limit: int = 50, offset: int = 0) -> List[Dict]:\n'
            '    """Retrieve paginated list of users.\n\n'
            '    Args:\n'
            '        limit: Maximum number of users to return (default 50).\n'
            '        offset: Number of users to skip (default 0).\n\n'
            '    Returns:\n'
            '        List of user dicts with id, name, email, created_at fields.\n'
            '    """\n'
            '    # Simulated response\n'
            '    users = [\n'
            '        {"id": 1, "name": "Sarah Chen", "email": "sarah.chen@example.com",\n'
            '         "created_at": "2024-01-15T10:30:00Z", "role": "admin"},\n'
            '        {"id": 2, "name": "Marcus Johnson", "email": "m.johnson@example.com",\n'
            '         "created_at": "2024-02-20T14:45:00Z", "role": "user"},\n'
            '        {"id": 3, "name": "Priya Patel", "email": "priya.patel@example.com",\n'
            '         "created_at": "2024-03-05T09:15:00Z", "role": "user"},\n'
            '        {"id": 4, "name": "Daniel Torres", "email": "d.torres@example.com",\n'
            '         "created_at": "2024-03-18T11:00:00Z", "role": "moderator"},\n'
            '    ]\n'
            '    return users[offset:offset + limit]\n\n\n'
            'def create_user(name: str, email: str, role: str = "user") -> Dict:\n'
            '    """Create a new user account.\n\n'
            '    Args:\n'
            '        name: Full name of the user.\n'
            '        email: Email address (must be unique).\n'
            '        role: User role (default "user").\n\n'
            '    Returns:\n'
            '        Created user dict with assigned id.\n'
            '    """\n'
            '    new_id = 1000 + hash(email) % 9000\n'
            '    return {\n'
            '        "id": new_id,\n'
            '        "name": name,\n'
            '        "email": email,\n'
            '        "role": role,\n'
            '        "created_at": datetime.datetime.utcnow().isoformat() + "Z",\n'
            '    }\n\n\n'
            'def delete_user(user_id: int) -> bool:\n'
            '    """Delete a user by ID.\n\n'
            '    Args:\n'
            '        user_id: The unique identifier of the user to delete.\n\n'
            '    Returns:\n'
            '        True if deletion succeeded, False otherwise.\n'
            '    """\n'
            '    # In production, this would call the DELETE endpoint\n'
            '    return user_id > 0\n\n\n'
            'def update_user(user_id: int, updates: Dict) -> Optional[Dict]:\n'
            '    """Update user attributes.\n\n'
            '    Args:\n'
            '        user_id: The unique identifier of the user.\n'
            '        updates: Dict of fields to update.\n\n'
            '    Returns:\n'
            '        Updated user dict, or None if user not found.\n'
            '    """\n'
            '    user = next((u for u in get_users() if u["id"] == user_id), None)\n'
            '    if user:\n'
            '        user.update(updates)\n'
            '    return user\n'
        )

    # CRITICAL: api_docs.md exists but is NOT staged/committed in this commit
    # It should appear as an untracked file, needing to be added to the commit
    with open(f'{PROJECT_DIR}/api_docs.md', 'w') as f:
        f.write(
            '# API Documentation\n\n'
            '## Overview\n\n'
            'This document describes the REST API endpoints for the MyApp project.\n\n'
            '## Base URL\n\n'
            '```\n'
            'https://api.example.com/v2\n'
            '```\n\n'
            '## Authentication\n\n'
            'All requests require an API key in the `Authorization` header:\n\n'
            '```\n'
            'Authorization: Bearer sk_live_abc123xyz789\n'
            '```\n\n'
            '## Endpoints\n\n'
            '### GET /users\n\n'
            'Retrieve a paginated list of users.\n\n'
            '**Parameters:**\n'
            '- `limit` (int, optional): Maximum results to return. Default: 50.\n'
            '- `offset` (int, optional): Number of results to skip. Default: 0.\n\n'
            '**Response:**\n'
            '```json\n'
            '[\n'
            '  {\n'
            '    "id": 1,\n'
            '    "name": "Sarah Chen",\n'
            '    "email": "sarah.chen@example.com",\n'
            '    "role": "admin",\n'
            '    "created_at": "2024-01-15T10:30:00Z"\n'
            '  }\n'
            ']\n'
            '```\n\n'
            '### POST /users\n\n'
            'Create a new user account.\n\n'
            '**Request body:**\n'
            '```json\n'
            '{\n'
            '  "name": "John Doe",\n'
            '  "email": "john.doe@example.com",\n'
            '  "role": "user"\n'
            '}\n'
            '```\n\n'
            '### DELETE /users/{id}\n\n'
            'Delete a user by their unique identifier.\n\n'
            '### PATCH /users/{id}\n\n'
            'Update one or more user attributes.\n\n'
            '## Error Codes\n\n'
            '| Code | Meaning |\n'
            '|------|---------|\n'
            '| 400  | Bad Request — invalid parameters |\n'
            '| 401  | Unauthorized — missing or invalid API key |\n'
            '| 404  | Not Found — user does not exist |\n'
            '| 500  | Internal Server Error |\n'
        )

    # Commit only api.py (NOT api_docs.md) — this is the "Update API" commit
    run('git add api.py', cwd=PROJECT_DIR)
    run('git commit -m "Update API"', cwd=PROJECT_DIR)

    # Verify state: api_docs.md should be untracked
    result = run('git status', cwd=PROJECT_DIR, capture=True)
    print('Git status after setup:')
    print(result.stdout)

    result = run('git log --oneline', cwd=PROJECT_DIR, capture=True)
    print('Git log:')
    print(result.stdout)

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
