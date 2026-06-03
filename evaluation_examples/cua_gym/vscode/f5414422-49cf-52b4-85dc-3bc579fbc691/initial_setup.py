"""
Initial Setup: Disable Code Lens globally but enable for Python only
Task ID: vscode_prod_020
Domain: vscode

Creates a mixed-language workspace with Python and JavaScript files.
VSCode settings have Code Lens enabled globally (default state).
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
TASK_ID = 'vscode_prod_020'
WORKSPACE_DIR = os.path.join(HOME, 'projects', 'mixed-lang')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
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


def create_workspace_files():
    """Create a realistic mixed-language project."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Python files
    py_main = os.path.join(WORKSPACE_DIR, 'app.py')
    with open(py_main, 'w') as f:
        f.write('''\
"""Flask application for inventory management."""

from flask import Flask, jsonify, request
from models import Product, Warehouse
from services import InventoryService

app = Flask(__name__)
inventory_service = InventoryService()


class ProductController:
    """Handles product-related API endpoints."""

    def __init__(self, service):
        self.service = service

    def get_all_products(self):
        """Return all products in the inventory."""
        products = self.service.list_products()
        return jsonify([p.to_dict() for p in products])

    def get_product(self, product_id):
        """Return a single product by ID."""
        product = self.service.find_product(product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.to_dict())

    def create_product(self):
        """Create a new product entry."""
        data = request.get_json()
        product = self.service.add_product(
            name=data["name"],
            sku=data["sku"],
            price=data["price"],
            quantity=data.get("quantity", 0),
        )
        return jsonify(product.to_dict()), 201


controller = ProductController(inventory_service)


@app.route("/api/products", methods=["GET"])
def list_products():
    return controller.get_all_products()


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    return controller.get_product(product_id)


@app.route("/api/products", methods=["POST"])
def create_product():
    return controller.create_product()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
''')

    py_models = os.path.join(WORKSPACE_DIR, 'models.py')
    with open(py_models, 'w') as f:
        f.write('''\
"""Data models for the inventory system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Represents a product in the inventory."""

    id: int
    name: str
    sku: str
    price: float
    quantity: int = 0
    category: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
        }

    def is_in_stock(self) -> bool:
        return self.quantity > 0


@dataclass
class Warehouse:
    """Represents a warehouse location."""

    id: int
    name: str
    location: str
    capacity: int
    current_load: int = 0

    @property
    def available_space(self) -> int:
        return self.capacity - self.current_load

    def has_capacity(self, amount: int) -> bool:
        return self.available_space >= amount
''')

    py_services = os.path.join(WORKSPACE_DIR, 'services.py')
    with open(py_services, 'w') as f:
        f.write('''\
"""Business logic services for inventory management."""

from typing import List, Optional
from models import Product


class InventoryService:
    """Core service for managing product inventory."""

    def __init__(self):
        self._products: List[Product] = []
        self._next_id = 1

    def add_product(self, name: str, sku: str, price: float,
                    quantity: int = 0, category: str = None) -> Product:
        """Add a new product to the inventory."""
        product = Product(
            id=self._next_id,
            name=name,
            sku=sku,
            price=price,
            quantity=quantity,
            category=category,
        )
        self._products.append(product)
        self._next_id += 1
        return product

    def find_product(self, product_id: int) -> Optional[Product]:
        """Find a product by its ID."""
        for product in self._products:
            if product.id == product_id:
                return product
        return None

    def list_products(self) -> List[Product]:
        """Return all products."""
        return list(self._products)

    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update stock quantity for a product."""
        product = self.find_product(product_id)
        if product is None:
            return False
        new_quantity = product.quantity + quantity_change
        if new_quantity < 0:
            return False
        product.quantity = new_quantity
        return True

    def get_low_stock(self, threshold: int = 5) -> List[Product]:
        """Get products with stock below the threshold."""
        return [p for p in self._products if p.quantity <= threshold]
''')

    py_tests = os.path.join(WORKSPACE_DIR, 'test_services.py')
    with open(py_tests, 'w') as f:
        f.write('''\
"""Tests for inventory services."""

import unittest
from services import InventoryService


class TestInventoryService(unittest.TestCase):
    """Test cases for InventoryService."""

    def setUp(self):
        self.service = InventoryService()
        self.service.add_product("Widget A", "WGT-001", 9.99, quantity=50)
        self.service.add_product("Gadget B", "GDG-002", 24.99, quantity=3)

    def test_add_product(self):
        product = self.service.add_product("Gizmo C", "GZM-003", 14.50)
        self.assertEqual(product.name, "Gizmo C")
        self.assertEqual(product.sku, "GZM-003")
        self.assertEqual(product.quantity, 0)

    def test_find_product(self):
        product = self.service.find_product(1)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Widget A")

    def test_find_product_not_found(self):
        product = self.service.find_product(999)
        self.assertIsNone(product)

    def test_update_stock(self):
        self.assertTrue(self.service.update_stock(1, -10))
        product = self.service.find_product(1)
        self.assertEqual(product.quantity, 40)

    def test_update_stock_negative_rejected(self):
        self.assertFalse(self.service.update_stock(2, -100))

    def test_get_low_stock(self):
        low = self.service.get_low_stock(threshold=5)
        self.assertEqual(len(low), 1)
        self.assertEqual(low[0].name, "Gadget B")


if __name__ == "__main__":
    unittest.main()
''')

    # JavaScript files
    js_main = os.path.join(WORKSPACE_DIR, 'index.js')
    with open(js_main, 'w') as f:
        f.write('''\
/**
 * Express server for the inventory management dashboard.
 */

const express = require("express");
const cors = require("cors");
const { connectDatabase } = require("./db");
const productRoutes = require("./routes/products");
const dashboardRoutes = require("./routes/dashboard");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use("/api/products", productRoutes);
app.use("/api/dashboard", dashboardRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

async function startServer() {
  try {
    await connectDatabase();
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
}

startServer();

module.exports = app;
''')

    js_utils = os.path.join(WORKSPACE_DIR, 'utils.js')
    with open(js_utils, 'w') as f:
        f.write('''\
/**
 * Utility functions for the inventory dashboard.
 */

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

function calculateTotalValue(products) {
  return products.reduce((sum, p) => sum + p.price * p.quantity, 0);
}

function groupByCategory(products) {
  return products.reduce((groups, product) => {
    const category = product.category || "Uncategorized";
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(product);
    return groups;
  }, {});
}

function paginate(items, page = 1, perPage = 20) {
  const start = (page - 1) * perPage;
  const end = start + perPage;
  return {
    data: items.slice(start, end),
    total: items.length,
    page,
    perPage,
    totalPages: Math.ceil(items.length / perPage),
  };
}

module.exports = {
  formatCurrency,
  calculateTotalValue,
  groupByCategory,
  paginate,
};
''')

    # Package file
    pkg = os.path.join(WORKSPACE_DIR, 'package.json')
    with open(pkg, 'w') as f:
        json.dump({
            "name": "inventory-dashboard",
            "version": "1.0.0",
            "description": "Inventory management dashboard backend",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "nodemon index.js",
                "test": "jest"
            },
            "dependencies": {
                "cors": "^2.8.5",
                "express": "^4.18.2"
            }
        }, f, indent=2)

    print(f'Workspace files created in {WORKSPACE_DIR}')


def setup_vscode_settings():
    """Set up VSCode settings with Code Lens enabled globally (default)."""
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)

    # Load existing settings or start empty
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure Code Lens is enabled globally (this is the default,
    # but set it explicitly so the user can see it in settings)
    settings["editor.codeLens"] = True
    settings.setdefault("workbench.colorTheme", "Default Dark Modern")
    settings.setdefault("editor.fontSize", 14)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to {SETTINGS_PATH}')
    print(f'  editor.codeLens = true (globally enabled)')


def main():
    create_workspace_files()
    setup_vscode_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
