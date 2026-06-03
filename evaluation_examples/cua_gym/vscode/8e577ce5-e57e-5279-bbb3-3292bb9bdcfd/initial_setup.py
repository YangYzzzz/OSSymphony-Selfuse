"""
Initial Setup: Set up terminal shell integration and command decoration
Task ID: vscode_rrt_079
Domain: vs_code

Creates a VSCode environment with basic settings but WITHOUT terminal
shell integration settings. Opens VSCode with a workspace folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_079'

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Create workspace directory with some sample files
WORKSPACE = os.path.join(WORKDIR, "workspace")
os.makedirs(WORKSPACE, exist_ok=True)

# Create a sample Python project for realistic workspace content
os.makedirs(os.path.join(WORKSPACE, "src"), exist_ok=True)

with open(os.path.join(WORKSPACE, "src", "app.py"), "w") as f:
    f.write("""#!/usr/bin/env python3
\"\"\"Simple Flask application for inventory management.\"\"\"

from flask import Flask, jsonify, request

app = Flask(__name__)

inventory = [
    {"id": 1, "name": "Wireless Keyboard", "price": 49.99, "stock": 120},
    {"id": 2, "name": "USB-C Hub", "price": 35.50, "stock": 85},
    {"id": 3, "name": "Monitor Stand", "price": 79.00, "stock": 42},
    {"id": 4, "name": "Laptop Sleeve 15-inch", "price": 24.99, "stock": 200},
    {"id": 5, "name": "Ergonomic Mouse", "price": 62.00, "stock": 67},
]


@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify(inventory)


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
""")

with open(os.path.join(WORKSPACE, "src", "utils.py"), "w") as f:
    f.write("""\"\"\"Utility functions for data processing.\"\"\"

import csv
from datetime import datetime


def parse_timestamp(ts_string: str) -> datetime:
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(ts_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse timestamp: {ts_string}")


def load_csv(filepath: str) -> list:
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
""")

with open(os.path.join(WORKSPACE, "README.md"), "w") as f:
    f.write("""# Inventory Management API

A lightweight REST API for tracking product inventory.

## Quick Start

```bash
pip install flask
python src/app.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/items | List all items |
| GET | /api/items/:id | Get item by ID |
""")

# Set up VSCode settings with some basic config but NO shell integration settings
os.makedirs(VSCODE_USER, exist_ok=True)

settings = {
    "editor.fontSize": 14,
    "editor.tabSize": 4,
    "editor.wordWrap": "on",
    "workbench.colorTheme": "Default Dark Modern",
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "editor.minimap.enabled": True,
    "editor.renderWhitespace": "selection",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.cursorBlinking": True
}

with open(SETTINGS_PATH, "w") as f:
    json.dump(settings, f, indent=4)

print(f"Settings written to: {SETTINGS_PATH}")
print(f"Workspace created at: {WORKSPACE}")


# Launch VSCode with the workspace
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


launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
print("GUI_READY: launched VSCode with DISPLAY=:0")
