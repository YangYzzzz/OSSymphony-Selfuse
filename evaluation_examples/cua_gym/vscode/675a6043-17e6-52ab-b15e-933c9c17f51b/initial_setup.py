"""
Initial Setup: Configure Better Comments extension FIXME tag styling
Task ID: vscode_gf3_024
Domain: vscode

Creates a workspace with Python source files containing FIXME comments,
sets up VSCode with some baseline settings (no better-comments config),
and opens VSCode on the workspace.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_024'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'webapp-project')


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


def load_settings():
    """Load existing settings.json, stripping JSONC comments."""
    import re
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    """Merge updates into existing settings."""
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_project_files():
    """Create a realistic webapp project with FIXME comments."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application file
    app_py = '''\
"""
Flask web application for inventory management.
Handles product tracking, stock levels, and supplier orders.
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory store (replace with database later)
inventory = {}


@app.route("/api/products", methods=["GET"])
def list_products():
    """Return all products in inventory."""
    # FIXME: add pagination support for large inventories
    return jsonify(list(inventory.values()))


@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieve a single product by ID."""
    product = inventory.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/products", methods=["POST"])
def create_product():
    """Add a new product to inventory."""
    data = request.get_json()
    # FIXME: validate required fields before inserting
    product_id = data.get("id", str(len(inventory) + 1))
    data["created_at"] = datetime.utcnow().isoformat()
    inventory[product_id] = data
    return jsonify(data), 201


@app.route("/api/products/<product_id>/restock", methods=["POST"])
def restock_product(product_id):
    """Increase stock quantity for a product."""
    product = inventory.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    quantity = request.get_json().get("quantity", 0)
    product["stock"] = product.get("stock", 0) + quantity
    # FIXME: send notification to warehouse system after restock
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py)

    # Database utility module
    db_utils = '''\
"""
Database utility layer for the inventory management system.
Provides connection pooling and query helpers.
"""

import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")


@contextmanager
def get_connection():
    """Yield a database connection with auto-commit."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create tables if they do not exist."""
    # FIXME: add migration support instead of raw CREATE TABLE
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price REAL,
                stock INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact_email TEXT,
                lead_time_days INTEGER
            )
        """)


def get_all_products():
    """Fetch every product row."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM products").fetchall()


def get_low_stock_products(threshold=10):
    """Return products below the stock threshold."""
    # FIXME: threshold should come from per-category settings
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM products WHERE stock < ?", (threshold,)
        ).fetchall()
'''
    with open(os.path.join(PROJECT_DIR, 'db_utils.py'), 'w') as f:
        f.write(db_utils)

    # Config file
    config_py = '''\
"""
Application configuration constants.
"""

# Server settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# Database
DATABASE_URL = "sqlite:///inventory.db"

# API rate limiting
RATE_LIMIT_PER_MINUTE = 60

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
'''
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write(config_py)


def setup_initial():
    """Set up the initial environment."""
    # 1. Create project files
    create_project_files()
    print(f"Project files created in {PROJECT_DIR}")

    # 2. Set some baseline VSCode settings (NO better-comments config)
    update_settings({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })
    print(f"VSCode settings written to {SETTINGS_PATH}")

    # 3. Verify no better-comments.tags in settings
    settings = load_settings()
    assert "better-comments.tags" not in settings, \
        "Initial settings must NOT contain better-comments.tags"
    print("Verified: no better-comments.tags in initial settings")

    # 4. Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


setup_initial()
