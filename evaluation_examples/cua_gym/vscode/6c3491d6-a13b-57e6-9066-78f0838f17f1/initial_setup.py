"""
Initial Setup: Configure multiple Python linters simultaneously
Task ID: vscode_py_065
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # --- Create Python project workspace ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main application file with some style issues and type issues
    main_py = '''\
"""Inventory Management System for Acme Electronics."""

from typing import List, Dict, Optional
import datetime


class Product:
    def __init__(self, sku: str, name: str, price: float, quantity: int):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.last_updated: datetime.datetime = datetime.datetime.now()

    def total_value(self) -> float:
        return self.price * self.quantity

    def restock(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Restock amount must be positive")
        self.quantity += amount
        self.last_updated = datetime.datetime.now()


class Inventory:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.transactions: List[dict] = []

    def add_product(self, product: Product) -> None:
        self.products[product.sku] = product
        self._log_transaction("add", product.sku, product.quantity)

    def remove_product(self, sku: str) -> Optional[Product]:
        product = self.products.pop(sku, None)
        if product:
            self._log_transaction("remove", sku, product.quantity)
        return product

    def get_product(self, sku: str) -> Optional[Product]:
        return self.products.get(sku)

    def total_inventory_value(self) -> float:
        return sum(p.total_value() for p in self.products.values())

    def low_stock_report(self, threshold: int = 10) -> List[Product]:
        return [p for p in self.products.values() if p.quantity < threshold]

    def _log_transaction(self, action: str, sku: str, qty: int) -> None:
        self.transactions.append({
            "action": action,
            "sku": sku,
            "quantity": qty,
            "timestamp": datetime.datetime.now().isoformat()
        })


def generate_monthly_report(inventory: Inventory) -> str:
    """Generate a summary report of current inventory status."""
    lines = ["=== Monthly Inventory Report ==="]
    lines.append(f"Total products: {len(inventory.products)}")
    lines.append(f"Total value: ${inventory.total_inventory_value():,.2f}")

    low_stock = inventory.low_stock_report()
    if low_stock:
        lines.append("\\nLow Stock Alerts:")
        for product in low_stock:
            lines.append(f"  - {product.name} (SKU: {product.sku}): {product.quantity} remaining")

    return "\\n".join(lines)


if __name__ == "__main__":
    inv = Inventory()
    inv.add_product(Product("ACE-001", "Wireless Mouse", 29.99, 150))
    inv.add_product(Product("ACE-002", "Mechanical Keyboard", 89.50, 75))
    inv.add_product(Product("ACE-003", "USB-C Hub", 45.00, 5))
    inv.add_product(Product("ACE-004", "Monitor Stand", 34.99, 200))
    inv.add_product(Product("ACE-005", "Webcam HD", 59.99, 8))

    report = generate_monthly_report(inv)
    print(report)
'''

    with open(os.path.join(WORKSPACE_DIR, "main.py"), "w") as f:
        f.write(main_py)

    # A utils module with some type annotation issues for mypy to find
    utils_py = '''\
"""Utility functions for data processing."""

from typing import List, Any, Union
import math


def calculate_discount(price: float, discount_pct: float) -> float:
    """Apply percentage discount to a price."""
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_pct / 100)


def format_currency(amount: float) -> str:
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"


def batch_process(items: List[Any], batch_size: int = 10) -> List[List[Any]]:
    """Split items into batches of given size."""
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def safe_divide(numerator: float, denominator: float) -> Union[float, None]:
    """Safely divide two numbers, returning None on zero division."""
    if denominator == 0:
        return None
    return numerator / denominator


def compute_statistics(values: List[float]) -> dict:
    """Compute basic statistics for a list of values."""
    if not values:
        return {"count": 0, "mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)

    return {
        "count": n,
        "mean": round(mean, 2),
        "std_dev": round(std_dev, 2),
        "min": min(values),
        "max": max(values),
    }
'''

    with open(os.path.join(WORKSPACE_DIR, "utils.py"), "w") as f:
        f.write(utils_py)

    # --- Configure VSCode settings with only pylint enabled ---
    update_settings({
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.linting.flake8Enabled": False,
        "python.linting.mypyEnabled": False,
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "workbench.colorTheme": "Default Dark Modern",
    })

    print(f"Initial workspace created: {WORKSPACE_DIR}")
    print(f"Settings configured at: {SETTINGS_PATH}")

    # --- Install flake8 and mypy so they are available ---
    subprocess.run(["pip3", "install", "flake8", "mypy"],
                    capture_output=True, text=True)
    print("flake8 and mypy installed")

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
