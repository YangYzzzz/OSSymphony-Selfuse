"""
Initial Setup: VSCode Flask debug launch.json task
Task ID: vscode_dbg_031
Domain: vs_code

Creates ~/projects/flask-app/app.py with a realistic Flask application.
No .vscode folder is created (the agent must create it).
Opens VSCode with the flask-app folder as the workspace.
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_031'
PROJECT_DIR = f'{WORKDIR}/projects/flask-app'
APP_PY = f'{PROJECT_DIR}/app.py'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # Ensure project directory exists
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Remove .vscode if it somehow already exists (idempotent reset)
    if os.path.exists(VSCODE_DIR):
        shutil.rmtree(VSCODE_DIR)

    # Write a realistic Flask application
    app_content = '''from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory store for demo purposes
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read Python docs", "done": True},
    {"id": 3, "title": "Write unit tests", "done": False},
]

HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Task Manager</title></head>
<body>
  <h1>Task Manager</h1>
  <ul>
    {% for task in tasks %}
      <li>{{ task.title }} - {{ "Done" if task.done else "Pending" }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE, tasks=tasks)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as JSON."""
    return jsonify({"tasks": tasks, "count": len(tasks)})


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Return a single task by ID."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task from JSON body."""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    new_task = {
        "id": max(t["id"] for t in tasks) + 1 if tasks else 1,
        "title": data["title"],
        "done": data.get("done", False),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update task done-status."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json() or {}
    if "done" in data:
        task["done"] = bool(data["done"])
    if "title" in data:
        task["title"] = data["title"]
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_len:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"deleted": task_id}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
'''

    with open(APP_PY, 'w') as f:
        f.write(app_content)
    print(f'Created: {APP_PY}')

    # Verify no .vscode directory exists
    assert not os.path.exists(VSCODE_DIR), f'.vscode directory should NOT exist in initial state'
    print('Verified: no .vscode directory present (as required by task)')

    # GUI-ready startup: open VSCode with the flask-app folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with flask-app folder (DISPLAY=:0)')


create_initial()
