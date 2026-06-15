"""
Initial Setup: Add secondary keybinding Ctrl+F12 for Go to Definition
Task ID: vscode_gf2_010
Domain: vscode

Creates a workspace with Python files, ensures keybindings.json is empty
(no custom keybindings), and opens VSCode.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_010'
HOME = os.path.expanduser('~')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'workspace')


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
    """Create a realistic Python project for the developer context."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application file
    main_py = '''\
"""Main entry point for the inventory management system."""

from models import Product, Warehouse
from utils import calculate_reorder_point, format_currency


def get_inventory_summary(warehouse: Warehouse) -> dict:
    """Return summary statistics for all products in a warehouse."""
    total_value = sum(p.price * p.quantity for p in warehouse.products)
    low_stock = [p for p in warehouse.products if p.quantity < p.reorder_threshold]
    return {
        "warehouse": warehouse.name,
        "total_products": len(warehouse.products),
        "total_value": format_currency(total_value),
        "low_stock_items": [p.name for p in low_stock],
    }


def process_shipment(warehouse: Warehouse, shipment: list):
    """Process incoming shipment and update inventory levels."""
    for item in shipment:
        product = warehouse.find_product(item["sku"])
        if product:
            product.quantity += item["quantity"]
            print(f"Updated {product.name}: +{item['quantity']} units")
        else:
            print(f"Unknown SKU: {item['sku']}")


if __name__ == "__main__":
    from sample_data import create_sample_warehouse
    wh = create_sample_warehouse()
    summary = get_inventory_summary(wh)
    for key, value in summary.items():
        print(f"  {key}: {value}")
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # Models file
    models_py = '''\
"""Data models for inventory management."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Product:
    sku: str
    name: str
    price: float
    quantity: int
    reorder_threshold: int = 10
    category: str = "General"
    last_restocked: Optional[datetime] = None

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    def needs_reorder(self) -> bool:
        return self.quantity < self.reorder_threshold


@dataclass
class Warehouse:
    name: str
    location: str
    products: List[Product] = field(default_factory=list)

    def find_product(self, sku: str) -> Optional[Product]:
        for product in self.products:
            if product.sku == sku:
                return product
        return None

    def add_product(self, product: Product):
        existing = self.find_product(product.sku)
        if existing:
            existing.quantity += product.quantity
        else:
            self.products.append(product)
'''
    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write(models_py)

    # Utils file
    utils_py = '''\
"""Utility functions for inventory calculations."""

import math
from datetime import timedelta


def calculate_reorder_point(avg_daily_usage: float, lead_time_days: int,
                             safety_stock: int = 5) -> int:
    """Calculate when to reorder based on usage and lead time."""
    return math.ceil(avg_daily_usage * lead_time_days) + safety_stock


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a number as currency string."""
    return f"{symbol}{amount:,.2f}"


def estimate_days_until_stockout(current_qty: int, avg_daily_usage: float) -> int:
    """Estimate how many days until stock runs out."""
    if avg_daily_usage <= 0:
        return 999
    return int(current_qty / avg_daily_usage)


def calculate_holding_cost(quantity: int, unit_cost: float,
                            holding_rate: float = 0.25,
                            period_days: int = 365) -> float:
    """Calculate inventory holding cost for a period."""
    return quantity * unit_cost * holding_rate * (period_days / 365)
'''
    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py)

    print(f'Workspace files created in {PROJECT_DIR}')


def setup_vscode_config():
    """Ensure VSCode config directory exists with empty keybindings."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Ensure keybindings.json is an empty array (no custom keybindings)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Keybindings reset to empty: {KEYBINDINGS_PATH}')

    # Load and preserve existing settings, just ensure reasonable defaults
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Merge in some reasonable defaults without overwriting existing
    defaults = {
        "editor.fontSize": 14,
        "editor.minimap.enabled": True,
    }
    for k, v in defaults.items():
        if k not in settings:
            settings[k] = v

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings updated: {SETTINGS_PATH}')


def main():
    create_workspace_files()
    setup_vscode_config()

    # Open VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
