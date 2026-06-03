"""
Initial Setup: Create a containerized-app project with Dockerfile and existing tasks.json
Task ID: vscode_td_020
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_020'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'containerized-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASKS_JSON = os.path.join(VSCODE_DIR, 'tasks.json')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create Dockerfile
    dockerfile_content = """\
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
"""
    with open(os.path.join(PROJECT_DIR, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # Create requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("flask==3.0.2\ngunicorn==21.2.0\nredis==5.0.1\n")

    # Create app.py
    app_content = """\
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": os.getenv("APP_VERSION", "1.0.0")})

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Containerized App"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
"""
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_content)

    # Create .dockerignore
    with open(os.path.join(PROJECT_DIR, '.dockerignore'), 'w') as f:
        f.write("__pycache__\n*.pyc\n.vscode\n.git\n*.md\n")

    # Create tasks.json with ONE existing task (Run Tests)
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Tests",
                "type": "shell",
                "command": "python -m pytest tests/ -v",
                "group": "test",
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "problemMatcher": []
            }
        ]
    }
    with open(TASKS_JSON, 'w') as f:
        json.dump(tasks_config, f, indent=4)

    # Create a simple test file for the existing task
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write("")
    with open(os.path.join(tests_dir, 'test_app.py'), 'w') as f:
        f.write("""\
def test_health_endpoint():
    from app import app
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
""")

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'tasks.json created at: {TASKS_JSON}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
