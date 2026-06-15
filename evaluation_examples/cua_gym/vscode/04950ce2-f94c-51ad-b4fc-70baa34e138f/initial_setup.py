"""
Initial Setup: Set up search.exclude settings to prevent VSCode search from
returning results in build output, coverage reports, and generated documentation.
Task ID: vscode_lp_070
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_070'
PROJECT_DIR = f'{WORKDIR}/workspace'

# VSCode config paths
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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


def create_project_structure():
    """Create a realistic project with source, build, coverage, and docs dirs."""

    # --- src/ directory (actual source code) ---
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, 'app.py'), 'w') as f:
        f.write('''"""Main application module for inventory management system."""

import logging
from datetime import datetime
from typing import List, Optional

from .models import Product, Order
from .database import DatabaseConnection

logger = logging.getLogger(__name__)


class InventoryManager:
    """Manages product inventory and order processing."""

    def __init__(self, db_url: str):
        self.db = DatabaseConnection(db_url)
        self.cache = {}
        logger.info("InventoryManager initialized with db: %s", db_url)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by its ID."""
        if product_id in self.cache:
            return self.cache[product_id]
        product = self.db.query_product(product_id)
        if product:
            self.cache[product_id] = product
        return product

    def process_order(self, order: Order) -> bool:
        """Process an incoming order, updating stock levels."""
        for item in order.items:
            product = self.get_product(item.product_id)
            if not product or product.stock < item.quantity:
                logger.warning("Insufficient stock for product %s", item.product_id)
                return False
            product.stock -= item.quantity
            self.db.update_product(product)
        order.processed_at = datetime.now()
        self.db.save_order(order)
        logger.info("Order %s processed successfully", order.order_id)
        return True

    def restock(self, product_id: str, quantity: int) -> None:
        """Add stock to an existing product."""
        product = self.get_product(product_id)
        if product:
            product.stock += quantity
            self.db.update_product(product)
            logger.info("Restocked %s: +%d units", product_id, quantity)
''')

    with open(os.path.join(src_dir, 'models.py'), 'w') as f:
        f.write('''"""Data models for the inventory system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Product:
    product_id: str
    name: str
    category: str
    price: float
    stock: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: datetime = None
    total: float = 0.0

    def calculate_total(self) -> float:
        self.total = sum(item.quantity * item.unit_price for item in self.items)
        return self.total
''')

    with open(os.path.join(src_dir, 'database.py'), 'w') as f:
        f.write('''"""Database connection and query utilities."""

import sqlite3
import logging
from typing import Optional

from .models import Product, Order

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """SQLite-based database connection for inventory data."""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = sqlite3.connect(db_url)
        self._initialize_tables()

    def _initialize_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price REAL,
                stock INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                total REAL,
                processed_at TEXT
            )
        """)
        self.conn.commit()

    def query_product(self, product_id: str) -> Optional[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(*row)
        return None

    def update_product(self, product: Product):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE products SET stock = ?, price = ? WHERE product_id = ?",
            (product.stock, product.price, product.product_id)
        )
        self.conn.commit()

    def save_order(self, order: Order):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, total, processed_at) VALUES (?, ?, ?, ?)",
            (order.order_id, order.customer_id, order.total,
             order.processed_at.isoformat() if order.processed_at else None)
        )
        self.conn.commit()
''')

    with open(os.path.join(src_dir, '__init__.py'), 'w') as f:
        f.write('"""Inventory management system."""\n')

    # --- tests/ directory ---
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, 'test_app.py'), 'w') as f:
        f.write('''"""Unit tests for the inventory manager."""

import unittest
from unittest.mock import MagicMock
from src.app import InventoryManager
from src.models import Product, Order, OrderItem


class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.manager = InventoryManager(":memory:")

    def test_process_order_success(self):
        product = Product("P001", "Widget A", "Hardware", 29.99, 100)
        self.manager.cache["P001"] = product
        order = Order("ORD001", "C001", [OrderItem("P001", 5, 29.99)])
        result = self.manager.process_order(order)
        self.assertTrue(result)
        self.assertEqual(product.stock, 95)

    def test_process_order_insufficient_stock(self):
        product = Product("P002", "Gadget B", "Electronics", 149.99, 2)
        self.manager.cache["P002"] = product
        order = Order("ORD002", "C002", [OrderItem("P002", 10, 149.99)])
        result = self.manager.process_order(order)
        self.assertFalse(result)

    def test_restock(self):
        product = Product("P003", "Tool C", "Hardware", 45.00, 50)
        self.manager.cache["P003"] = product
        self.manager.db.update_product = MagicMock()
        self.manager.restock("P003", 25)
        self.assertEqual(product.stock, 75)


if __name__ == "__main__":
    unittest.main()
''')

    # --- dist/ directory (build output - should be excluded from search) ---
    dist_dir = os.path.join(PROJECT_DIR, 'dist')
    os.makedirs(dist_dir, exist_ok=True)

    with open(os.path.join(dist_dir, 'bundle.js'), 'w') as f:
        f.write('''// Auto-generated build output - DO NOT EDIT
// Generated at 2025-11-15T08:32:14Z
!function(e,t){"use strict";var n=function(){function Product(e,t,n,r,i){this.product_id=e;
this.name=t;this.category=n;this.price=r;this.stock=i}return Product}();
var o=function(){function InventoryManager(e){this.db=new DatabaseConnection(e);
this.cache={};console.log("InventoryManager initialized")}
InventoryManager.prototype.get_product=function(e){if(e in this.cache)return this.cache[e];
var t=this.db.query_product(e);if(t)this.cache[e]=t;return t};
InventoryManager.prototype.process_order=function(e){for(var t=0;t<e.items.length;t++){
var n=this.get_product(e.items[t].product_id);if(!n||n.stock<e.items[t].quantity)
return console.warn("Insufficient stock"),!1;n.stock-=e.items[t].quantity;
this.db.update_product(n)}return e.processed_at=new Date,this.db.save_order(e),!0};
return InventoryManager}();e.InventoryManager=o;e.Product=n}(this.inventory=this.inventory||{});
''')

    with open(os.path.join(dist_dir, 'bundle.min.css'), 'w') as f:
        f.write('''/* Minified CSS - auto-generated */
.inventory-app{font-family:Inter,Helvetica,Arial,sans-serif;max-width:1200px;margin:0 auto}
.product-card{border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin:8px}
.product-card .name{font-size:18px;font-weight:600;color:#1a202c}
.product-card .price{font-size:24px;color:#2d7d46;font-weight:700}
.product-card .stock{font-size:14px;color:#718096}
.order-table{width:100%;border-collapse:collapse}.order-table th{background:#4a5568;color:#fff;padding:12px}
.order-table td{padding:10px;border-bottom:1px solid #e2e8f0}
''')

    # --- coverage/ directory (test coverage reports) ---
    coverage_dir = os.path.join(PROJECT_DIR, 'coverage')
    os.makedirs(coverage_dir, exist_ok=True)

    with open(os.path.join(coverage_dir, 'index.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html><head><title>Coverage Report - inventory system</title>
<style>body{font-family:sans-serif}table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ddd;padding:8px}th{background:#4a5568;color:#fff}
.high{color:#2d7d46}.medium{color:#d69e2e}.low{color:#e53e3e}</style></head>
<body><h1>Coverage Report</h1>
<p>Generated: 2025-11-15 08:35:22</p>
<table><tr><th>Module</th><th>Statements</th><th>Missing</th><th>Coverage</th></tr>
<tr><td>src/app.py</td><td>45</td><td>3</td><td class="high">93%</td></tr>
<tr><td>src/models.py</td><td>28</td><td>0</td><td class="high">100%</td></tr>
<tr><td>src/database.py</td><td>52</td><td>8</td><td class="medium">85%</td></tr>
<tr><td><strong>TOTAL</strong></td><td><strong>125</strong></td><td><strong>11</strong></td>
<td class="high"><strong>91%</strong></td></tr></table></body></html>
''')

    with open(os.path.join(coverage_dir, 'coverage.json'), 'w') as f:
        json.dump({
            "meta": {"version": "7.3.2", "timestamp": "2025-11-15T08:35:22"},
            "totals": {"covered_lines": 114, "num_statements": 125,
                       "percent_covered": 91.2, "missing_lines": 11},
            "files": {
                "src/app.py": {"covered_lines": 42, "num_statements": 45,
                               "percent_covered": 93.3},
                "src/models.py": {"covered_lines": 28, "num_statements": 28,
                                  "percent_covered": 100.0},
                "src/database.py": {"covered_lines": 44, "num_statements": 52,
                                    "percent_covered": 84.6}
            }
        }, f, indent=2)

    # --- docs/generated/ directory (auto-generated documentation) ---
    docs_gen_dir = os.path.join(PROJECT_DIR, 'docs', 'generated')
    os.makedirs(docs_gen_dir, exist_ok=True)

    with open(os.path.join(docs_gen_dir, 'api_reference.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html><head><title>API Reference - Inventory System</title></head>
<body><h1>API Reference</h1>
<h2>class InventoryManager</h2>
<p>Manages product inventory and order processing.</p>
<h3>Methods</h3>
<dl>
<dt><code>get_product(product_id: str) -> Optional[Product]</code></dt>
<dd>Retrieve a product by its ID. Returns cached version if available.</dd>
<dt><code>process_order(order: Order) -> bool</code></dt>
<dd>Process an incoming order, updating stock levels. Returns True on success.</dd>
<dt><code>restock(product_id: str, quantity: int) -> None</code></dt>
<dd>Add stock to an existing product.</dd>
</dl>
<h2>class Product</h2>
<p>Data model representing a product in the inventory.</p>
<h3>Attributes</h3>
<ul>
<li><code>product_id</code> (str): Unique identifier</li>
<li><code>name</code> (str): Product display name</li>
<li><code>category</code> (str): Product category</li>
<li><code>price</code> (float): Unit price</li>
<li><code>stock</code> (int): Current stock level</li>
</ul></body></html>
''')

    with open(os.path.join(docs_gen_dir, 'models.md'), 'w') as f:
        f.write('''# Models Reference

Auto-generated from source docstrings.

## Product
| Field | Type | Description |
|-------|------|-------------|
| product_id | str | Unique identifier |
| name | str | Product display name |
| category | str | Product category |
| price | float | Unit price in USD |
| stock | int | Current stock quantity |

## OrderItem
| Field | Type | Description |
|-------|------|-------------|
| product_id | str | Reference to product |
| quantity | int | Number of units |
| unit_price | float | Price per unit at time of order |

## Order
| Field | Type | Description |
|-------|------|-------------|
| order_id | str | Unique order identifier |
| customer_id | str | Customer reference |
| items | List[OrderItem] | Line items in the order |
| total | float | Computed total amount |
''')

    # --- docs/ (non-generated, hand-written docs) ---
    with open(os.path.join(PROJECT_DIR, 'docs', 'README.md'), 'w') as f:
        f.write('''# Inventory Management System

## Overview
A lightweight inventory management system built with Python and SQLite.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python -m src.app`
3. Run tests: `python -m pytest tests/`

## Architecture
- `src/app.py` - Main application logic (InventoryManager)
- `src/models.py` - Data models (Product, Order, OrderItem)
- `src/database.py` - Database abstraction layer
''')

    # --- config files at project root ---
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('sqlite3\npytest>=7.0\npytest-cov>=4.0\nblack>=23.0\nmypy>=1.0\n')

    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[project]
name = "inventory-system"
version = "1.2.0"
description = "Lightweight inventory management system"
requires-python = ">=3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=html:coverage"

[tool.black]
line-length = 100
target-version = ["py39"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
''')

    print(f"Project structure created at {PROJECT_DIR}")


def setup_vscode_settings():
    """Ensure VSCode settings exist but do NOT include search.exclude."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove search.exclude if it exists (initial state must NOT have it)
    settings.pop("search.exclude", None)

    # Add some reasonable default settings (but NOT search.exclude)
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "editor.minimap.enabled": True,
        "editor.renderWhitespace": "selection",
        "terminal.integrated.fontSize": 13
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings written to {SETTINGS_PATH} (no search.exclude)")


def main():
    create_project_structure()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
