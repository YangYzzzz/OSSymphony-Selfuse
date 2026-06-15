"""
Initial Setup: Set up a git project with 10 commits on main, no tags.
Task ID: vscode_git_065
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_065'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command and return its output."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        env=env,
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
    # Remove existing project directory if it exists (idempotent)
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR)

    # Configure git identity for this repo
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'devuser@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'devuser@example.com'

    # Initialize git repository
    run('git init', cwd=PROJECT_DIR, env=git_env)
    run('git config user.email "devuser@example.com"', cwd=PROJECT_DIR, env=git_env)
    run('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)

    # Define 10 commits with realistic content
    commits = [
        ('Initial project scaffold', 'README.md',
         '# MyApp\n\nA modular web application for team collaboration.\n'),
        ('Add project configuration', 'config.json',
         '{\n  "appName": "MyApp",\n  "version": "0.1.0",\n  "debug": true\n}\n'),
        ('Add core authentication module', 'auth.py',
         'class AuthManager:\n    """Handles user authentication and sessions."""\n\n    def login(self, username, password):\n        pass\n\n    def logout(self, session_id):\n        pass\n'),
        ('Add database connection layer', 'db.py',
         'import sqlite3\n\nclass Database:\n    """SQLite database connection manager."""\n\n    def __init__(self, path):\n        self.path = path\n        self.conn = None\n\n    def connect(self):\n        self.conn = sqlite3.connect(self.path)\n'),
        ('Add user model and validation', 'models.py',
         'class User:\n    """User domain model."""\n\n    def __init__(self, id, username, email):\n        self.id = id\n        self.username = username\n        self.email = email\n\n    def is_valid(self):\n        return bool(self.username and self.email)\n'),
        ('Add REST API endpoints', 'api.py',
         'from flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n@app.route("/users", methods=["GET"])\ndef list_users():\n    return jsonify({"users": []})\n\n@app.route("/users/<int:uid>", methods=["GET"])\ndef get_user(uid):\n    return jsonify({"id": uid})\n'),
        ('Add unit tests for auth module', 'test_auth.py',
         'import unittest\nfrom auth import AuthManager\n\nclass TestAuth(unittest.TestCase):\n    def setUp(self):\n        self.mgr = AuthManager()\n\n    def test_login_returns_none_without_impl(self):\n        result = self.mgr.login("alice", "secret")\n        self.assertIsNone(result)\n\nif __name__ == "__main__":\n    unittest.main()\n'),
        ('Add logging and error handling', 'logger.py',
         'import logging\n\nlogging.basicConfig(\n    level=logging.INFO,\n    format="%(asctime)s %(levelname)s %(name)s %(message)s"\n)\n\ndef get_logger(name):\n    return logging.getLogger(name)\n'),
        ('Add deployment scripts', 'deploy.sh',
         '#!/usr/bin/env bash\nset -euo pipefail\n\necho "Deploying MyApp..."\npip install -r requirements.txt\npython manage.py migrate\npython manage.py collectstatic --noinput\ngunicorn myapp.wsgi:application --bind 0.0.0.0:8000\n'),
        ('Bump version to 2.0.0 and update changelog', 'CHANGELOG.md',
         '# Changelog\n\n## [2.0.0] - 2025-06-01\n### Added\n- Complete REST API\n- Authentication module\n- Database layer\n- Unit test coverage\n- Deployment automation\n\n## [1.1.0] - 2025-03-15\n### Added\n- Feature updates and stability improvements\n\n## [1.0.0] - 2025-01-10\n### Added\n- First stable release\n'),
    ]

    for commit_message, filename, content in commits:
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        run(f'git add {filename}', cwd=PROJECT_DIR, env=git_env)
        run(['git', 'commit', '-m', commit_message], cwd=PROJECT_DIR, env=git_env)

    # Verify we have exactly 10 commits and NO tags
    result = run('git log --oneline', cwd=PROJECT_DIR, env=git_env)
    commit_count = len(result.stdout.strip().splitlines())
    print(f'Created {commit_count} commits on main branch')

    tag_result = run('git tag -l', cwd=PROJECT_DIR, env=git_env)
    tag_count = len([t for t in tag_result.stdout.strip().splitlines() if t])
    print(f'Tags present: {tag_count} (should be 0)')

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
