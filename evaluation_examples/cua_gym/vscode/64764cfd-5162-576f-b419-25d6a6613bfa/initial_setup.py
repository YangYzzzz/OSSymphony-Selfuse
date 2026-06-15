"""
Initial Setup: Create a Python project workspace for remote debugging task.
Task ID: vscode_td_057
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_057'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'remote-debug')


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
    # Create the project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # Create a realistic Python application
    main_py = os.path.join(PROJECT_DIR, 'src', 'main.py')
    with open(main_py, 'w') as f:
        f.write('''"""Remote inventory management service."""

import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

inventory = {}


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "inventory-manager"})


@app.route("/items", methods=["GET"])
def list_items():
    logger.info("Listing all inventory items")
    return jsonify(list(inventory.values()))


@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    item = inventory.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "Missing item id"}), 400
    inventory[item_id] = {
        "id": item_id,
        "name": data.get("name", ""),
        "quantity": data.get("quantity", 0),
        "warehouse": data.get("warehouse", "main"),
    }
    logger.info(f"Created item {item_id}")
    return jsonify(inventory[item_id]), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
''')

    # Create a config module
    config_py = os.path.join(PROJECT_DIR, 'src', 'config.py')
    with open(config_py, 'w') as f:
        f.write('''"""Application configuration."""

import os


class Config:
    DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", 8080))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///inventory.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
''')

    # Create a test file
    test_py = os.path.join(PROJECT_DIR, 'tests', 'test_main.py')
    with open(test_py, 'w') as f:
        f.write('''"""Tests for the inventory management service."""

import pytest
from src.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_create_and_get_item(client):
    item_data = {"id": "SKU001", "name": "Widget", "quantity": 50}
    response = client.post("/items", json=item_data)
    assert response.status_code == 201

    response = client.get("/items/SKU001")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Widget"
    assert data["quantity"] == 50
''')

    # Create requirements.txt
    req_txt = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(req_txt, 'w') as f:
        f.write('''flask==3.0.0
debugpy==1.8.0
pytest==7.4.3
gunicorn==21.2.0
''')

    # Create a Dockerfile (realistic remote deployment context)
    dockerfile = os.path.join(PROJECT_DIR, 'Dockerfile')
    with open(dockerfile, 'w') as f:
        f.write('''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# debugpy listens on port 5678 for remote debugging
EXPOSE 8080 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "src/main.py"]
''')

    # Create a README
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''# Remote Debug - Inventory Manager

A Flask-based inventory management microservice deployed on remote server 192.168.1.100.

## Development

```bash
pip install -r requirements.txt
python src/main.py
```

## Remote Deployment

The service runs in a Docker container on the remote server with debugpy enabled on port 5678.

```bash
docker build -t inventory-manager .
docker run -p 8080:8080 -p 5678:5678 inventory-manager
```
''')

    # Ensure NO .vscode/launch.json exists (task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: src/main.py, src/config.py, tests/test_main.py, requirements.txt, Dockerfile, README.md')
    print(f'No .vscode/launch.json exists (task is to create it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
