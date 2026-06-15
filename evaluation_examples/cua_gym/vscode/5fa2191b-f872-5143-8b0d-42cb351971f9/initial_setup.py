"""
Initial Setup: Fix Flask debug launch configuration
Task ID: vscode_fix_052
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_052'
PROJECT_DIR = os.path.join(WORKDIR, 'flask-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    templates_dir = os.path.join(PROJECT_DIR, 'templates')
    static_dir = os.path.join(PROJECT_DIR, 'static', 'css')
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    # --- app.py: Main Flask application ---
    app_py = '''\
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# In-memory product catalog
products = [
    {"id": 1, "name": "Wireless Keyboard", "price": 49.99, "category": "Electronics", "stock": 120},
    {"id": 2, "name": "Ergonomic Mouse", "price": 34.50, "category": "Electronics", "stock": 85},
    {"id": 3, "name": "USB-C Hub", "price": 27.99, "category": "Accessories", "stock": 200},
    {"id": 4, "name": "Monitor Stand", "price": 65.00, "category": "Furniture", "stock": 45},
    {"id": 5, "name": "Desk Lamp", "price": 39.95, "category": "Furniture", "stock": 60},
    {"id": 6, "name": "Webcam HD", "price": 79.99, "category": "Electronics", "stock": 33},
    {"id": 7, "name": "Laptop Sleeve", "price": 22.00, "category": "Accessories", "stock": 150},
    {"id": 8, "name": "Cable Organizer", "price": 12.99, "category": "Accessories", "stock": 300},
]


@app.route("/")
def index():
    return render_template("index.html", products=products)


@app.route("/api/products")
def api_products():
    category = request.args.get("category")
    if category:
        filtered = [p for p in products if p["category"].lower() == category.lower()]
        return jsonify(filtered)
    return jsonify(products)


@app.route("/api/products/<int:product_id>")
def api_product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/stats")
def api_stats():
    total_value = sum(p["price"] * p["stock"] for p in products)
    categories = {}
    for p in products:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    return jsonify({
        "total_products": len(products),
        "total_inventory_value": round(total_value, 2),
        "categories": categories,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py)

    # --- requirements.txt ---
    requirements = 'flask==3.0.0\nWerkzeug==3.0.1\nJinja2==3.1.2\n'
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # --- templates/index.html ---
    index_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Product Catalog</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Product Catalog</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Category</th>
                <th>Stock</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>${{ "%.2f"|format(product.price) }}</td>
                <td>{{ product.category }}</td>
                <td>{{ product.stock }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(index_html)

    # --- static/css/style.css ---
    style_css = '''\
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 2rem;
    background-color: #f5f5f5;
}
h1 {
    color: #333;
}
table {
    border-collapse: collapse;
    width: 100%;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
th {
    background-color: #4a90d9;
    color: white;
}
tr:hover {
    background-color: #f0f7ff;
}
'''
    with open(os.path.join(static_dir, 'style.css'), 'w') as f:
        f.write(style_css)

    # --- .vscode/launch.json: BROKEN Flask config (missing FLASK_APP env, missing jinja) ---
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask",
                "type": "debugpy",
                "request": "launch",
                "module": "flask",
                "args": [
                    "run",
                    "--no-debugger",
                    "--no-reload",
                    "--port", "5001"
                ],
                "env": {
                    "FLASK_DEBUG": "1"
                },
                "justMyCode": True
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'launch.json'), 'w') as f:
        json.dump(launch_json, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json (broken): {os.path.join(VSCODE_DIR, "launch.json")}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
