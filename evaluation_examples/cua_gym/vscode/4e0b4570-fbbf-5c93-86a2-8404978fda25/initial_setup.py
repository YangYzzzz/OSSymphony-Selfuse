"""
Initial Setup: Configure VSCode with empty default settings and open it.
Task ID: vscode_we_017
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_017'

# VSCode config paths
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Workspace folder with some sample files so VSCode has something to show
WORKSPACE = os.path.join(WORKDIR, "workspace")


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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings.json (default state)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)
    print(f"Settings file created: {SETTINGS_PATH}")

    # Create a workspace with some sample files for context
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a sample Python file
    sample_py = os.path.join(WORKSPACE, "app.py")
    with open(sample_py, "w") as f:
        f.write('''"""Simple Flask application for inventory management."""

from flask import Flask, jsonify

app = Flask(__name__)

inventory = [
    {"id": 1, "name": "Wireless Mouse", "quantity": 45, "price": 29.99},
    {"id": 2, "name": "Mechanical Keyboard", "quantity": 30, "price": 89.50},
    {"id": 3, "name": "USB-C Hub", "quantity": 60, "price": 34.99},
    {"id": 4, "name": "Monitor Stand", "quantity": 25, "price": 49.00},
]


@app.route("/api/items")
def get_items():
    return jsonify(inventory)


@app.route("/api/items/<int:item_id>")
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
''')

    readme = os.path.join(WORKSPACE, "README.md")
    with open(readme, "w") as f:
        f.write('''# Inventory Management API

A simple REST API for managing product inventory.

## Setup

```bash
pip install flask
python app.py
```

## Endpoints

- `GET /api/items` — List all items
- `GET /api/items/<id>` — Get item by ID
''')

    print(f"Workspace created: {WORKSPACE}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
