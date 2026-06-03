"""
Initial Setup: Configure Docker development workflow in ~/project
Task ID: vscode_wf_044
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/project'

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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create app.py - a realistic Flask application
    app_py_content = '''from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo
tasks = [
    {"id": 1, "title": "Set up development environment", "status": "done", "created": "2025-12-01"},
    {"id": 2, "title": "Design database schema", "status": "in_progress", "created": "2025-12-05"},
    {"id": 3, "title": "Implement user authentication", "status": "todo", "created": "2025-12-10"},
    {"id": 4, "title": "Build REST API endpoints", "status": "todo", "created": "2025-12-12"},
    {"id": 5, "title": "Write integration tests", "status": "todo", "created": "2025-12-15"},
]

@app.route("/")
def index():
    return jsonify({"message": "Task Manager API v1.0", "endpoints": ["/tasks", "/tasks/<id>", "/health"]})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    status_filter = request.args.get("status")
    if status_filter:
        filtered = [t for t in tasks if t["status"] == status_filter]
        return jsonify(filtered)
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    new_task = {
        "id": max(t["id"] for t in tasks) + 1 if tasks else 1,
        "title": data["title"],
        "status": data.get("status", "todo"),
        "created": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # Create requirements.txt
    requirements_content = '''flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: app.py, requirements.txt')

    # Ensure no Docker extension is installed (remove if present)
    subprocess.run(
        ['code', '--uninstall-extension', 'ms-azuretools.vscode-docker'],
        capture_output=True, text=True
    )

    # Ensure no Dockerfile, docker-compose.yml, .vscode/tasks.json, .vscode/launch.json exist
    for f in ['Dockerfile', 'docker-compose.yml']:
        path = os.path.join(PROJECT_DIR, f)
        if os.path.exists(path):
            os.remove(path)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    for f in ['tasks.json', 'launch.json']:
        path = os.path.join(vscode_dir, f)
        if os.path.exists(path):
            os.remove(path)

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
