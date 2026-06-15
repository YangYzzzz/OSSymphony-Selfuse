"""
Initial Setup: Add a pytest task to tasks.json in a Flask API project
Task ID: vscode_td_003
Domain: vscode (tasks.json configuration)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'flask-api')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')
TESTS_DIR = os.path.join(PROJECT_DIR, 'tests')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # Create the existing tasks.json with only a build task
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Install Dependencies",
                "type": "shell",
                "command": "pip install -r requirements.txt",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "problemMatcher": []
            }
        ]
    }
    with open(TASKS_PATH, 'w') as f:
        json.dump(tasks_config, f, indent=4)
    print(f'Created tasks.json: {TASKS_PATH}')

    # Create project files for a realistic Flask API
    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("flask==3.0.0\nflask-restful==0.3.10\npytest==7.4.3\npytest-cov==4.1.0\nrequests==2.31.0\n")

    # app.py
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write('''from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demo purposes
inventory = [
    {"id": 1, "name": "Wireless Mouse", "price": 29.99, "stock": 150},
    {"id": 2, "name": "Mechanical Keyboard", "price": 89.95, "stock": 75},
    {"id": 3, "name": "USB-C Hub", "price": 45.00, "stock": 200},
    {"id": 4, "name": "Monitor Stand", "price": 34.50, "stock": 60},
]


@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(inventory)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in inventory if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_product = {
        "id": max(p["id"] for p in inventory) + 1 if inventory else 1,
        "name": data["name"],
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_product)
    return jsonify(new_product), 201


if __name__ == "__main__":
    app.run(debug=True, port=5050)
''')

    # tests/__init__.py
    with open(os.path.join(TESTS_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # tests/test_api.py
    with open(os.path.join(TESTS_DIR, 'test_api.py'), 'w') as f:
        f.write('''import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 4


def test_get_product_by_id(client):
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Wireless Mouse"


def test_get_product_not_found(client):
    response = client.get("/api/products/999")
    assert response.status_code == 404


def test_create_product(client):
    new_product = {"name": "Laptop Stand", "price": 55.00, "stock": 30}
    response = client.post("/api/products", json=new_product)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Laptop Stand"
''')

    # tests/test_models.py
    with open(os.path.join(TESTS_DIR, 'test_models.py'), 'w') as f:
        f.write('''import pytest


def test_product_price_positive():
    """Ensure product prices are non-negative."""
    price = 29.99
    assert price >= 0


def test_stock_integer():
    """Ensure stock values are integers."""
    stock = 150
    assert isinstance(stock, int)
''')

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("__pycache__/\n*.pyc\n.env\nvenv/\n*.egg-info/\ndist/\nbuild/\n.pytest_cache/\n")

    print(f'Created Flask API project at: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
