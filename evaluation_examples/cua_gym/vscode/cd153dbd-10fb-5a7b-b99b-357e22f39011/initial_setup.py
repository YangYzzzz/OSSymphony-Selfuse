"""
Initial Setup: Resolve merge conflict in app.py by accepting both changes
Task ID: vscode_stu_061
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_061'
REPO_DIR = f'{WORKDIR}/workspace'
APP_PY = f'{REPO_DIR}/app.py'


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


def run(cmd, cwd=None):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result


def create_initial():
    # Clean up any existing repo
    if os.path.exists(REPO_DIR):
        import shutil
        shutil.rmtree(REPO_DIR)

    os.makedirs(REPO_DIR, exist_ok=True)

    # Initialize git repo
    run('git init', cwd=REPO_DIR)
    run('git config user.email "student@university.edu"', cwd=REPO_DIR)
    run('git config user.name "Student"', cwd=REPO_DIR)

    # Create base version of app.py (common ancestor)
    base_content = '''from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = []


@app.route("/")
def home():
    return "Welcome to the Task Manager API"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True)
'''

    with open(APP_PY, 'w') as f:
        f.write(base_content)

    # Also create a requirements.txt for realism
    with open(f'{REPO_DIR}/requirements.txt', 'w') as f:
        f.write("flask==3.0.0\ngunicorn==21.2.0\npytest==7.4.3\n")

    with open(f'{REPO_DIR}/README.md', 'w') as f:
        f.write("# Task Manager API\n\nA simple Flask-based task management REST API for the CS301 group project.\n\n## Setup\n```\npip install -r requirements.txt\npython app.py\n```\n")

    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Initial commit: basic task manager API"', cwd=REPO_DIR)

    # Create a feature branch with incoming changes
    run('git checkout -b feature/add-validation', cwd=REPO_DIR)

    # Incoming changes: add validation and a delete endpoint
    incoming_content = '''from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = []


@app.route("/")
def home():
    return "Welcome to the Task Manager API"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
'''

    with open(APP_PY, 'w') as f:
        f.write(incoming_content)

    run('git add app.py', cwd=REPO_DIR)
    run('git commit -m "Add input validation and delete endpoint"', cwd=REPO_DIR)

    # Go back to main/master and make conflicting changes
    # Detect default branch name
    result = run('git branch --list main master', cwd=REPO_DIR)
    default_branch = 'main' if 'main' in result.stdout else 'master'
    run(f'git checkout {default_branch}', cwd=REPO_DIR)

    # Current changes: add priority field and update endpoint
    current_content = '''from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = []


@app.route("/")
def home():
    return "Welcome to the Task Manager API"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "priority": data.get("priority", "medium"),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = data.get("done", task["done"])
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
'''

    with open(APP_PY, 'w') as f:
        f.write(current_content)

    run('git add app.py', cwd=REPO_DIR)
    run('git commit -m "Add priority field and update endpoint"', cwd=REPO_DIR)

    # Now attempt merge — this will create the conflict
    result = run('git merge feature/add-validation', cwd=REPO_DIR)
    print(f"Merge result: {result.stdout}")
    print(f"Merge stderr: {result.stderr}")

    # Verify conflict markers exist
    with open(APP_PY, 'r') as f:
        content = f.read()

    if '<<<<<<< HEAD' in content:
        print("SUCCESS: Merge conflict created in app.py")
    else:
        print("WARNING: No conflict markers found, creating manually")
        # If git auto-resolved, we need to manually create the conflict
        run('git merge --abort', cwd=REPO_DIR)

        conflict_content = '''from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = []


@app.route("/")
def home():
    return "Welcome to the Task Manager API"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
<<<<<<< HEAD
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "priority": data.get("priority", "medium"),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = data.get("done", task["done"])
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404
=======
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200
>>>>>>> feature/add-validation


if __name__ == "__main__":
    app.run(debug=True)
'''
        with open(APP_PY, 'w') as f:
            f.write(conflict_content)

    print(f"app.py created at: {APP_PY}")

    # Launch VSCode with the workspace folder and the conflicted file open
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{APP_PY}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
