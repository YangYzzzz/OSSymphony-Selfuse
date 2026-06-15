"""
Initial Setup: Configure a Kubernetes development workflow in ~/project
Task ID: vscode_wf_088
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_088'
PROJECT_DIR = f'{WORKDIR}/project'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic Dockerfile for a Python web app
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
"""
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write(dockerfile_content)

    # Create requirements.txt
    requirements_content = """flask==3.0.2
gunicorn==21.2.0
redis==5.0.1
prometheus-client==0.20.0
"""
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # Create a realistic Flask web application
    app_content = '''"""
Web application for inventory management service.
Provides REST API endpoints for product tracking.
"""

import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory store (replaced by Redis in production)
products = {
    "SKU-1001": {"name": "Wireless Mouse", "price": 29.99, "stock": 150},
    "SKU-1002": {"name": "Mechanical Keyboard", "price": 89.50, "stock": 75},
    "SKU-1003": {"name": "USB-C Hub", "price": 45.00, "stock": 200},
    "SKU-1004": {"name": "Monitor Stand", "price": 34.95, "stock": 60},
    "SKU-1005": {"name": "Webcam HD", "price": 59.99, "stock": 120},
}


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.4.2"})


@app.route("/api/products", methods=["GET"])
def list_products():
    return jsonify({"products": products, "count": len(products)})


@app.route("/api/products/<sku>", methods=["GET"])
def get_product(sku):
    product = products.get(sku)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/products/<sku>/stock", methods=["PUT"])
def update_stock(sku):
    product = products.get(sku)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    product["stock"] = data.get("stock", product["stock"])
    return jsonify(product)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
'''
    with open(f'{PROJECT_DIR}/app.py', 'w') as f:
        f.write(app_content)

    # Create .dockerignore
    dockerignore_content = """__pycache__
*.pyc
.git
.env
.vscode
k8s
"""
    with open(f'{PROJECT_DIR}/.dockerignore', 'w') as f:
        f.write(dockerignore_content)

    # Create a basic .gitignore
    gitignore_content = """__pycache__/
*.pyc
.env
*.log
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    # Ensure NO k8s directory exists (negative constraint)
    # Ensure NO .vscode/tasks.json exists
    # Ensure NO yaml.schemas in settings

    # Create minimal .vscode directory with empty settings (no yaml.schemas)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    os.makedirs(vscode_dir, exist_ok=True)

    # Minimal launch.json for Python debugging (realistic pre-existing config)
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask",
                "type": "debugpy",
                "request": "launch",
                "module": "flask",
                "env": {
                    "FLASK_APP": "app.py",
                    "FLASK_DEBUG": "1"
                },
                "args": ["run", "--port", "8080"],
                "jinja": True
            }
        ]
    }
    with open(f'{vscode_dir}/launch.json', 'w') as f:
        json.dump(launch_config, f, indent=4)

    # Ensure global VSCode settings exist but without yaml.schemas
    os.makedirs(VSCODE_USER, exist_ok=True)
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                settings = {}
    else:
        settings = {}

    # Remove yaml.schemas if somehow present
    settings.pop('yaml.schemas', None)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: Dockerfile, app.py, requirements.txt, .dockerignore, .gitignore')
    print(f'No k8s/ directory, no tasks.json, no yaml.schemas configured')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
