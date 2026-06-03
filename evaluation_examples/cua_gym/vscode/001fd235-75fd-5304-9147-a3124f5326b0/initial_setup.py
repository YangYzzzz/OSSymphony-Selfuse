"""
Initial Setup: Configure Python extension for virtual environment
Task ID: vscode_we_062
Domain: vscode

Creates a realistic Python project with a virtual environment at ~/projects/myapp/.
The .vscode/settings.json does NOT exist yet (the agent must create it).
VSCode is opened with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_062'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'myapp')
VENV_DIR = os.path.join(PROJECT_DIR, '.venv')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # --- Create realistic Python source files ---
    # Main application file
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('"""MyApp - Inventory Management System"""\n\n__version__ = "1.2.0"\n')

    with open(os.path.join(SRC_DIR, 'models.py'), 'w') as f:
        f.write('''"""Data models for the inventory system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_price: float
    quantity_on_hand: int
    reorder_level: int = 10
    supplier_id: Optional[str] = None
    last_restocked: Optional[datetime] = None

    @property
    def total_value(self) -> float:
        return self.unit_price * self.quantity_on_hand

    def needs_reorder(self) -> bool:
        return self.quantity_on_hand <= self.reorder_level


@dataclass
class Warehouse:
    warehouse_id: str
    location: str
    capacity: int
    products: List[Product] = field(default_factory=list)

    def utilization_rate(self) -> float:
        total_items = sum(p.quantity_on_hand for p in self.products)
        return total_items / self.capacity if self.capacity > 0 else 0.0
''')

    with open(os.path.join(SRC_DIR, 'services.py'), 'w') as f:
        f.write('''"""Business logic for inventory operations."""

from typing import Dict, List
from .models import Product, Warehouse


class InventoryService:
    def __init__(self):
        self._warehouses: Dict[str, Warehouse] = {}

    def register_warehouse(self, warehouse: Warehouse) -> None:
        self._warehouses[warehouse.warehouse_id] = warehouse

    def get_low_stock_items(self) -> List[Product]:
        low_stock = []
        for wh in self._warehouses.values():
            for product in wh.products:
                if product.needs_reorder():
                    low_stock.append(product)
        return low_stock

    def transfer_stock(self, sku: str, from_wh: str, to_wh: str, qty: int) -> bool:
        src = self._warehouses.get(from_wh)
        dst = self._warehouses.get(to_wh)
        if not src or not dst:
            return False
        src_product = next((p for p in src.products if p.sku == sku), None)
        if not src_product or src_product.quantity_on_hand < qty:
            return False
        src_product.quantity_on_hand -= qty
        dst_product = next((p for p in dst.products if p.sku == sku), None)
        if dst_product:
            dst_product.quantity_on_hand += qty
        return True
''')

    # Test file
    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'tests', 'test_models.py'), 'w') as f:
        f.write('''"""Tests for inventory models."""

import pytest
from src.models import Product, Warehouse


class TestProduct:
    def test_total_value(self):
        p = Product(sku="WH-1001", name="Widget", category="Hardware",
                    unit_price=12.50, quantity_on_hand=200)
        assert p.total_value == 2500.0

    def test_needs_reorder_below_threshold(self):
        p = Product(sku="WH-1002", name="Gadget", category="Electronics",
                    unit_price=45.00, quantity_on_hand=5, reorder_level=10)
        assert p.needs_reorder() is True

    def test_needs_reorder_above_threshold(self):
        p = Product(sku="WH-1003", name="Bolt Pack", category="Hardware",
                    unit_price=3.25, quantity_on_hand=500, reorder_level=50)
        assert p.needs_reorder() is False


class TestWarehouse:
    def test_utilization_rate(self):
        wh = Warehouse(warehouse_id="WH-EAST", location="Boston", capacity=1000)
        wh.products = [
            Product(sku="A1", name="Item A", category="General",
                    unit_price=10.0, quantity_on_hand=300),
            Product(sku="A2", name="Item B", category="General",
                    unit_price=20.0, quantity_on_hand=200),
        ]
        assert wh.utilization_rate() == 0.5
''')

    # Project config files
    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "myapp"
version = "1.2.0"
description = "Inventory Management System"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.5.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0",
    "ruff>=0.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.ruff]
line-length = 120
target-version = "py310"
''')

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# MyApp - Inventory Management System

A Python-based inventory management system for multi-warehouse operations.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```
''')

    # --- Create virtual environment structure manually ---
    # python3-venv may not be installed, so create the structure by hand
    venv_bin = os.path.join(VENV_DIR, 'bin')
    venv_lib = os.path.join(VENV_DIR, 'lib', 'python3.10', 'site-packages')
    os.makedirs(venv_bin, exist_ok=True)
    os.makedirs(venv_lib, exist_ok=True)

    # Create symlink to system python as the venv python
    venv_python = os.path.join(venv_bin, 'python')
    if not os.path.exists(venv_python):
        os.symlink('/usr/bin/python3', venv_python)

    # Create pyvenv.cfg
    with open(os.path.join(VENV_DIR, 'pyvenv.cfg'), 'w') as f:
        f.write('home = /usr/bin\n')
        f.write('include-system-site-packages = false\n')
        f.write('version = 3.10.12\n')

    # Create activate script (minimal)
    with open(os.path.join(venv_bin, 'activate'), 'w') as f:
        f.write(f'export VIRTUAL_ENV="{VENV_DIR}"\nexport PATH="$VIRTUAL_ENV/bin:$PATH"\n')

    print(f'Virtual environment created at: {VENV_DIR}')
    assert os.path.exists(venv_python), f'venv python not found at {venv_python}'

    # --- Ensure NO .vscode/settings.json exists ---
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    settings_path = os.path.join(vscode_dir, 'settings.json')
    if os.path.exists(settings_path):
        os.remove(settings_path)
    if os.path.exists(vscode_dir) and not os.listdir(vscode_dir):
        os.rmdir(vscode_dir)
    print('Confirmed: No .vscode/settings.json exists')

    # --- Launch VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: launched VSCode with DISPLAY=:0 on {PROJECT_DIR}')


create_initial()
