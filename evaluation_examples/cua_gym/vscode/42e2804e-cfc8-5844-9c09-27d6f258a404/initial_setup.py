"""
Initial Setup: Fix .editorconfig indent_style conflict with VSCode settings
Task ID: vscode_fix_083
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_083'
PROJECT_DIR = f'{WORKDIR}/project'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # --- Create project directory structure ---
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # --- .editorconfig with indent_style = tab (the conflict source) ---
    editorconfig_content = """# EditorConfig helps maintain consistent coding styles
# https://editorconfig.org

root = true

[*]
indent_style = tab
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2
"""
    with open(os.path.join(PROJECT_DIR, '.editorconfig'), 'w') as f:
        f.write(editorconfig_content)

    # --- VSCode settings.json with editor.insertSpaces: true ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    settings.update({
        "editor.insertSpaces": True,
        "editor.tabSize": 4,
        "editor.fontSize": 14,
        "editor.wordWrap": "on",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    # --- Workspace-level .vscode/settings.json ---
    vscode_ws_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_ws_dir, exist_ok=True)
    ws_settings = {
        "editor.insertSpaces": True,
        "editor.tabSize": 4,
        "python.analysis.typeCheckingMode": "basic"
    }
    with open(os.path.join(vscode_ws_dir, 'settings.json'), 'w') as f:
        json.dump(ws_settings, f, indent=4)

    # --- Create realistic project files ---

    # README.md
    readme = """# Inventory Management System

A lightweight inventory tracking application for small businesses.

## Features

- Track product stock levels in real-time
- Generate weekly and monthly sales reports
- Automated reorder notifications when stock falls below threshold
- Multi-warehouse support with transfer tracking

## Getting Started

```bash
pip install -r requirements.txt
python src/main.py
```

## Configuration

Copy `.env.example` to `.env` and update the database connection string.

## License

MIT License - see LICENSE for details.
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # requirements.txt
    requirements = """flask==3.0.2
sqlalchemy==2.0.25
python-dotenv==1.0.1
marshmallow==3.20.2
pytest==8.0.2
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # src/main.py
    main_py = '''"""
Inventory Management System - Main Entry Point
"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
\t"DATABASE_URL", "sqlite:///inventory.db"
)


@app.route("/api/health")
def health_check():
\t"""Return service health status."""
\treturn jsonify({"status": "healthy", "version": "1.2.0"})


@app.route("/api/products")
def list_products():
\t"""List all products in inventory."""
\tfrom models.product import Product

\tproducts = Product.query.all()
\treturn jsonify([p.to_dict() for p in products])


@app.route("/api/warehouses")
def list_warehouses():
\t"""List all warehouse locations."""
\tfrom models.warehouse import Warehouse

\twarehouses = Warehouse.query.all()
\treturn jsonify([w.to_dict() for w in warehouses])


if __name__ == "__main__":
\tapp.run(debug=True, port=5000)
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'main.py'), 'w') as f:
        f.write(main_py)

    # src/models.py
    models_py = '''"""
Database models for inventory management.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
\t"""Represents a product in the inventory system."""

\tid: int
\tname: str
\tsku: str
\tcategory: str
\tunit_price: float
\tstock_quantity: int
\treorder_level: int
\tsupplier_id: int
\tcreated_at: datetime
\tupdated_at: Optional[datetime] = None

\tdef to_dict(self):
\t\treturn {
\t\t\t"id": self.id,
\t\t\t"name": self.name,
\t\t\t"sku": self.sku,
\t\t\t"category": self.category,
\t\t\t"unit_price": self.unit_price,
\t\t\t"stock_quantity": self.stock_quantity,
\t\t\t"reorder_level": self.reorder_level,
\t\t}

\tdef needs_reorder(self) -> bool:
\t\t"""Check if stock is below reorder threshold."""
\t\treturn self.stock_quantity <= self.reorder_level


@dataclass
class Warehouse:
\t"""Represents a warehouse location."""

\tid: int
\tname: str
\taddress: str
\tcapacity: int
\tcurrent_occupancy: int

\tdef to_dict(self):
\t\treturn {
\t\t\t"id": self.id,
\t\t\t"name": self.name,
\t\t\t"address": self.address,
\t\t\t"capacity": self.capacity,
\t\t\t"utilization": round(self.current_occupancy / self.capacity * 100, 1),
\t\t}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models.py'), 'w') as f:
        f.write(models_py)

    # src/config.py
    config_py = '''"""
Application configuration settings.
"""

import os


class Config:
\t"""Base configuration."""

\tSECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
\tSQLALCHEMY_TRACK_MODIFICATIONS = False
\tLOG_LEVEL = "INFO"


class DevelopmentConfig(Config):
\t"""Development configuration."""

\tDEBUG = True
\tSQLALCHEMY_DATABASE_URI = "sqlite:///dev_inventory.db"


class ProductionConfig(Config):
\t"""Production configuration."""

\tDEBUG = False
\tSQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'config.py'), 'w') as f:
        f.write(config_py)

    # tests/test_models.py
    test_py = '''"""
Unit tests for inventory models.
"""

import pytest
from datetime import datetime


def test_product_needs_reorder():
\t"""Product should flag reorder when stock is at or below threshold."""
\tfrom src.models import Product

\tproduct = Product(
\t\tid=1,
\t\tname="Wireless Mouse",
\t\tsku="WM-001",
\t\tcategory="Electronics",
\t\tunit_price=29.99,
\t\tstock_quantity=5,
\t\treorder_level=10,
\t\tsupplier_id=101,
\t\tcreated_at=datetime(2025, 1, 15),
\t)
\tassert product.needs_reorder() is True


def test_product_no_reorder():
\t"""Product should not flag reorder when stock is above threshold."""
\tfrom src.models import Product

\tproduct = Product(
\t\tid=2,
\t\tname="USB-C Cable",
\t\tsku="UC-042",
\t\tcategory="Accessories",
\t\tunit_price=12.50,
\t\tstock_quantity=150,
\t\treorder_level=25,
\t\tsupplier_id=103,
\t\tcreated_at=datetime(2025, 3, 22),
\t)
\tassert product.needs_reorder() is False


def test_warehouse_utilization():
\t"""Warehouse utilization should be calculated correctly."""
\tfrom src.models import Warehouse

\twh = Warehouse(
\t\tid=1,
\t\tname="Downtown Hub",
\t\taddress="742 Evergreen Terrace, Springfield",
\t\tcapacity=1000,
\t\tcurrent_occupancy=680,
\t)
\tresult = wh.to_dict()
\tassert result["utilization"] == 68.0
'''
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_models.py'), 'w') as f:
        f.write(test_py)

    # .gitignore
    gitignore = """__pycache__/
*.pyc
.env
*.db
.vscode/
venv/
dist/
*.egg-info/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # .env.example
    env_example = """DATABASE_URL=sqlite:///inventory.db
SECRET_KEY=your-secret-key-here
LOG_LEVEL=DEBUG
"""
    with open(os.path.join(PROJECT_DIR, '.env.example'), 'w') as f:
        f.write(env_example)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'.editorconfig indent_style = tab (conflict)')
    print(f'VSCode settings editor.insertSpaces = true')

    # Install EditorConfig extension
    try:
        subprocess.run(
            ['code', '--install-extension', 'EditorConfig.EditorConfig'],
            capture_output=True, text=True, timeout=30
        )
        print('EditorConfig extension installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
