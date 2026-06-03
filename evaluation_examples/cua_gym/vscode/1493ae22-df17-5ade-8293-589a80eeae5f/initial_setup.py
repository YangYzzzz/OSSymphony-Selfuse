"""
Initial Setup: Configure Python debug launch configuration
Task ID: vscode_wf_013
Domain: vscode

Creates a Flask app.py in ~/project and opens VSCode with that folder.
No .vscode/launch.json exists yet — that is the task for the agent.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_013'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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

    # Remove any existing .vscode/launch.json to ensure clean initial state
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    # Create a realistic Flask application file
    app_py_content = '''"""
Flask Application - Task Management API
A simple REST API for managing tasks with Flask.
"""

from flask import Flask, jsonify, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory task store
tasks = [
    {"id": 1, "title": "Review pull request #42", "status": "pending", "assignee": "Sarah Chen"},
    {"id": 2, "title": "Deploy staging environment", "status": "in_progress", "assignee": "Marcus Johnson"},
    {"id": 3, "title": "Update API documentation", "status": "completed", "assignee": "Aisha Patel"},
    {"id": 4, "title": "Fix database connection pooling", "status": "pending", "assignee": "David Kim"},
]

next_id = 5


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "1.3.0"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Retrieve all tasks, optionally filtered by status."""
    status_filter = request.args.get("status")
    if status_filter:
        filtered = [t for t in tasks if t["status"] == status_filter]
        return jsonify(filtered)
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Retrieve a single task by ID."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": next_id,
        "title": data["title"],
        "status": data.get("status", "pending"),
        "assignee": data.get("assignee", "Unassigned"),
    }
    tasks.append(new_task)
    next_id += 1
    logger.info(f"Created task {new_task['id']}: {new_task['title']}")
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.update({k: v for k, v in data.items() if k in ("title", "status", "assignee")})
    logger.info(f"Updated task {task_id}")
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_len:
        return jsonify({"error": "Task not found"}), 404
    logger.info(f"Deleted task {task_id}")
    return jsonify({"message": f"Task {task_id} deleted"})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task Management API")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
'''

    app_py_path = os.path.join(PROJECT_DIR, 'app.py')
    with open(app_py_path, 'w') as f:
        f.write(app_py_content)

    # Also create a requirements.txt for realism
    requirements_content = """flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
pytest==7.4.3
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'  app.py: {app_py_path}')
    print(f'  .vscode/launch.json: does NOT exist (task for agent)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
