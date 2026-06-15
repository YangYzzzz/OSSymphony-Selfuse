"""
Initial Setup: VSCode Python workspace with empty settings
Task ID: vscode_py_039
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_039'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
SETTINGS_PATH = f'{VSCODE_DIR}/settings.json'


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

    # Create empty .vscode/settings.json
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Created empty settings: {SETTINGS_PATH}')

    # Create a realistic Python project
    # main.py
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write('''\
"""Main entry point for the inventory management system."""

from inventory import InventoryManager
from reports import generate_monthly_report


def main():
    manager = InventoryManager(db_path="data/inventory.db")
    manager.load_products()

    low_stock = manager.get_low_stock_items(threshold=10)
    if low_stock:
        print(f"Warning: {len(low_stock)} items below minimum stock level")
        for item in low_stock:
            print(f"  - {item.name}: {item.quantity} remaining")

    report = generate_monthly_report(manager, month=3, year=2026)
    report.save("reports/march_2026.pdf")
    print("Monthly report generated successfully.")


if __name__ == "__main__":
    main()
''')

    # inventory.py
    with open(f'{PROJECT_DIR}/inventory.py', 'w') as f:
        f.write('''\
"""Inventory management module for tracking products and stock levels."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    sku: str
    name: str
    quantity: int
    price: float
    category: str
    supplier: str


class InventoryManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.products: List[Product] = []

    def load_products(self) -> None:
        # Simulated data loading
        self.products = [
            Product("SKU-001", "Wireless Mouse", 45, 29.99, "Electronics", "TechSupply Co"),
            Product("SKU-002", "USB-C Hub", 8, 49.99, "Electronics", "TechSupply Co"),
            Product("SKU-003", "Standing Desk Mat", 23, 34.50, "Office", "ErgoWorks Ltd"),
            Product("SKU-004", "Mechanical Keyboard", 5, 129.99, "Electronics", "KeyCraft Inc"),
            Product("SKU-005", "Monitor Arm", 15, 89.00, "Office", "ErgoWorks Ltd"),
        ]

    def get_low_stock_items(self, threshold: int = 10) -> List[Product]:
        return [p for p in self.products if p.quantity < threshold]

    def find_product(self, sku: str) -> Optional[Product]:
        for product in self.products:
            if product.sku == sku:
                return product
        return None

    def update_quantity(self, sku: str, delta: int) -> bool:
        product = self.find_product(sku)
        if product is None:
            return False
        product.quantity += delta
        return True
''')

    # reports.py
    with open(f'{PROJECT_DIR}/reports.py', 'w') as f:
        f.write('''\
"""Report generation utilities for inventory analytics."""

from datetime import datetime


class Report:
    def __init__(self, title: str, data: dict):
        self.title = title
        self.data = data
        self.generated_at = datetime.now()

    def save(self, path: str) -> None:
        print(f"Saving report '{self.title}' to {path}")


def generate_monthly_report(manager, month: int, year: int) -> Report:
    total_value = sum(p.price * p.quantity for p in manager.products)
    low_stock_count = len(manager.get_low_stock_items())

    data = {
        "period": f"{year}-{month:02d}",
        "total_products": len(manager.products),
        "total_inventory_value": round(total_value, 2),
        "low_stock_alerts": low_stock_count,
    }

    return Report(f"Inventory Report - {year}/{month:02d}", data)
''')

    # utils.py
    with open(f'{PROJECT_DIR}/utils.py', 'w') as f:
        f.write('''\
"""Utility functions for data validation and formatting."""


def format_currency(amount: float, currency: str = "USD") -> str:
    symbols = {"USD": "$", "EUR": "\\u20ac", "GBP": "\\u00a3"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def validate_sku(sku: str) -> bool:
    if not sku or len(sku) < 5:
        return False
    parts = sku.split("-")
    return len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit()
''')

    print(f'Python project created at: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with DISPLAY=:0')


create_initial()
