"""
Initial Setup: Set up a Flask project workspace for VSCode debug configuration task.
Task ID: vscode_lp_026
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_026'
PROJECT_DIR = f'{WORKDIR}/workspace'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create app.py - a realistic Flask application
    app_py_content = '''from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory storage for demo purposes
tasks = [
    {"id": 1, "title": "Review pull requests", "done": False},
    {"id": 2, "title": "Update documentation", "done": False},
    {"id": 3, "title": "Deploy staging environment", "done": True},
]

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Task Manager</title></head>
<body>
    <h1>Task Manager API</h1>
    <p>Endpoints:</p>
    <ul>
        <li>GET /api/tasks - List all tasks</li>
        <li>POST /api/tasks - Create a new task</li>
        <li>PUT /api/tasks/&lt;id&gt; - Update a task</li>
        <li>DELETE /api/tasks/&lt;id&gt; - Delete a task</li>
    </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    new_task = {
        "id": max(t["id"] for t in tasks) + 1 if tasks else 1,
        "title": data["title"],
        "done": False,
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"result": "deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # Create requirements.txt
    requirements_content = '''flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Create a simple README
    readme_content = '''# Task Manager API

A simple Flask-based REST API for managing tasks.

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

The server starts on http://localhost:5000
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Create a basic config.py
    config_content = '''import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
'''
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write(config_content)

    # Create a tests directory with a basic test file
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    test_content = '''import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task Manager" in response.data


def test_get_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert len(data["tasks"]) == 3


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={"title": "New test task"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "New test task"
    assert data["done"] is False
'''
    with open(os.path.join(tests_dir, 'test_app.py'), 'w') as f:
        f.write(test_content)

    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Ensure NO .vscode directory exists (task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial Flask project created at: {PROJECT_DIR}')
    print(f'  - app.py (main entry point)')
    print(f'  - requirements.txt')
    print(f'  - config.py')
    print(f'  - tests/test_app.py')
    print(f'  - No .vscode/ directory (task requires creating it)')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
