"""
Initial Setup: Set up a compound launch configuration for Flask backend + Chrome frontend
Task ID: vscode_stu_092
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_092'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # Create project structure
    os.makedirs(f'{PROJECT_DIR}/backend', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/frontend', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- backend/app.py ---
    app_py_content = '''\
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# Serve static frontend files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'endpoints': ['/api/status', '/api/users', '/api/products']
    })


@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': 'Sarah Chen', 'role': 'admin'},
        {'id': 2, 'name': 'Marcus Johnson', 'role': 'editor'},
        {'id': 3, 'name': 'Priya Patel', 'role': 'viewer'},
        {'id': 4, 'name': 'James Wilson', 'role': 'editor'},
    ]
    return jsonify(users)


@app.route('/api/products')
def get_products():
    products = [
        {'id': 101, 'name': 'Widget Pro', 'price': 29.99, 'stock': 150},
        {'id': 102, 'name': 'Gadget Plus', 'price': 49.99, 'stock': 75},
        {'id': 103, 'name': 'Tool Master', 'price': 19.99, 'stock': 300},
    ]
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    with open(f'{PROJECT_DIR}/backend/app.py', 'w') as f:
        f.write(app_py_content)

    # --- backend/requirements.txt ---
    with open(f'{PROJECT_DIR}/backend/requirements.txt', 'w') as f:
        f.write('flask>=2.3.0\n')

    # --- frontend/index.html ---
    index_html_content = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full-Stack Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4a90d9;
            padding-bottom: 10px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: #4caf50;
            margin-right: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: left;
            padding: 8px 12px;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #4a90d9;
            color: white;
        }
        #user-list, #product-list {
            min-height: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Full-Stack Dashboard</h1>

        <div class="card">
            <h2><span class="status-indicator"></span>API Status</h2>
            <p id="api-status">Checking...</p>
        </div>

        <div class="card">
            <h2>Users</h2>
            <table>
                <thead>
                    <tr><th>ID</th><th>Name</th><th>Role</th></tr>
                </thead>
                <tbody id="user-list"></tbody>
            </table>
        </div>

        <div class="card">
            <h2>Products</h2>
            <table>
                <thead>
                    <tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th></tr>
                </thead>
                <tbody id="product-list"></tbody>
            </table>
        </div>
    </div>

    <script>
        async function loadStatus() {
            try {
                const resp = await fetch('/api/status');
                const data = await resp.json();
                document.getElementById('api-status').textContent =
                    `Server ${data.status} - v${data.version}`;
            } catch (e) {
                document.getElementById('api-status').textContent = 'API unreachable';
            }
        }

        async function loadUsers() {
            try {
                const resp = await fetch('/api/users');
                const users = await resp.json();
                const tbody = document.getElementById('user-list');
                tbody.innerHTML = users.map(u =>
                    `<tr><td>${u.id}</td><td>${u.name}</td><td>${u.role}</td></tr>`
                ).join('');
            } catch (e) {
                console.error('Failed to load users:', e);
            }
        }

        async function loadProducts() {
            try {
                const resp = await fetch('/api/products');
                const products = await resp.json();
                const tbody = document.getElementById('product-list');
                tbody.innerHTML = products.map(p =>
                    `<tr><td>${p.id}</td><td>${p.name}</td><td>$${p.price.toFixed(2)}</td><td>${p.stock}</td></tr>`
                ).join('');
            } catch (e) {
                console.error('Failed to load products:', e);
            }
        }

        loadStatus();
        loadUsers();
        loadProducts();
    </script>
</body>
</html>
'''
    with open(f'{PROJECT_DIR}/frontend/index.html', 'w') as f:
        f.write(index_html_content)

    # --- frontend/style.css ---
    with open(f'{PROJECT_DIR}/frontend/style.css', 'w') as f:
        f.write('/* Additional styles can go here */\n')

    # --- .vscode/settings.json (basic workspace settings, NO launch config) ---
    vscode_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True
        }
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # NO launch.json — this is what the agent needs to create
    # Ensure it does NOT exist
    launch_json_path = f'{VSCODE_DIR}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  backend/app.py')
    print(f'  frontend/index.html')
    print(f'  .vscode/settings.json')
    print(f'  No launch.json (task is to create it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
