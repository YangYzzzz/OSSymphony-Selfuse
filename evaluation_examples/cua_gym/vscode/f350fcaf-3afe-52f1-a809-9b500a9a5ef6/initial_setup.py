"""
Initial Setup: VSCode Find & Replace regex to swap route decorator parameters
Task ID: vscode_edit_048
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_048'
OUTPUT = f'{WORKDIR}/Desktop/routes.py'


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
    # Ensure Desktop directory exists
    desktop_dir = f'{WORKDIR}/Desktop'
    os.makedirs(desktop_dir, exist_ok=True)

    # Create a realistic 60-line Flask routes.py with 5 route decorators
    # MUST use format @app.route("/path", methods=["METHOD"]) — NOT swapped
    routes_content = '''"""
Flask application routes for a task management web service.
Handles CRUD operations for tasks, users, and project management.
"""

from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data store (replace with database in production)
tasks = {}
users = {}
task_counter = 0
user_counter = 0


@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    """Retrieve all tasks from the task store."""
    task_list = list(tasks.values())
    return jsonify({
        "tasks": task_list,
        "count": len(task_list),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/api/tasks/<int:task_id>", methods=["POST"])
def create_task(task_id):
    """Create a new task with provided data."""
    global task_counter
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="Missing required field: title")
    task_counter += 1
    task = {
        "id": task_counter,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "assignee": data.get("assignee", None)
    }
    tasks[task_counter] = task
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>/update", methods=["PUT"])
def update_task(task_id):
    """Update an existing task by its ID."""
    if task_id not in tasks:
        abort(404, description=f"Task {task_id} not found")
    data = request.get_json()
    task = tasks[task_id]
    if "title" in data:
        task["title"] = data["title"]
    if "status" in data:
        valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
        if data["status"] not in valid_statuses:
            abort(400, description="Invalid status value")
        task["status"] = data["status"]
    if "description" in data:
        task["description"] = data["description"]
    task["updated_at"] = datetime.utcnow().isoformat()
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>/delete", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task permanently by its ID."""
    if task_id not in tasks:
        abort(404, description=f"Task {task_id} not found")
    deleted_task = tasks.pop(task_id)
    return jsonify({
        "message": f"Task {task_id} deleted successfully",
        "deleted": deleted_task
    })


@app.route("/api/users/register", methods=["POST"])
def register_user():
    """Register a new user in the system."""
    global user_counter
    data = request.get_json()
    if not data or "username" not in data or "email" not in data:
        abort(400, description="Missing required fields: username, email")
    user_counter += 1
    user = {
        "id": user_counter,
        "username": data["username"],
        "email": data["email"],
        "role": data.get("role", "developer"),
        "registered_at": datetime.utcnow().isoformat()
    }
    users[user_counter] = user
    return jsonify(user), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
'''

    with open(OUTPUT, 'w') as f:
        f.write(routes_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the routes.py file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
