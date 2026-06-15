"""
Initial Setup: Install Python Test Explorer extension and configure CodeLens
Task ID: vscode_py_035
Domain: vscode

Creates a Python project with pytest test files. The Python extension is
installed but pytest testing is NOT enabled, so no CodeLens annotations appear.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_035'
WORKSPACE = os.path.join(WORKDIR, 'workspace')
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


def create_project():
    """Create a realistic Python project with pytest test files."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # Main application module: inventory tracker
    src_dir = os.path.join(WORKSPACE, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # __init__.py
    with open(os.path.join(src_dir, '__init__.py'), 'w') as f:
        f.write('')

    # inventory.py - main module
    with open(os.path.join(src_dir, 'inventory.py'), 'w') as f:
        f.write('''\
"""Inventory management module for a small retail store."""


class Product:
    """Represents a product in the inventory."""

    def __init__(self, sku: str, name: str, price: float, quantity: int = 0):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    def restock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self.quantity += amount

    def sell(self, amount: int) -> float:
        if amount <= 0:
            raise ValueError("Sell amount must be positive")
        if amount > self.quantity:
            raise ValueError(f"Insufficient stock: {self.quantity} available")
        self.quantity -= amount
        return self.price * amount

    def __repr__(self) -> str:
        return f"Product(sku={self.sku!r}, name={self.name!r}, price={self.price}, qty={self.quantity})"


class Inventory:
    """Manages a collection of products."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.sku in self._products:
            raise KeyError(f"Product with SKU {product.sku!r} already exists")
        self._products[product.sku] = product

    def remove_product(self, sku: str) -> Product:
        if sku not in self._products:
            raise KeyError(f"Product with SKU {sku!r} not found")
        return self._products.pop(sku)

    def get_product(self, sku: str) -> Product:
        if sku not in self._products:
            raise KeyError(f"Product with SKU {sku!r} not found")
        return self._products[sku]

    def total_inventory_value(self) -> float:
        return sum(p.total_value for p in self._products.values())

    def low_stock_products(self, threshold: int = 5) -> list[Product]:
        return [p for p in self._products.values() if p.quantity <= threshold]

    @property
    def product_count(self) -> int:
        return len(self._products)
''')

    # Create tests directory
    tests_dir = os.path.join(WORKSPACE, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    # test_inventory.py
    with open(os.path.join(tests_dir, 'test_inventory.py'), 'w') as f:
        f.write('''\
"""Tests for the inventory management module."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from inventory import Product, Inventory


class TestProduct:
    """Tests for the Product class."""

    def test_create_product(self):
        product = Product("SKU-001", "Wireless Mouse", 29.99, 50)
        assert product.sku == "SKU-001"
        assert product.name == "Wireless Mouse"
        assert product.price == 29.99
        assert product.quantity == 50

    def test_product_total_value(self):
        product = Product("SKU-002", "USB-C Hub", 45.00, 20)
        assert product.total_value == 900.00

    def test_product_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product("SKU-003", "Bad Item", -10.0, 5)

    def test_restock_product(self):
        product = Product("SKU-004", "Mechanical Keyboard", 89.99, 10)
        product.restock(25)
        assert product.quantity == 35

    def test_sell_product(self):
        product = Product("SKU-005", "Monitor Stand", 34.50, 15)
        revenue = product.sell(3)
        assert revenue == 103.50
        assert product.quantity == 12

    def test_sell_insufficient_stock_raises(self):
        product = Product("SKU-006", "Webcam", 59.99, 2)
        with pytest.raises(ValueError, match="Insufficient stock"):
            product.sell(5)


class TestInventory:
    """Tests for the Inventory class."""

    def test_add_and_get_product(self):
        inv = Inventory()
        product = Product("SKU-101", "Laptop Sleeve", 24.99, 40)
        inv.add_product(product)
        retrieved = inv.get_product("SKU-101")
        assert retrieved.name == "Laptop Sleeve"

    def test_remove_product(self):
        inv = Inventory()
        inv.add_product(Product("SKU-102", "Desk Lamp", 42.00, 8))
        removed = inv.remove_product("SKU-102")
        assert removed.name == "Desk Lamp"
        assert inv.product_count == 0

    def test_total_inventory_value(self):
        inv = Inventory()
        inv.add_product(Product("SKU-201", "Notebook", 12.50, 100))
        inv.add_product(Product("SKU-202", "Pen Set", 8.99, 200))
        expected = 12.50 * 100 + 8.99 * 200
        assert inv.total_inventory_value() == expected

    def test_low_stock_products(self):
        inv = Inventory()
        inv.add_product(Product("SKU-301", "Stapler", 15.00, 3))
        inv.add_product(Product("SKU-302", "Paper Ream", 7.50, 50))
        inv.add_product(Product("SKU-303", "Tape Dispenser", 5.25, 1))
        low = inv.low_stock_products(threshold=5)
        assert len(low) == 2
        skus = {p.sku for p in low}
        assert skus == {"SKU-301", "SKU-303"}

    def test_duplicate_sku_raises(self):
        inv = Inventory()
        inv.add_product(Product("SKU-401", "Eraser", 1.50, 200))
        with pytest.raises(KeyError):
            inv.add_product(Product("SKU-401", "Duplicate", 2.00, 10))
''')

    # pytest.ini
    with open(os.path.join(WORKSPACE, 'pytest.ini'), 'w') as f:
        f.write('''\
[pytest]
testpaths = tests
''')

    print(f'Project created at: {WORKSPACE}')


def setup_vscode_settings():
    """Configure VSCode settings - Python extension present but testing NOT enabled."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set Python-related settings but do NOT enable pytest
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "python.defaultInterpreterPath": "/usr/bin/python3",
        # Explicitly do NOT set python.testing.pytestEnabled
        # or set it to false to represent the initial state
        "python.testing.pytestEnabled": False,
        "python.testing.unittestEnabled": False,
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to: {SETTINGS_PATH}')


def install_extensions():
    """Ensure the Python extension is installed."""
    # Install Python extension (includes test explorer functionality)
    subprocess.run(
        ["code", "--install-extension", "ms-python.python", "--force"],
        capture_output=True, text=True
    )
    print('Python extension installed')


def main():
    create_project()
    setup_vscode_settings()
    install_extensions()

    # Open VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
