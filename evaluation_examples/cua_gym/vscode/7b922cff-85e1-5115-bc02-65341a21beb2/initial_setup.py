"""
Initial Setup: Configure VSCode Git settings (autofetch, autofetchPeriod, defaultBranchName)
Task ID: vscode_git_042
Domain: vs_code

This script creates the initial VM state BEFORE the agent acts:
- VSCode settings.json WITHOUT git.autofetch, git.autofetchPeriod, or git.defaultBranchName
- A realistic project workspace folder opened in VSCode
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(HOME, 'project_alpha')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # --- Create VSCode User config directory ---
    os.makedirs(VSCODE_USER, exist_ok=True)

    # --- Write initial settings.json WITHOUT git autofetch settings ---
    # These settings must NOT contain git.autofetch, git.autofetchPeriod, or git.defaultBranchName
    initial_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "editor.formatOnSave": False,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark+",
        "workbench.startupEditor": "welcomePage",
        "terminal.integrated.fontSize": 13,
        "files.autoSave": "off",
        "files.trimTrailingWhitespace": True,
        "explorer.confirmDelete": True,
        "git.enabled": True,
        "git.confirmSync": True
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(initial_settings, f, indent=4)
    print(f'Initial settings.json created: {SETTINGS_PATH}')

    # --- Create a realistic project workspace ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a README.md
    readme_path = os.path.join(WORKSPACE_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("""# Project Alpha

A Python web service for inventory management.

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
pip install -r requirements.txt
python app.py
```

## Structure
- `app.py` — Main application entry point
- `models/` — Database models
- `api/` — REST API endpoints
- `tests/` — Unit and integration tests
""")

    # Create app.py
    app_path = os.path.join(WORKSPACE_DIR, 'app.py')
    with open(app_path, 'w') as f:
        f.write("""from flask import Flask, jsonify
from models.inventory import Inventory

app = Flask(__name__)

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Inventory.get_all()
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Inventory.get_by_id(item_id)
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
""")

    # Create models directory and a model file
    models_dir = os.path.join(WORKSPACE_DIR, 'models')
    os.makedirs(models_dir, exist_ok=True)
    inventory_path = os.path.join(models_dir, 'inventory.py')
    with open(inventory_path, 'w') as f:
        f.write("""class Inventory:
    _items = [
        {'id': 1, 'name': 'Widget A', 'quantity': 150, 'price': 9.99},
        {'id': 2, 'name': 'Gadget B', 'quantity': 75, 'price': 24.50},
        {'id': 3, 'name': 'Component C', 'quantity': 200, 'price': 4.99},
    ]

    @classmethod
    def get_all(cls):
        return cls._items

    @classmethod
    def get_by_id(cls, item_id):
        return next((i for i in cls._items if i['id'] == item_id), None)
""")

    # Create requirements.txt
    req_path = os.path.join(WORKSPACE_DIR, 'requirements.txt')
    with open(req_path, 'w') as f:
        f.write("flask>=2.0\nsqlalchemy>=1.4\npytest>=7.0\n")

    print(f'Workspace created: {WORKSPACE_DIR}')

    # --- GUI-ready startup: open VSCode settings.json so agent can edit it ---
    launch_gui(f'code --new-window "{WORKSPACE_DIR}"', delay_sec=2.0)
    launch_gui(f'code --reuse-window "{SETTINGS_PATH}"', delay_sec=1.5)
    print('GUI_READY: launched VSCode with project workspace and settings.json open')


create_initial()
