"""
Initial Setup: Create a Git repository with multiple branches and commits for tag management.
Task ID: vscode_git_079
Domain: vs_code (git operations)

Creates:
  - /home/user/project: Git repo with branches 'main' (10 commits)
    and 'release/v2' (branched at commit 7, with 3 additional commits)
  - NO tags in initial state (agent must add them)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_079'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command."""
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        shlex.split(cmd),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        env=merged_env,
    )
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
    # Remove old project directory if it exists (idempotent)
    if os.path.exists(PROJECT_DIR):
        subprocess.run(['rm', '-rf', PROJECT_DIR], check=True)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Git config env for commits
    git_env = {
        'GIT_AUTHOR_NAME': 'Alice Dev',
        'GIT_AUTHOR_EMAIL': 'alice@example.com',
        'GIT_COMMITTER_NAME': 'Alice Dev',
        'GIT_COMMITTER_EMAIL': 'alice@example.com',
        'HOME': WORKDIR,
    }

    # Initialize repository
    run('git init -b main', cwd=PROJECT_DIR, env=git_env)
    run('git config user.email "alice@example.com"', cwd=PROJECT_DIR, env=git_env)
    run('git config user.name "Alice Dev"', cwd=PROJECT_DIR, env=git_env)

    # --- Create 10 commits on main ---
    # Commit 1
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('# Project\n\nA sample project for demonstrating Git workflows.\n')
    run('git add README.md', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Initial commit: add README"', cwd=PROJECT_DIR, env=git_env)

    # Commit 2
    with open(f'{PROJECT_DIR}/setup.py', 'w') as f:
        f.write(
            'from setuptools import setup\n\n'
            'setup(\n'
            '    name="myproject",\n'
            '    version="0.1.0",\n'
            '    packages=["myproject"],\n'
            ')\n'
        )
    run('git add setup.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add setup.py for packaging"', cwd=PROJECT_DIR, env=git_env)

    # Commit 3  <-- v1.0.0 annotated tag should go here
    os.makedirs(f'{PROJECT_DIR}/myproject', exist_ok=True)
    with open(f'{PROJECT_DIR}/myproject/__init__.py', 'w') as f:
        f.write('"""My project package."""\n\n__version__ = "1.0.0"\n')
    with open(f'{PROJECT_DIR}/myproject/core.py', 'w') as f:
        f.write(
            '"""Core module."""\n\n\n'
            'class Application:\n'
            '    """Main application class."""\n\n'
            '    def __init__(self, name: str):\n'
            '        self.name = name\n\n'
            '    def run(self):\n'
            '        print(f"Running {self.name}")\n'
        )
    run('git add myproject/', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Release 1.0.0: add core package structure"', cwd=PROJECT_DIR, env=git_env)

    # Commit 4
    with open(f'{PROJECT_DIR}/myproject/utils.py', 'w') as f:
        f.write(
            '"""Utility functions."""\n\n\n'
            'def format_output(data: dict) -> str:\n'
            '    """Format data as readable string."""\n'
            '    return "\\n".join(f"{k}: {v}" for k, v in data.items())\n\n\n'
            'def validate_input(value: str) -> bool:\n'
            '    """Validate that input is non-empty string."""\n'
            '    return isinstance(value, str) and len(value.strip()) > 0\n'
        )
    run('git add myproject/utils.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add utility functions module"', cwd=PROJECT_DIR, env=git_env)

    # Commit 5  <-- v1.0.0-dev lightweight tag should go here
    with open(f'{PROJECT_DIR}/myproject/config.py', 'w') as f:
        f.write(
            '"""Configuration module."""\n\n'
            'import os\n\n\n'
            'DEFAULT_CONFIG = {\n'
            '    "debug": False,\n'
            '    "log_level": "INFO",\n'
            '    "max_retries": 3,\n'
            '    "timeout": 30,\n'
            '}\n\n\n'
            'def load_config(path: str = None) -> dict:\n'
            '    """Load configuration from file or return defaults."""\n'
            '    if path and os.path.exists(path):\n'
            '        import json\n'
            '        with open(path) as f:\n'
            '            return {**DEFAULT_CONFIG, **json.load(f)}\n'
            '    return DEFAULT_CONFIG.copy()\n'
        )
    run('git add myproject/config.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add configuration module with defaults"', cwd=PROJECT_DIR, env=git_env)

    # Commit 6
    with open(f'{PROJECT_DIR}/myproject/exceptions.py', 'w') as f:
        f.write(
            '"""Custom exceptions."""\n\n\n'
            'class ProjectError(Exception):\n'
            '    """Base exception for project errors."""\n'
            '    pass\n\n\n'
            'class ConfigError(ProjectError):\n'
            '    """Raised when configuration is invalid."""\n'
            '    pass\n\n\n'
            'class ValidationError(ProjectError):\n'
            '    """Raised when input validation fails."""\n'
            '    pass\n'
        )
    run('git add myproject/exceptions.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add custom exception hierarchy"', cwd=PROJECT_DIR, env=git_env)

    # Commit 7 (this is where release/v2 branches off)
    with open(f'{PROJECT_DIR}/CHANGELOG.md', 'w') as f:
        f.write(
            '# Changelog\n\n'
            '## [1.0.0] - 2025-01-10\n'
            '### Added\n'
            '- Core application structure\n'
            '- Configuration management\n'
            '- Utility functions\n'
            '- Custom exception hierarchy\n\n'
            '## [Unreleased]\n'
            '### Planned\n'
            '- Database integration\n'
            '- REST API layer\n'
            '- Authentication module\n'
        )
    run('git add CHANGELOG.md', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add CHANGELOG with version history"', cwd=PROJECT_DIR, env=git_env)

    # Save commit 7 hash for branching
    result = run('git rev-parse HEAD', cwd=PROJECT_DIR, env=git_env)
    commit7_hash = result.stdout.strip()

    # Create release/v2 branch from commit 7
    run('git checkout -b release/v2', cwd=PROJECT_DIR, env=git_env)

    # Commit 8 on release/v2
    with open(f'{PROJECT_DIR}/myproject/api.py', 'w') as f:
        f.write(
            '"""REST API layer for v2."""\n\n'
            'from typing import Optional\n\n\n'
            'class APIClient:\n'
            '    """HTTP API client."""\n\n'
            '    def __init__(self, base_url: str, timeout: int = 30):\n'
            '        self.base_url = base_url\n'
            '        self.timeout = timeout\n\n'
            '    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:\n'
            '        """Perform GET request."""\n'
            '        url = f"{self.base_url}/{endpoint.lstrip(\'/\')}"\n'
            '        print(f"GET {url} params={params}")\n'
            '        return {"status": "ok", "data": []}\n\n'
            '    def post(self, endpoint: str, body: dict) -> dict:\n'
            '        """Perform POST request."""\n'
            '        url = f"{self.base_url}/{endpoint.lstrip(\'/\')}"\n'
            '        print(f"POST {url} body={body}")\n'
            '        return {"status": "created", "id": 1}\n'
        )
    run('git add myproject/api.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "v2: add REST API client"', cwd=PROJECT_DIR, env=git_env)

    # Commit 9 on release/v2
    with open(f'{PROJECT_DIR}/myproject/auth.py', 'w') as f:
        f.write(
            '"""Authentication module for v2."""\n\n'
            'import hashlib\n'
            'import secrets\n\n\n'
            'class Authenticator:\n'
            '    """Handles user authentication."""\n\n'
            '    def __init__(self):\n'
            '        self._tokens: dict = {}\n\n'
            '    def generate_token(self, user_id: str) -> str:\n'
            '        """Generate a secure token for a user."""\n'
            '        token = secrets.token_hex(32)\n'
            '        self._tokens[user_id] = hashlib.sha256(token.encode()).hexdigest()\n'
            '        return token\n\n'
            '    def verify_token(self, user_id: str, token: str) -> bool:\n'
            '        """Verify token for a given user."""\n'
            '        stored = self._tokens.get(user_id)\n'
            '        if not stored:\n'
            '            return False\n'
            '        return stored == hashlib.sha256(token.encode()).hexdigest()\n'
        )
    run('git add myproject/auth.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "v2: add authentication module"', cwd=PROJECT_DIR, env=git_env)

    # Commit 10 on release/v2 (HEAD)
    with open(f'{PROJECT_DIR}/myproject/database.py', 'w') as f:
        f.write(
            '"""Database integration for v2."""\n\n'
            'from typing import List, Optional\n\n\n'
            'class DatabaseConnection:\n'
            '    """Manages database connections."""\n\n'
            '    def __init__(self, dsn: str):\n'
            '        self.dsn = dsn\n'
            '        self._connected = False\n\n'
            '    def connect(self):\n'
            '        """Establish database connection."""\n'
            '        print(f"Connecting to {self.dsn}")\n'
            '        self._connected = True\n\n'
            '    def disconnect(self):\n'
            '        """Close database connection."""\n'
            '        self._connected = False\n\n'
            '    def execute(self, query: str, params: Optional[tuple] = None) -> List[dict]:\n'
            '        """Execute a query and return results."""\n'
            '        if not self._connected:\n'
            '            raise RuntimeError("Not connected to database")\n'
            '        print(f"QUERY: {query} PARAMS: {params}")\n'
            '        return []\n'
        )
    run('git add myproject/database.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "v2: add database integration module"', cwd=PROJECT_DIR, env=git_env)

    # Go back to main and continue with more commits
    run('git checkout main', cwd=PROJECT_DIR, env=git_env)

    # Commit 8 on main
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')
    with open(f'{PROJECT_DIR}/tests/test_core.py', 'w') as f:
        f.write(
            '"""Tests for core module."""\n\n'
            'import unittest\n'
            'from myproject.core import Application\n\n\n'
            'class TestApplication(unittest.TestCase):\n'
            '    def test_init(self):\n'
            '        app = Application("test")\n'
            '        self.assertEqual(app.name, "test")\n\n'
            '    def test_run(self):\n'
            '        app = Application("test")\n'
            '        app.run()  # Should not raise\n\n\n'
            'if __name__ == "__main__":\n'
            '    unittest.main()\n'
        )
    run('git add tests/', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add test suite for core module"', cwd=PROJECT_DIR, env=git_env)

    # Commit 9 on main
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('# Runtime dependencies\nrequests>=2.28.0\nclick>=8.1.0\n')
    with open(f'{PROJECT_DIR}/requirements-dev.txt', 'w') as f:
        f.write('# Development dependencies\npytest>=7.4.0\nblack>=23.0.0\nflake8>=6.0.0\nmypy>=1.4.0\n')
    run('git add requirements.txt requirements-dev.txt', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add requirements files for runtime and dev dependencies"', cwd=PROJECT_DIR, env=git_env)

    # Commit 10 on main
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(
            '# Python\n__pycache__/\n*.py[cod]\n*.egg-info/\ndist/\nbuild/\n.eggs/\n\n'
            '# Testing\n.pytest_cache/\n.coverage\nhtmlcov/\n\n'
            '# Virtual environments\n.venv/\nvenv/\nenv/\n\n'
            '# IDE\n.vscode/\n.idea/\n*.swp\n\n'
            '# Misc\n*.log\n.DS_Store\n'
        )
    run('git add .gitignore', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add comprehensive .gitignore"', cwd=PROJECT_DIR, env=git_env)

    # Verify commit counts
    main_count = run('git rev-list --count main', cwd=PROJECT_DIR, env=git_env).stdout.strip()
    rv2_count = run('git rev-list --count release/v2', cwd=PROJECT_DIR, env=git_env).stdout.strip()
    print(f'Branch main: {main_count} commits')
    print(f'Branch release/v2: {rv2_count} commits')

    # Verify no tags in initial state
    tags = run('git tag --list', cwd=PROJECT_DIR, env=git_env).stdout.strip()
    print(f'Tags in initial repo (should be empty): "{tags}"')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI startup: open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project directory on DISPLAY=:0')


create_initial()
