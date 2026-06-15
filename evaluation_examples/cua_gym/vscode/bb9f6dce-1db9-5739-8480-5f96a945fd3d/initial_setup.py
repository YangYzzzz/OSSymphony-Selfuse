"""
Initial Setup: Configure a Python virtual environment by creating a .venv
Task ID: vscode_lp_016
Domain: vscode

Creates a Python project workspace ~/projects/newapp/ with realistic files.
No .venv exists. VSCode opens the workspace folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_016'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'newapp')

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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # Ensure NO .venv exists
    venv_path = os.path.join(PROJECT_DIR, '.venv')
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)

    # Create main application file
    with open(os.path.join(PROJECT_DIR, 'src', 'app.py'), 'w') as f:
        f.write('''"""
NewApp - Inventory Management System
A lightweight REST API for managing product inventory.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: float
    quantity: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_stock(self, delta: int) -> None:
        """Adjust stock quantity by delta (positive or negative)."""
        new_qty = self.quantity + delta
        if new_qty < 0:
            raise ValueError(f"Insufficient stock for {self.sku}: have {self.quantity}, need {abs(delta)}")
        self.quantity = new_qty
        self.updated_at = datetime.now()

    def apply_discount(self, percent: float) -> float:
        """Return discounted price without modifying the original."""
        if not 0 < percent < 100:
            raise ValueError("Discount must be between 0 and 100")
        return round(self.price * (1 - percent / 100), 2)


class InventoryManager:
    def __init__(self):
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.sku in self._products:
            raise KeyError(f"Product {product.sku} already exists")
        self._products[product.sku] = product

    def get_product(self, sku: str) -> Product:
        if sku not in self._products:
            raise KeyError(f"Product {sku} not found")
        return self._products[sku]

    def list_by_category(self, category: str) -> list[Product]:
        return [p for p in self._products.values() if p.category == category]

    def total_inventory_value(self) -> float:
        return sum(p.price * p.quantity for p in self._products.values())
''')

    # Create test file
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_inventory.py'), 'w') as f:
        f.write('''"""Tests for the inventory management system."""

import pytest
from src.app import Product, InventoryManager


def test_product_creation():
    p = Product(sku="WH-1001", name="Wireless Headphones", category="Electronics",
                price=79.99, quantity=150)
    assert p.sku == "WH-1001"
    assert p.quantity == 150


def test_update_stock():
    p = Product(sku="KB-2003", name="Mechanical Keyboard", category="Electronics",
                price=129.99, quantity=50)
    p.update_stock(-10)
    assert p.quantity == 40
    p.update_stock(25)
    assert p.quantity == 65


def test_insufficient_stock():
    p = Product(sku="MS-3005", name="Ergonomic Mouse", category="Electronics",
                price=45.00, quantity=5)
    with pytest.raises(ValueError):
        p.update_stock(-10)


def test_inventory_manager():
    mgr = InventoryManager()
    mgr.add_product(Product(sku="CH-4001", name="Office Chair", category="Furniture",
                            price=299.99, quantity=20))
    mgr.add_product(Product(sku="DK-4002", name="Standing Desk", category="Furniture",
                            price=549.00, quantity=12))
    mgr.add_product(Product(sku="MN-5001", name="Ultrawide Monitor", category="Electronics",
                            price=899.99, quantity=8))

    furniture = mgr.list_by_category("Furniture")
    assert len(furniture) == 2

    total = mgr.total_inventory_value()
    assert total > 0
''')

    # Create requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''flask==3.0.2
requests==2.31.0
pytest==8.0.2
python-dotenv==1.0.1
gunicorn==21.2.0
''')

    # Create a simple README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# NewApp - Inventory Management System

A lightweight REST API for managing product inventory, built with Flask.

## Setup

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest tests/`

## Project Structure

```
newapp/
  src/
    app.py          # Core inventory logic
  tests/
    test_inventory.py
  requirements.txt
  README.md
```
''')

    # Create __init__.py files
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('')
    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    # Create .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('''.venv/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
dist/
build/
.env
''')

    print(f'Project created at: {PROJECT_DIR}')

    # Remove any existing workspace-level python interpreter setting
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    settings_file = os.path.join(vscode_dir, 'settings.json')
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                settings = {}
        # Remove python interpreter path if set
        settings.pop('python.defaultInterpreterPath', None)
        settings.pop('python.pythonPath', None)
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    # Launch VSCode with the project workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
