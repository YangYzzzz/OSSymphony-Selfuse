"""
Initial Setup: Multi-root workspace with empty settings
Task ID: vscode_we_029
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_029'
PROJECTS_DIR = os.path.join(WORKDIR, 'projects')
WORKSPACE_FILE = os.path.join(PROJECTS_DIR, 'fullstack.code-workspace')


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
    # Create project directories
    for folder in ['frontend', 'backend', 'shared']:
        folder_path = os.path.join(PROJECTS_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)

    # Create some realistic files in each folder
    # Frontend
    frontend_dir = os.path.join(PROJECTS_DIR, 'frontend')
    with open(os.path.join(frontend_dir, 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fullstack App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>
""")
    with open(os.path.join(frontend_dir, 'app.js'), 'w') as f:
        f.write("""// Main application entry point
const API_BASE = 'http://localhost:3000/api';

async function fetchUsers() {
    const response = await fetch(`${API_BASE}/users`);
    const data = await response.json();
    return data;
}

async function renderDashboard() {
    const users = await fetchUsers();
    const container = document.getElementById('app');
    container.innerHTML = users.map(u => `<div class="user-card">${u.name}</div>`).join('');
}

document.addEventListener('DOMContentLoaded', renderDashboard);
""")
    with open(os.path.join(frontend_dir, 'styles.css'), 'w') as f:
        f.write("""body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.user-card {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
""")

    # Backend
    backend_dir = os.path.join(PROJECTS_DIR, 'backend')
    with open(os.path.join(backend_dir, 'server.py'), 'w') as f:
        f.write("""from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

users = [
    {"id": 1, "name": "Sarah Chen", "role": "Engineer", "joined": "2024-01-15"},
    {"id": 2, "name": "Marcus Johnson", "role": "Designer", "joined": "2023-11-20"},
    {"id": 3, "name": "Aisha Patel", "role": "Product Manager", "joined": "2024-03-08"},
]

@app.route('/api/users')
def get_users():
    return jsonify(users)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
""")
    with open(os.path.join(backend_dir, 'requirements.txt'), 'w') as f:
        f.write("flask==3.0.0\nrequests==2.31.0\npytest==7.4.3\n")

    # Shared
    shared_dir = os.path.join(PROJECTS_DIR, 'shared')
    with open(os.path.join(shared_dir, 'config.py'), 'w') as f:
        f.write("""# Shared configuration constants
DATABASE_URL = "postgresql://localhost:5432/fullstack_db"
API_VERSION = "v1"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
LOG_LEVEL = "INFO"
""")
    with open(os.path.join(shared_dir, 'utils.py'), 'w') as f:
        f.write("""import hashlib
import re
from datetime import datetime


def sanitize_input(text: str) -> str:
    return re.sub(r'[<>&\"\\'']', '', text.strip())


def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def format_timestamp(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')
""")

    # Create the workspace file with EMPTY settings
    workspace = {
        "folders": [
            {"path": "frontend"},
            {"path": "backend"},
            {"path": "shared"}
        ],
        "settings": {}
    }
    with open(WORKSPACE_FILE, 'w') as f:
        json.dump(workspace, f, indent=4)

    print(f'Workspace file created: {WORKSPACE_FILE}')
    print(f'Project directories created with sample files')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace DISPLAY=:0')


create_initial()
