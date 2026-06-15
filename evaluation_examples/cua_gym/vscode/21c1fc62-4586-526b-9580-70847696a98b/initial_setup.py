"""
Initial Setup: Configure VSCode pytest testing framework
Task ID: vscode_lp_003
Domain: vscode

Creates a realistic Python project at ~/projects/myapp/ with a tests/ directory
containing pytest-style test files. VSCode settings do NOT include any
python.testing.* configuration (that is the task for the agent to do).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_003'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'myapp')
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
    """Create a realistic Python project structure."""
    # --- Source code ---
    src_dir = os.path.join(PROJECT_DIR, 'src', 'myapp')
    os.makedirs(src_dir, exist_ok=True)

    # Package init
    with open(os.path.join(src_dir, '__init__.py'), 'w') as f:
        f.write('"""myapp — a lightweight inventory management library."""\n\n__version__ = "0.3.1"\n')

    # Core module
    with open(os.path.join(src_dir, 'inventory.py'), 'w') as f:
        f.write('''"""Inventory management utilities."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Product:
    sku: str
    name: str
    price: float
    quantity: int = 0
    category: str = "general"

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    def restock(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Restock amount must be non-negative")
        self.quantity += amount

    def sell(self, amount: int) -> float:
        if amount > self.quantity:
            raise ValueError(f"Insufficient stock: {self.quantity} available, {amount} requested")
        self.quantity -= amount
        return self.price * amount


class Warehouse:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.sku in self._products:
            raise KeyError(f"Product {product.sku} already exists")
        self._products[product.sku] = product

    def get_product(self, sku: str) -> Optional[Product]:
        return self._products.get(sku)

    def list_products(self, category: Optional[str] = None) -> List[Product]:
        products = list(self._products.values())
        if category:
            products = [p for p in products if p.category == category]
        return sorted(products, key=lambda p: p.name)

    def total_inventory_value(self) -> float:
        return sum(p.total_value for p in self._products.values())

    def low_stock_products(self, threshold: int = 5) -> List[Product]:
        return [p for p in self._products.values() if p.quantity <= threshold]
''')

    # Utils module
    with open(os.path.join(src_dir, 'utils.py'), 'w') as f:
        f.write('''"""Utility helpers for formatting and validation."""

import re
from typing import Optional


def format_currency(amount: float, currency: str = "USD") -> str:
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{amount:,.2f}"


def validate_sku(sku: str) -> bool:
    """SKU must be 2-4 uppercase letters followed by a dash and 3-6 digits."""
    return bool(re.match(r"^[A-Z]{2,4}-\\d{3,6}$", sku))


def parse_quantity(value: str) -> Optional[int]:
    """Parse a quantity string, returning None for invalid input."""
    try:
        qty = int(value.strip().replace(",", ""))
        return qty if qty >= 0 else None
    except (ValueError, AttributeError):
        return None
''')

    # --- Tests directory ---
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(tests_dir, 'conftest.py'), 'w') as f:
        f.write('''"""Shared pytest fixtures for myapp tests."""

import sys
import os
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from myapp.inventory import Product, Warehouse


@pytest.fixture
def sample_product():
    return Product(sku="ELC-1001", name="Wireless Mouse", price=29.99, quantity=150, category="electronics")


@pytest.fixture
def empty_warehouse():
    return Warehouse(name="West Coast Hub", location="Portland, OR")


@pytest.fixture
def stocked_warehouse(empty_warehouse, sample_product):
    wh = empty_warehouse
    wh.add_product(sample_product)
    wh.add_product(Product(sku="OFF-2010", name="Standing Desk", price=549.00, quantity=12, category="furniture"))
    wh.add_product(Product(sku="ELC-1045", name="USB-C Hub", price=45.50, quantity=3, category="electronics"))
    wh.add_product(Product(sku="OFF-2055", name="Ergonomic Chair", price=399.99, quantity=0, category="furniture"))
    return wh
''')

    with open(os.path.join(tests_dir, 'test_inventory.py'), 'w') as f:
        f.write('''"""Tests for the inventory module."""

import pytest
from myapp.inventory import Product, Warehouse


class TestProduct:
    def test_total_value(self, sample_product):
        assert sample_product.total_value == 29.99 * 150

    def test_restock(self, sample_product):
        sample_product.restock(50)
        assert sample_product.quantity == 200

    def test_restock_negative_raises(self, sample_product):
        with pytest.raises(ValueError, match="non-negative"):
            sample_product.restock(-10)

    def test_sell(self, sample_product):
        revenue = sample_product.sell(10)
        assert revenue == 299.90
        assert sample_product.quantity == 140

    def test_sell_insufficient_stock(self, sample_product):
        with pytest.raises(ValueError, match="Insufficient stock"):
            sample_product.sell(999)


class TestWarehouse:
    def test_add_and_get_product(self, empty_warehouse):
        p = Product(sku="TST-100", name="Test Widget", price=9.99, quantity=50)
        empty_warehouse.add_product(p)
        assert empty_warehouse.get_product("TST-100") is p

    def test_add_duplicate_raises(self, stocked_warehouse, sample_product):
        with pytest.raises(KeyError):
            stocked_warehouse.add_product(sample_product)

    def test_list_products_all(self, stocked_warehouse):
        products = stocked_warehouse.list_products()
        assert len(products) == 4

    def test_list_products_by_category(self, stocked_warehouse):
        electronics = stocked_warehouse.list_products(category="electronics")
        assert len(electronics) == 2

    def test_total_inventory_value(self, stocked_warehouse):
        value = stocked_warehouse.total_inventory_value()
        assert value > 0

    def test_low_stock_products(self, stocked_warehouse):
        low = stocked_warehouse.low_stock_products(threshold=5)
        assert len(low) == 2  # USB-C Hub (3) and Ergonomic Chair (0)
''')

    with open(os.path.join(tests_dir, 'test_utils.py'), 'w') as f:
        f.write('''"""Tests for utility functions."""

from myapp.utils import format_currency, validate_sku, parse_quantity


class TestFormatCurrency:
    def test_usd_default(self):
        assert format_currency(1234.5) == "$1,234.50"

    def test_euro(self):
        assert format_currency(999.0, "EUR") == "€999.00"

    def test_unknown_currency(self):
        result = format_currency(50.0, "CHF")
        assert "50.00" in result


class TestValidateSku:
    def test_valid_sku(self):
        assert validate_sku("ELC-1001") is True

    def test_invalid_sku_lowercase(self):
        assert validate_sku("elc-1001") is False

    def test_invalid_sku_no_dash(self):
        assert validate_sku("ELC1001") is False


class TestParseQuantity:
    def test_simple_number(self):
        assert parse_quantity("42") == 42

    def test_with_commas(self):
        assert parse_quantity("1,000") == 1000

    def test_invalid_string(self):
        assert parse_quantity("abc") is None

    def test_negative(self):
        assert parse_quantity("-5") is None
''')

    # --- Project config files ---
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('pytest>=7.4.0\npytest-cov>=4.1.0\nrequests>=2.31.0\n')

    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "myapp"
version = "0.3.1"
description = "A lightweight inventory management library"
requires-python = ">=3.9"
dependencies = ["requests>=2.31.0"]

[project.optional-dependencies]
dev = ["pytest>=7.4.0", "pytest-cov>=4.1.0", "ruff>=0.1.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
''')

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# myapp

A lightweight inventory management library for small-to-medium warehouses.

## Installation

```bash
pip install -e .
```

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
myapp/
├── src/myapp/
│   ├── __init__.py
│   ├── inventory.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_inventory.py
│   └── test_utils.py
├── pyproject.toml
└── requirements.txt
```
''')

    # --- VSCode workspace settings (NO python.testing.* settings) ---
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # Workspace-level settings — intentionally empty of testing config
    workspace_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.formatOnSave": True,
        "editor.rulers": [88],
        "files.trimTrailingWhitespace": True
    }
    with open(os.path.join(vscode_dir, 'settings.json'), 'w') as f:
        json.dump(workspace_settings, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Ensure user-level VSCode settings exist but do NOT contain testing config."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing or create base settings
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Ensure some basic settings exist, but NO python.testing.* keys
    settings.setdefault("editor.fontSize", 14)
    settings.setdefault("workbench.colorTheme", "Default Dark+")
    settings.setdefault("editor.minimap.enabled", True)
    settings.setdefault("editor.tabSize", 4)

    # Remove any existing python.testing.* keys to guarantee clean initial state
    keys_to_remove = [k for k in settings if k.startswith("python.testing.")]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode user settings configured at: {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the project workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
