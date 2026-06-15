"""
Initial Setup: VSCode multi-cursor modifier set to 'alt' (problematic on Linux)
Task ID: vscode_fix_080
Domain: vscode
"""

import json
import os
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


def create_workspace_files():
    """Create a realistic workspace with Python files for multi-cursor editing."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main application file
    main_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''\
#!/usr/bin/env python3
"""Inventory Management System - Main Entry Point"""

from inventory import InventoryManager
from reports import generate_monthly_report


def main():
    manager = InventoryManager(db_path="data/inventory.db")
    manager.load_products()

    print("=== Inventory Management System ===")
    print(f"Total products: {manager.product_count}")
    print(f"Low stock items: {manager.get_low_stock_count()}")

    # Generate end-of-month report
    report = generate_monthly_report(manager, month=3, year=2026)
    report.save("reports/march_2026.csv")
    print(f"Report saved: {report.filepath}")


if __name__ == "__main__":
    main()
''')

    # Inventory module
    inventory_py = os.path.join(WORKSPACE_DIR, "inventory.py")
    with open(inventory_py, "w") as f:
        f.write('''\
"""Inventory management module with product tracking."""

import sqlite3
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    sku: str
    name: str
    category: str
    quantity: int
    unit_price: float
    reorder_threshold: int = 10


class InventoryManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.products: List[Product] = []

    def load_products(self) -> None:
        """Load all products from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            self.products.append(Product(*row))
        conn.close()

    @property
    def product_count(self) -> int:
        return len(self.products)

    def get_low_stock_count(self) -> int:
        return sum(1 for p in self.products if p.quantity < p.reorder_threshold)

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

    # Reports module
    reports_py = os.path.join(WORKSPACE_DIR, "reports.py")
    with open(reports_py, "w") as f:
        f.write('''\
"""Report generation for inventory analytics."""

import csv
import os
from datetime import datetime


class Report:
    def __init__(self, title: str, rows: list, filepath: str = ""):
        self.title = title
        self.rows = rows
        self.filepath = filepath

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.filepath = path
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["SKU", "Name", "Category", "Qty", "Price", "Status"])
            writer.writerows(self.rows)


def generate_monthly_report(manager, month: int, year: int) -> Report:
    """Generate a monthly inventory snapshot report."""
    title = f"Inventory Report - {datetime.strptime(str(month), '%m').strftime('%B')} {year}"
    rows = []
    for p in manager.products:
        status = "LOW" if p.quantity < p.reorder_threshold else "OK"
        rows.append([p.sku, p.name, p.category, p.quantity, p.unit_price, status])
    return Report(title=title, rows=rows)
''')

    print(f"Workspace created: {WORKSPACE_DIR}")


def setup_initial():
    # Create workspace files
    create_workspace_files()

    # Set VSCode settings with multi-cursor modifier as 'alt' (the problematic setting)
    update_settings({
        "editor.multiCursorModifier": "alt",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })
    print(f"Settings written to: {SETTINGS_PATH}")

    # Verify
    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)
    print(f"editor.multiCursorModifier = {settings.get('editor.multiCursorModifier')}")

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


setup_initial()
