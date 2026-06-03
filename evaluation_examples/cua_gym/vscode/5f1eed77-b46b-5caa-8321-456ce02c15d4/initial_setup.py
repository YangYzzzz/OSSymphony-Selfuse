"""
Initial Setup: Configure a custom keyboard shortcut in VSCode that maps Ctrl+Shift+D to run the task 'Deploy Staging'
Task ID: vscode_ops_047
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_047'
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
VSCODE_DIR = os.path.join(WORKSPACE_DIR, '.vscode')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')


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
    # 1. Create workspace directory with project files
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create a realistic project structure
    # Main deployment script
    deploy_script = os.path.join(WORKSPACE_DIR, 'deploy.sh')
    with open(deploy_script, 'w') as f:
        f.write("""#!/bin/bash
# Deploy to staging environment
# Usage: ./deploy.sh [environment]

set -euo pipefail

ENVIRONMENT="${1:-staging}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
APP_NAME="inventory-service"
REGISTRY="registry.internal.acme.com"

echo "=== Deploying $APP_NAME to $ENVIRONMENT ==="
echo "Timestamp: $TIMESTAMP"

# Build Docker image
echo "Building Docker image..."
# docker build -t $REGISTRY/$APP_NAME:$TIMESTAMP .

# Run database migrations
echo "Running database migrations..."
# python manage.py migrate --database=$ENVIRONMENT

# Deploy to Kubernetes
echo "Deploying to $ENVIRONMENT cluster..."
# kubectl set image deployment/$APP_NAME $APP_NAME=$REGISTRY/$APP_NAME:$TIMESTAMP -n $ENVIRONMENT

echo "Deployment to $ENVIRONMENT complete!"
""")

    # Application config
    app_config = os.path.join(WORKSPACE_DIR, 'config.yaml')
    with open(app_config, 'w') as f:
        f.write("""# Inventory Service Configuration
app:
  name: inventory-service
  version: 2.4.1
  port: 8080

database:
  host: db.internal.acme.com
  port: 5432
  name: inventory_db
  pool_size: 20

staging:
  url: https://staging.acme.com
  api_key_env: STAGING_API_KEY
  debug: true

production:
  url: https://api.acme.com
  api_key_env: PROD_API_KEY
  debug: false

logging:
  level: INFO
  format: json
  output: stdout
""")

    # Python application file
    app_py = os.path.join(WORKSPACE_DIR, 'app.py')
    with open(app_py, 'w') as f:
        f.write("""\"\"\"Inventory Service - Main Application\"\"\"
import os
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

ITEMS = [
    {"id": 1, "name": "Widget A", "quantity": 150, "price": 24.99},
    {"id": 2, "name": "Widget B", "quantity": 85, "price": 34.50},
    {"id": 3, "name": "Gadget Pro", "quantity": 200, "price": 129.99},
    {"id": 4, "name": "Component X", "quantity": 42, "price": 8.75},
]


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


@app.route("/api/inventory")
def get_inventory():
    return jsonify({"items": ITEMS, "total": len(ITEMS)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
""")

    # 2. Create .vscode/tasks.json with the Deploy Staging task
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Deploy Staging",
                "type": "shell",
                "command": "bash",
                "args": ["deploy.sh", "staging"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Run Tests",
                "type": "shell",
                "command": "python",
                "args": ["-m", "pytest", "tests/", "-v"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Lint Code",
                "type": "shell",
                "command": "flake8",
                "args": [".", "--max-line-length=120"],
                "group": "test",
                "problemMatcher": []
            }
        ]
    }

    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    with open(tasks_path, 'w') as f:
        json.dump(tasks_config, f, indent=4)

    print(f'Created tasks.json at: {tasks_path}')

    # 3. Ensure keybindings.json is empty (no custom keybindings)
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)

    print(f'Created empty keybindings.json at: {KEYBINDINGS_PATH}')

    # 4. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
