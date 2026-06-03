"""
Initial Setup: Configure an advanced Git branch management workflow
Task ID: vscode_wf_063
Domain: vscode

Creates ~/project as a git repo on main with an initial commit,
some realistic project files, and opens VSCode.
No extra branches, no Git Graph extension, no git settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_063'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
        print(f"CMD FAILED: {cmd}\nSTDERR: {result.stderr}")
    return result


def create_initial():
    # --- 1. Create project directory ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- 2. Initialize git repo ---
    run('git init', cwd=PROJECT_DIR)
    run('git config user.email "developer@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Alex Developer"', cwd=PROJECT_DIR)

    # --- 3. Create realistic project files ---

    # README.md
    readme_content = """# TaskFlow - Project Management Dashboard

A lightweight project management tool built with Python and Flask.

## Features
- Task creation and assignment
- Sprint planning board
- Team velocity tracking
- Burndown chart visualization

## Getting Started

```bash
pip install -r requirements.txt
python src/app.py
```

## License
MIT License
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # requirements.txt
    requirements = """flask==3.0.2
sqlalchemy==2.0.25
jinja2==3.1.3
pytest==8.0.1
requests==2.31.0
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # src directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # src/app.py
    app_content = """from flask import Flask, render_template, jsonify
from models import db, Task, Sprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
db.init_app(app)


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/api/tasks')
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])


@app.route('/api/sprints')
def get_sprints():
    sprints = Sprint.query.all()
    return jsonify([s.to_dict() for s in sprints])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
"""
    with open(os.path.join(src_dir, 'app.py'), 'w') as f:
        f.write(app_content)

    # src/models.py
    models_content = """from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')
    assignee = db.Column(db.String(100))
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(10), default='medium')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'assignee': self.assignee,
            'priority': self.priority,
        }


class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    tasks = db.relationship('Task', backref='sprint', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
        }
"""
    with open(os.path.join(src_dir, 'models.py'), 'w') as f:
        f.write(models_content)

    # src/utils.py
    utils_content = """import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def calculate_velocity(completed_points: list) -> float:
    \"\"\"Calculate team velocity from last N sprints.\"\"\"
    if not completed_points:
        return 0.0
    return sum(completed_points) / len(completed_points)


def estimate_completion(remaining_points: int, velocity: float) -> int:
    \"\"\"Estimate number of sprints to complete remaining work.\"\"\"
    if velocity <= 0:
        return -1
    return int(remaining_points / velocity) + 1


def format_date_range(start: datetime, end: datetime) -> str:
    \"\"\"Format a date range for sprint display.\"\"\"
    return f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}"
"""
    with open(os.path.join(src_dir, 'utils.py'), 'w') as f:
        f.write(utils_content)

    # .gitignore
    gitignore = """__pycache__/
*.pyc
*.pyo
.env
*.db
.vscode/
venv/
dist/
*.egg-info/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # --- 4. Initial commit on main ---
    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Initial commit: TaskFlow project structure"', cwd=PROJECT_DIR)

    # Ensure branch is named "main"
    run('git branch -M main', cwd=PROJECT_DIR)

    print(f'Initial project created: {PROJECT_DIR}')

    # --- 5. Ensure no git-related settings in VSCode ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}
    # Remove any git settings that should not be present
    for key in ['git.mergeEditor', 'git.autoStash', 'git.branchProtection']:
        settings.pop(key, None)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    # --- 6. Ensure git-graph extension is NOT installed ---
    run('code --uninstall-extension mhutchie.git-graph 2>/dev/null || true')

    # --- 7. Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
