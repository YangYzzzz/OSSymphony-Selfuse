"""
Initial Setup: Configure workspace to use mypy as type checker for Python
Task ID: vscode_lp_037
Domain: vscode

Creates a typed Python project with multiple modules. The mypy extension
is installed but NOT configured. No mypy.ini exists. VSCode settings do
NOT contain mypy-type-checker.args.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_037'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'

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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_project():
    """Create a typed Python project with realistic modules."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application module
    create_file(f'{PROJECT_DIR}/main.py', '''\
"""Entry point for the inventory management system."""
from typing import List
from models import Product, Warehouse
from analytics import calculate_total_value, find_low_stock


def run_inventory_report(warehouse: Warehouse) -> None:
    """Generate and print the daily inventory report."""
    products: List[Product] = warehouse.get_products()
    total_value: float = calculate_total_value(products)
    low_stock: List[Product] = find_low_stock(products, threshold=10)

    print(f"Warehouse: {warehouse.name}")
    print(f"Total products: {len(products)}")
    print(f"Total value: ${total_value:,.2f}")
    print(f"Low stock items: {len(low_stock)}")

    for product in low_stock:
        print(f"  - {product.name}: {product.quantity} remaining")


if __name__ == "__main__":
    wh = Warehouse(name="West Coast Distribution", location="Portland, OR")
    run_inventory_report(wh)
''')

    # Data models
    create_file(f'{PROJECT_DIR}/models.py', '''\
"""Data models for the inventory system."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Product:
    """Represents a product in the inventory."""
    sku: str
    name: str
    quantity: int
    unit_price: float
    category: str
    last_restocked: Optional[datetime] = None

    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_price

    def is_low_stock(self, threshold: int = 10) -> bool:
        return self.quantity < threshold


@dataclass
class Supplier:
    """Represents a product supplier."""
    supplier_id: str
    company_name: str
    contact_email: str
    lead_time_days: int
    products_supplied: List[str]

    def can_supply(self, sku: str) -> bool:
        return sku in self.products_supplied


class Warehouse:
    """Manages a warehouse and its inventory."""

    def __init__(self, name: str, location: str) -> None:
        self.name = name
        self.location = location
        self._products: List[Product] = []
        self._suppliers: List[Supplier] = []

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def get_products(self) -> List[Product]:
        return list(self._products)

    def find_product(self, sku: str) -> Optional[Product]:
        for p in self._products:
            if p.sku == sku:
                return p
        return None

    def get_suppliers_for(self, sku: str) -> List[Supplier]:
        return [s for s in self._suppliers if s.can_supply(sku)]
''')

    # Analytics module
    create_file(f'{PROJECT_DIR}/analytics.py', '''\
"""Analytics functions for inventory data."""
from typing import List, Dict, Tuple
from collections import defaultdict
from models import Product


def calculate_total_value(products: List[Product]) -> float:
    """Calculate the total value of all products in inventory."""
    return sum(p.total_value for p in products)


def find_low_stock(products: List[Product], threshold: int = 10) -> List[Product]:
    """Find all products below the stock threshold."""
    return [p for p in products if p.is_low_stock(threshold)]


def group_by_category(products: List[Product]) -> Dict[str, List[Product]]:
    """Group products by their category."""
    groups: Dict[str, List[Product]] = defaultdict(list)
    for product in products:
        groups[product.category].append(product)
    return dict(groups)


def get_restock_priorities(
    products: List[Product],
    threshold: int = 10,
    value_weight: float = 0.6
) -> List[Tuple[Product, float]]:
    """
    Calculate restock priority scores for low-stock items.
    Higher scores indicate more urgent restocking needs.
    """
    low_stock = find_low_stock(products, threshold)
    priorities: List[Tuple[Product, float]] = []

    for product in low_stock:
        stock_urgency: float = 1.0 - (product.quantity / threshold)
        value_factor: float = product.unit_price / 100.0
        score: float = (stock_urgency * (1 - value_weight)) + (value_factor * value_weight)
        priorities.append((product, score))

    priorities.sort(key=lambda x: x[1], reverse=True)
    return priorities


def calculate_category_summary(products: List[Product]) -> Dict[str, Dict[str, float]]:
    """Summarize inventory metrics by category."""
    groups = group_by_category(products)
    summary: Dict[str, Dict[str, float]] = {}

    for category, items in groups.items():
        total_qty = sum(p.quantity for p in items)
        total_val = sum(p.total_value for p in items)
        avg_price = total_val / total_qty if total_qty > 0 else 0.0
        summary[category] = {
            "total_quantity": float(total_qty),
            "total_value": total_val,
            "average_price": avg_price,
            "item_count": float(len(items)),
        }

    return summary
''')

    # Test module with type annotations
    create_file(f'{PROJECT_DIR}/test_models.py', '''\
"""Tests for inventory models."""
from datetime import datetime
from models import Product, Warehouse, Supplier


def test_product_value() -> None:
    product = Product(
        sku="WH-1042",
        name="Industrial Sensor",
        quantity=25,
        unit_price=149.99,
        category="Electronics",
        last_restocked=datetime(2025, 11, 3),
    )
    assert product.total_value == 25 * 149.99
    assert not product.is_low_stock(threshold=10)
    assert product.is_low_stock(threshold=30)


def test_warehouse_operations() -> None:
    warehouse = Warehouse(name="Test Warehouse", location="Test City")
    p1 = Product(sku="A-001", name="Widget", quantity=50, unit_price=9.99, category="Parts")
    p2 = Product(sku="A-002", name="Gadget", quantity=3, unit_price=29.99, category="Parts")

    warehouse.add_product(p1)
    warehouse.add_product(p2)

    assert len(warehouse.get_products()) == 2
    assert warehouse.find_product("A-001") is not None
    assert warehouse.find_product("MISSING") is None


def test_supplier() -> None:
    supplier = Supplier(
        supplier_id="SUP-100",
        company_name="TechParts Co.",
        contact_email="orders@techparts.example.com",
        lead_time_days=14,
        products_supplied=["WH-1042", "A-001"],
    )
    assert supplier.can_supply("WH-1042")
    assert not supplier.can_supply("UNKNOWN")


if __name__ == "__main__":
    test_product_value()
    test_warehouse_operations()
    test_supplier()
    print("All tests passed.")
''')

    # Ensure no mypy.ini exists (negative constraint)
    mypy_ini_path = f'{PROJECT_DIR}/mypy.ini'
    if os.path.exists(mypy_ini_path):
        os.remove(mypy_ini_path)

    print(f'Project created at: {PROJECT_DIR}')


def create_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def configure_vscode():
    """Set up VSCode with Python support but NO mypy configuration."""
    # Install mypy-type-checker extension (installed but not configured)
    subprocess.run(['code', '--install-extension', 'ms-python.mypy-type-checker'],
                   capture_output=True, text=True)
    subprocess.run(['code', '--install-extension', 'ms-python.python'],
                   capture_output=True, text=True)

    # Set up basic VSCode settings (NO mypy-type-checker.args)
    update_settings({
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "editor.formatOnSave": False,
        "workbench.colorTheme": "Default Dark Modern",
    })

    # Ensure NO workspace settings with mypy config exist
    ws_settings_dir = f'{PROJECT_DIR}/.vscode'
    ws_settings_path = f'{ws_settings_dir}/settings.json'
    if os.path.exists(ws_settings_path):
        with open(ws_settings_path, 'r') as f:
            try:
                ws = json.load(f)
                ws.pop('mypy-type-checker.args', None)
                with open(ws_settings_path, 'w') as wf:
                    json.dump(ws, wf, indent=4)
            except json.JSONDecodeError:
                pass

    print('VSCode configured (mypy extension installed, not configured)')


def main():
    create_project()
    configure_vscode()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
