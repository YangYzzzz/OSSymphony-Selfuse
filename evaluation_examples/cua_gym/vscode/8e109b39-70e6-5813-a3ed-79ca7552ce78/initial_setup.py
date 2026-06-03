"""
Initial Setup: Configure Docker-based debugging for a Python Flask application in VSCode
Task ID: vscode_gf6_040
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_040'
PROJECT_DIR = f'{WORKDIR}/projects/docker-python-debug'


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
    os.makedirs(f'{PROJECT_DIR}/app', exist_ok=True)

    # --- app/__init__.py ---
    with open(f'{PROJECT_DIR}/app/__init__.py', 'w') as f:
        f.write('''from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-2025'

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
''')

    # --- app/main.py ---
    with open(f'{PROJECT_DIR}/app/main.py', 'w') as f:
        f.write('''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
''')

    # --- app/routes.py ---
    with open(f'{PROJECT_DIR}/app/routes.py', 'w') as f:
        f.write('''from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

# In-memory user store for demo purposes
USERS = [
    {"id": 1, "name": "Sarah Chen", "email": "sarah.chen@example.com", "role": "admin"},
    {"id": 2, "name": "Marcus Johnson", "email": "marcus.j@example.com", "role": "editor"},
    {"id": 3, "name": "Priya Patel", "email": "priya.p@example.com", "role": "viewer"},
    {"id": 4, "name": "James O'Brien", "email": "james.ob@example.com", "role": "editor"},
    {"id": 5, "name": "Aiko Tanaka", "email": "aiko.t@example.com", "role": "admin"},
]


@api_bp.route('/api/users', methods=['GET'])
def get_users():
    """Return all users, optionally filtered by role."""
    role = request.args.get('role')
    if role:
        filtered = [u for u in USERS if u['role'] == role]
        return jsonify({"users": filtered, "count": len(filtered)})
    return jsonify({"users": USERS, "count": len(USERS)})


@api_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a single user by ID."""
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@api_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.2.0"})
''')

    # --- requirements.txt ---
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''flask==3.0.2
debugpy==1.8.1
gunicorn==21.2.0
''')

    # --- Dockerfile ---
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write('''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.main:app
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
''')

    # --- docker-compose.yml (only 'api' service, NO debug service) ---
    docker_compose = {
        "version": "3.8",
        "services": {
            "api": {
                "build": ".",
                "ports": ["5000:5000"],
                "volumes": [".:/app"],
                "environment": {
                    "FLASK_APP": "app.main:app",
                    "FLASK_ENV": "development"
                },
                "command": "flask run --host 0.0.0.0"
            }
        }
    }

    # Write docker-compose.yml as YAML manually for proper formatting
    with open(f'{PROJECT_DIR}/docker-compose.yml', 'w') as f:
        f.write('''version: "3.8"

services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      FLASK_APP: app.main:app
      FLASK_ENV: development
    command: flask run --host 0.0.0.0
''')

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.pyc
.env
*.egg-info/
dist/
build/
.venv/
''')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
