"""
Initial Setup: Pull latest changes from remote 'origin' on current branch
Task ID: vscode_gs_012
Domain: vscode

Creates a git repo at ~/projects/team-repo/ with a local 'main' branch.
Sets up a bare remote repo at ~/projects/team-repo-remote.git that is
3 commits ahead of local main. Configures origin to point to the bare repo.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_012'
REPO_DIR = f'{WORKDIR}/projects/team-repo'
REMOTE_BARE = f'{WORKDIR}/projects/team-repo-remote.git'


def run(cmd, cwd=None):
    """Run a shell command, raising on failure."""
    result = subprocess.run(cmd, shell=True, cwd=cwd,
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


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
    import shutil

    # Clean up any previous state
    for p in [REPO_DIR, REMOTE_BARE]:
        if os.path.exists(p):
            shutil.rmtree(p)

    os.makedirs(REPO_DIR, exist_ok=True)

    # --- Step 1: Create the local repo with initial commits ---
    run('git init -b main', cwd=REPO_DIR)
    run('git config user.email "developer@teamcorp.com"', cwd=REPO_DIR)
    run('git config user.name "Alex Rivera"', cwd=REPO_DIR)

    # Create realistic project files and initial commits

    # Commit 1: Project scaffold
    readme_content = """# Team Dashboard API

A RESTful API service for the internal team dashboard.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

- `GET /api/health` - Health check
- `GET /api/users` - List team members
- `POST /api/tasks` - Create a new task

## License

MIT License - TeamCorp 2025
"""
    with open(os.path.join(REPO_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    app_content = """from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory store
users = [
    {"id": 1, "name": "Sarah Chen", "role": "Backend Engineer"},
    {"id": 2, "name": "Marcus Johnson", "role": "Frontend Engineer"},
    {"id": 3, "name": "Priya Patel", "role": "DevOps Engineer"},
]

tasks = []


@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/users')
def get_users():
    return jsonify(users)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "assignee": data.get("assignee", ""),
        "status": "open"
    }
    tasks.append(task)
    return jsonify(task), 201


if __name__ == '__main__':
    app.run(debug=True, port=8080)
"""
    with open(os.path.join(REPO_DIR, 'app.py'), 'w') as f:
        f.write(app_content)

    requirements = """flask==3.0.0
gunicorn==21.2.0
pytest==7.4.3
requests==2.31.0
"""
    with open(os.path.join(REPO_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Initial project scaffold with Flask API"', cwd=REPO_DIR)

    # Commit 2: Add config module
    os.makedirs(os.path.join(REPO_DIR, 'config'), exist_ok=True)
    config_content = """import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///test.db'
"""
    with open(os.path.join(REPO_DIR, 'config', '__init__.py'), 'w') as f:
        f.write(config_content)

    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Add configuration module with environment support"', cwd=REPO_DIR)

    # --- Step 2: Create a bare remote and push local to it ---
    run(f'git clone --bare {REPO_DIR} {REMOTE_BARE}')

    # Set origin to bare repo
    run(f'git remote add origin {REMOTE_BARE}', cwd=REPO_DIR)
    run('git push -u origin main', cwd=REPO_DIR)

    # --- Step 3: Add 3 commits to the bare remote (via a temp clone) ---
    tmp_clone = f'{WORKDIR}/projects/.tmp-clone'
    if os.path.exists(tmp_clone):
        shutil.rmtree(tmp_clone)
    run(f'git clone {REMOTE_BARE} {tmp_clone}')
    run('git config user.email "priya.patel@teamcorp.com"', cwd=tmp_clone)
    run('git config user.name "Priya Patel"', cwd=tmp_clone)

    # Remote commit 1: Add Dockerfile
    dockerfile = """FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
"""
    with open(os.path.join(tmp_clone, 'Dockerfile'), 'w') as f:
        f.write(dockerfile)

    dockerignore = """__pycache__
*.pyc
.env
.git
*.db
venv/
"""
    with open(os.path.join(tmp_clone, '.dockerignore'), 'w') as f:
        f.write(dockerignore)

    run('git add -A', cwd=tmp_clone)
    run('git commit -m "Add Dockerfile and .dockerignore for containerized deployment"', cwd=tmp_clone)

    # Remote commit 2: Add tests directory
    os.makedirs(os.path.join(tmp_clone, 'tests'), exist_ok=True)
    test_content = """import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    users = response.get_json()
    assert len(users) == 3
    assert users[0]['name'] == 'Sarah Chen'


def test_create_task(client):
    payload = {"title": "Fix login bug", "assignee": "Marcus Johnson"}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    task = response.get_json()
    assert task['title'] == 'Fix login bug'
    assert task['status'] == 'open'
"""
    with open(os.path.join(tmp_clone, 'tests', 'test_api.py'), 'w') as f:
        f.write(test_content)

    with open(os.path.join(tmp_clone, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    run('git add -A', cwd=tmp_clone)
    run('git commit -m "Add pytest test suite for API endpoints"', cwd=tmp_clone)

    # Remote commit 3: Add CI workflow
    os.makedirs(os.path.join(tmp_clone, '.github', 'workflows'), exist_ok=True)
    ci_content = """name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install flake8
        run: pip install flake8
      - name: Run linter
        run: flake8 . --max-line-length=120
"""
    with open(os.path.join(tmp_clone, '.github', 'workflows', 'ci.yml'), 'w') as f:
        f.write(ci_content)

    run('git add -A', cwd=tmp_clone)
    run('git commit -m "Add GitHub Actions CI pipeline for tests and linting"', cwd=tmp_clone)

    # Push all 3 commits to the bare remote
    run('git push origin main', cwd=tmp_clone)

    # Clean up temp clone
    shutil.rmtree(tmp_clone)

    # --- Step 4: Verify local is behind ---
    status = run('git log --oneline origin/main..HEAD', cwd=REPO_DIR)
    behind = run('git rev-list HEAD..origin/main --count', cwd=REPO_DIR)
    # Need to fetch first to know about remote changes
    run('git fetch origin', cwd=REPO_DIR)
    behind = run('git rev-list HEAD..origin/main --count', cwd=REPO_DIR)
    print(f'Local main is {behind} commits behind origin/main')

    # --- Step 5: Launch VSCode ---
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    print(f'Initial setup complete: {REPO_DIR}')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
