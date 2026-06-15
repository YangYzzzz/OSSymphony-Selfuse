"""
Initial Setup: VSCode tasks.json with broken compound task dependency
Task ID: vscode_fix_047
Domain: vscode

Creates a project with a tasks.json where:
- 'build' task has isBackground: true but NO proper problemMatcher endPattern
- 'test' task depends on 'build' but never starts because VSCode thinks build runs forever
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_047'
PROJECT_DIR = f'{WORKDIR}/project'
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
    # Create project directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- Create realistic source files ---

    # Main application file
    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write('''\
"""Inventory Management System - Main Application"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: float
    quantity: int
    last_restocked: datetime


class InventoryManager:
    def __init__(self):
        self.products: List[Product] = []
        self._load_initial_stock()

    def _load_initial_stock(self):
        self.products = [
            Product("SKU-001", "Wireless Mouse", "Electronics", 29.99, 150, datetime(2025, 3, 10)),
            Product("SKU-002", "USB-C Hub", "Electronics", 45.50, 75, datetime(2025, 2, 28)),
            Product("SKU-003", "Standing Desk Mat", "Office", 34.00, 200, datetime(2025, 3, 1)),
            Product("SKU-004", "Mechanical Keyboard", "Electronics", 89.99, 50, datetime(2025, 1, 15)),
            Product("SKU-005", "Monitor Light Bar", "Accessories", 55.00, 120, datetime(2025, 3, 5)),
        ]

    def add_product(self, product: Product) -> bool:
        if any(p.sku == product.sku for p in self.products):
            return False
        self.products.append(product)
        return True

    def get_by_category(self, category: str) -> List[Product]:
        return [p for p in self.products if p.category == category]

    def get_low_stock(self, threshold: int = 60) -> List[Product]:
        return [p for p in self.products if p.quantity < threshold]

    def total_inventory_value(self) -> float:
        return sum(p.price * p.quantity for p in self.products)


if __name__ == "__main__":
    mgr = InventoryManager()
    print(f"Total inventory value: ${mgr.total_inventory_value():,.2f}")
    low = mgr.get_low_stock()
    if low:
        print("Low stock items:")
        for p in low:
            print(f"  {p.name} ({p.sku}): {p.quantity} remaining")
    print("Build completed successfully.")
''')

    # Build script
    with open(f'{PROJECT_DIR}/build.sh', 'w') as f:
        f.write('''\
#!/bin/bash
echo "Starting build process..."
echo "Compiling inventory module..."
python3 -c "import py_compile; py_compile.compile('src/app.py')"
echo "Build completed successfully."
''')
    os.chmod(f'{PROJECT_DIR}/build.sh', 0o755)

    # Test file
    with open(f'{PROJECT_DIR}/tests/test_inventory.py', 'w') as f:
        f.write('''\
"""Unit tests for Inventory Management System"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import InventoryManager, Product
from datetime import datetime


def test_initial_stock_count():
    mgr = InventoryManager()
    assert len(mgr.products) == 5, f"Expected 5 products, got {len(mgr.products)}"
    print("PASS: test_initial_stock_count")


def test_add_product():
    mgr = InventoryManager()
    new_product = Product("SKU-100", "Webcam", "Electronics", 79.99, 30, datetime(2025, 3, 12))
    assert mgr.add_product(new_product) is True
    assert len(mgr.products) == 6
    # Duplicate should fail
    assert mgr.add_product(new_product) is False
    print("PASS: test_add_product")


def test_get_by_category():
    mgr = InventoryManager()
    electronics = mgr.get_by_category("Electronics")
    assert len(electronics) == 3
    print("PASS: test_get_by_category")


def test_low_stock():
    mgr = InventoryManager()
    low = mgr.get_low_stock(threshold=100)
    assert len(low) == 2, f"Expected 2 low-stock items, got {len(low)}"
    print("PASS: test_low_stock")


def test_total_value():
    mgr = InventoryManager()
    value = mgr.total_inventory_value()
    assert value > 0, "Total value should be positive"
    print("PASS: test_total_value")


if __name__ == "__main__":
    test_initial_stock_count()
    test_add_product()
    test_get_by_category()
    test_low_stock()
    test_total_value()
    print("\\nAll tests passed!")
''')

    # Run test script
    with open(f'{PROJECT_DIR}/run_tests.sh', 'w') as f:
        f.write('''\
#!/bin/bash
echo "Running test suite..."
cd "$(dirname "$0")"
python3 tests/test_inventory.py
echo "Test suite completed."
''')
    os.chmod(f'{PROJECT_DIR}/run_tests.sh', 0o755)

    # --- Create the BROKEN tasks.json ---
    # The build task has isBackground: true but the problemMatcher has NO
    # background section (no begPattern/endPattern). VSCode sees the build
    # task as running indefinitely, so 'test' (which dependsOn build) never starts.
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "build",
                "type": "shell",
                "command": "./build.sh",
                "isBackground": True,
                "problemMatcher": {
                    "owner": "custom",
                    "pattern": {
                        "regexp": "^(.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
                        "file": 1,
                        "line": 2,
                        "column": 3,
                        "severity": 4,
                        "message": 5
                    }
                },
                "group": {
                    "kind": "build",
                    "isDefault": True
                }
            },
            {
                "label": "test",
                "type": "shell",
                "command": "./run_tests.sh",
                "dependsOn": ["build"],
                "problemMatcher": [],
                "group": "test"
            },
            {
                "label": "build and test",
                "dependsOn": ["build", "test"],
                "dependsOrder": "sequence",
                "problemMatcher": [],
                "group": "none"
            }
        ]
    }

    with open(f'{VSCODE_DIR}/tasks.json', 'w') as f:
        json.dump(tasks_config, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'tasks.json created at: {VSCODE_DIR}/tasks.json')
    print(f'Issue: build task has isBackground=true but no background problemMatcher patterns')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
