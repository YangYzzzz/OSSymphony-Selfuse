"""
Initial Setup: Set up a Python project with pytest test files and a basic VSCode debug config.
Task ID: vscode_py_044
Domain: vscode (libreoffice_calc mapped to vscode task)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_044'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
TESTS_DIR = f'{PROJECT_DIR}/tests'


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
    # Create project directories
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # --- pytest.ini for marker registration ---
    pytest_ini = """[pytest]
markers =
    unit: Unit tests that run quickly without external dependencies
    integration: Integration tests that verify component interactions
    slow: Tests that take a long time to complete
"""
    with open(f'{PROJECT_DIR}/pytest.ini', 'w') as f:
        f.write(pytest_ini)

    # --- conftest.py at project root ---
    conftest_content = """import pytest


@pytest.fixture
def db_connection():
    \"\"\"Simulated database connection for integration tests.\"\"\"
    conn = {"host": "localhost", "port": 5432, "db": "inventory_test"}
    yield conn


@pytest.fixture
def sample_products():
    \"\"\"Sample product data for testing.\"\"\"
    return [
        {"id": 1, "name": "Wireless Mouse", "price": 29.99, "stock": 150},
        {"id": 2, "name": "Mechanical Keyboard", "price": 89.50, "stock": 75},
        {"id": 3, "name": "USB-C Hub", "price": 45.00, "stock": 200},
        {"id": 4, "name": "Monitor Stand", "price": 34.99, "stock": 60},
    ]
"""
    with open(f'{PROJECT_DIR}/conftest.py', 'w') as f:
        f.write(conftest_content)

    # --- Main application module ---
    app_content = '''"""
Inventory Management System - Core Module
"""


class InventoryManager:
    """Manages product inventory with CRUD operations."""

    def __init__(self):
        self._products = {}

    def add_product(self, product_id: int, name: str, price: float, stock: int):
        if product_id in self._products:
            raise ValueError(f"Product {product_id} already exists")
        self._products[product_id] = {
            "name": name,
            "price": price,
            "stock": stock,
        }

    def get_product(self, product_id: int) -> dict:
        if product_id not in self._products:
            raise KeyError(f"Product {product_id} not found")
        return self._products[product_id]

    def update_stock(self, product_id: int, quantity: int):
        product = self.get_product(product_id)
        new_stock = product["stock"] + quantity
        if new_stock < 0:
            raise ValueError("Stock cannot go below zero")
        product["stock"] = new_stock

    def total_inventory_value(self) -> float:
        return sum(
            p["price"] * p["stock"] for p in self._products.values()
        )

    def low_stock_products(self, threshold: int = 10) -> list:
        return [
            {"id": pid, **pdata}
            for pid, pdata in self._products.items()
            if pdata["stock"] < threshold
        ]
'''
    with open(f'{PROJECT_DIR}/inventory.py', 'w') as f:
        f.write(app_content)

    # --- tests/__init__.py ---
    with open(f'{TESTS_DIR}/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_unit.py - Unit tests ---
    test_unit = '''"""Unit tests for InventoryManager core operations."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import InventoryManager


@pytest.mark.unit
class TestAddProduct:
    def test_add_single_product(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Wireless Mouse", 29.99, 150)
        product = mgr.get_product(1)
        assert product["name"] == "Wireless Mouse"
        assert product["price"] == 29.99

    def test_add_duplicate_raises(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Wireless Mouse", 29.99, 150)
        with pytest.raises(ValueError, match="already exists"):
            mgr.add_product(1, "Another Mouse", 19.99, 50)

    def test_add_multiple_products(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Mouse", 29.99, 100)
        mgr.add_product(2, "Keyboard", 89.50, 75)
        mgr.add_product(3, "Hub", 45.00, 200)
        assert mgr.get_product(1)["name"] == "Mouse"
        assert mgr.get_product(2)["name"] == "Keyboard"
        assert mgr.get_product(3)["name"] == "Hub"


@pytest.mark.unit
class TestUpdateStock:
    def test_increase_stock(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Monitor Stand", 34.99, 60)
        mgr.update_stock(1, 40)
        assert mgr.get_product(1)["stock"] == 100

    def test_decrease_stock(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Monitor Stand", 34.99, 60)
        mgr.update_stock(1, -20)
        assert mgr.get_product(1)["stock"] == 40

    def test_negative_stock_raises(self):
        mgr = InventoryManager()
        mgr.add_product(1, "Monitor Stand", 34.99, 10)
        with pytest.raises(ValueError, match="cannot go below zero"):
            mgr.update_stock(1, -15)


@pytest.mark.unit
def test_get_nonexistent_product():
    mgr = InventoryManager()
    with pytest.raises(KeyError, match="not found"):
        mgr.get_product(999)
'''
    with open(f'{TESTS_DIR}/test_unit.py', 'w') as f:
        f.write(test_unit)

    # --- tests/test_integration.py - Integration tests ---
    test_integration = '''"""Integration tests for inventory system component interactions."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import InventoryManager


@pytest.mark.integration
class TestInventoryWorkflow:
    def test_full_product_lifecycle(self, sample_products):
        mgr = InventoryManager()
        for p in sample_products:
            mgr.add_product(p["id"], p["name"], p["price"], p["stock"])

        # Verify all products added
        for p in sample_products:
            stored = mgr.get_product(p["id"])
            assert stored["name"] == p["name"]
            assert stored["price"] == p["price"]

    def test_stock_adjustments_across_products(self, sample_products):
        mgr = InventoryManager()
        for p in sample_products:
            mgr.add_product(p["id"], p["name"], p["price"], p["stock"])

        mgr.update_stock(1, -50)   # Mouse: 150 -> 100
        mgr.update_stock(2, 25)    # Keyboard: 75 -> 100
        mgr.update_stock(3, -180)  # Hub: 200 -> 20

        assert mgr.get_product(1)["stock"] == 100
        assert mgr.get_product(2)["stock"] == 100
        assert mgr.get_product(3)["stock"] == 20

    def test_inventory_value_after_changes(self, sample_products):
        mgr = InventoryManager()
        for p in sample_products:
            mgr.add_product(p["id"], p["name"], p["price"], p["stock"])

        initial_value = mgr.total_inventory_value()
        mgr.update_stock(1, -100)  # Remove significant stock
        new_value = mgr.total_inventory_value()
        assert new_value < initial_value


@pytest.mark.integration
def test_low_stock_detection(sample_products):
    mgr = InventoryManager()
    for p in sample_products:
        mgr.add_product(p["id"], p["name"], p["price"], p["stock"])

    # Deplete stock on two products
    mgr.update_stock(1, -145)  # Mouse: 150 -> 5
    mgr.update_stock(4, -55)   # Stand: 60 -> 5

    low = mgr.low_stock_products(threshold=10)
    low_ids = [p["id"] for p in low]
    assert 1 in low_ids
    assert 4 in low_ids
    assert len(low) == 2
'''
    with open(f'{TESTS_DIR}/test_integration.py', 'w') as f:
        f.write(test_integration)

    # --- tests/test_slow.py - Slow tests ---
    test_slow = '''"""Slow performance and stress tests."""
import pytest
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory import InventoryManager


@pytest.mark.slow
def test_bulk_product_insertion():
    mgr = InventoryManager()
    for i in range(500):
        mgr.add_product(i, f"Product_{i:04d}", round(10.0 + i * 0.5, 2), 100)
    assert mgr.total_inventory_value() > 0


@pytest.mark.slow
def test_repeated_stock_updates():
    mgr = InventoryManager()
    mgr.add_product(1, "Stress Test Item", 9.99, 10000)
    for _ in range(1000):
        mgr.update_stock(1, -1)
    assert mgr.get_product(1)["stock"] == 9000


@pytest.mark.slow
def test_large_inventory_value_calculation():
    mgr = InventoryManager()
    for i in range(1, 201):
        mgr.add_product(i, f"Item_{i}", float(i) * 1.5, i * 10)
    value = mgr.total_inventory_value()
    assert value > 0
'''
    with open(f'{TESTS_DIR}/test_slow.py', 'w') as f:
        f.write(test_slow)

    # --- .vscode/launch.json - Basic Python debug config only ---
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": True
            }
        ]
    }
    with open(f'{VSCODE_DIR}/launch.json', 'w') as f:
        json.dump(launch_config, f, indent=4)

    # --- .vscode/settings.json - Basic Python settings ---
    vscode_settings = {
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": [
            "tests"
        ],
        "editor.formatOnSave": True,
        "python.analysis.typeCheckingMode": "basic"
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json: {VSCODE_DIR}/launch.json')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
