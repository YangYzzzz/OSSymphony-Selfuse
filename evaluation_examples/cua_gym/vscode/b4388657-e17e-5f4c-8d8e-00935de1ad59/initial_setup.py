"""
Initial Setup: Configure a pair programming workflow in ~/project
Task ID: vscode_wf_084
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
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

def create_project():
    """Create a realistic Python web project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'js'), exist_ok=True)

    # Main application file
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write('''from flask import Flask, render_template, jsonify, request
from models import db, Task, User
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskboard.db"
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"
db.init_app(app)


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        assigned_to=data.get("assigned_to"),
        priority=data.get("priority", "medium"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.assigned_to = data.get("assigned_to", task.assigned_to)
    task.priority = data.get("priority", task.priority)
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)
''')

    # Models file
    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write('''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default="developer")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="todo")
    priority = db.Column(db.String(10), default="medium")
    assigned_to = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
''')

    # Requirements
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''flask==3.0.0
flask-sqlalchemy==3.1.1
pytest==7.4.3
pytest-flask==1.3.0
requests==2.31.0
gunicorn==21.2.0
''')

    # Test file
    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'tests', 'test_app.py'), 'w') as f:
        f.write('''import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_tasks_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Fix login bug", "priority": "high"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Fix login bug"
    assert data["priority"] == "high"
    assert data["status"] == "todo"


def test_update_task(client):
    client.post("/api/tasks", json={"title": "Write docs"})
    response = client.put(
        "/api/tasks/1",
        json={"status": "in_progress", "assigned_to": "sarah"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "in_progress"
    assert data["assigned_to"] == "sarah"


def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
''')

    # Template
    with open(os.path.join(PROJECT_DIR, 'templates', 'index.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskBoard - Team Project Tracker</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>TaskBoard</h1>
        <nav>
            <a href="/">Dashboard</a>
            <a href="/api/tasks">API</a>
        </nav>
    </header>
    <main>
        <section class="task-list">
            {% for task in tasks %}
            <div class="task-card priority-{{ task.priority }}">
                <h3>{{ task.title }}</h3>
                <p>{{ task.description }}</p>
                <span class="status">{{ task.status }}</span>
                <span class="assignee">{{ task.assigned_to or 'Unassigned' }}</span>
            </div>
            {% endfor %}
        </section>
    </main>
    <script src="/static/js/app.js"></script>
</body>
</html>
''')

    # CSS
    with open(os.path.join(PROJECT_DIR, 'static', 'css', 'style.css'), 'w') as f:
        f.write('''body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.task-list {
    padding: 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}

.task-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #3498db;
}

.task-card.priority-high { border-left-color: #e74c3c; }
.task-card.priority-medium { border-left-color: #f39c12; }
.task-card.priority-low { border-left-color: #27ae60; }
''')

    # JS
    with open(os.path.join(PROJECT_DIR, 'static', 'js', 'app.js'), 'w') as f:
        f.write('''document.addEventListener("DOMContentLoaded", () => {
    console.log("TaskBoard loaded");

    async function fetchTasks() {
        const response = await fetch("/api/tasks");
        return response.json();
    }

    async function createTask(taskData) {
        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(taskData),
        });
        return response.json();
    }
});
''')

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# TaskBoard

A collaborative team task tracking application built with Flask.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Running Tests

```bash
pytest tests/
```

## API Endpoints

- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a task
- `PUT /api/tasks/<id>` - Update a task
- `GET /api/users` - List all users
''')

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('''__pycache__/
*.pyc
*.db
.env
venv/
instance/
''')

    # Ensure NO .vscode directory exists (clean initial state)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Project created at {PROJECT_DIR}')

def main():
    create_project()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project on DISPLAY=:0')

main()
