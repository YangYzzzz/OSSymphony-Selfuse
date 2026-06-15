"""
Initial Setup: Configure Flake8 linter extension in VSCode
Task ID: vscode_we_064
Domain: vscode

Creates a Python project workspace with empty user settings.
The ms-python.flake8 extension is assumed pre-installed.
VSCode is opened with the workspace folder.
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


def create_initial():
    # --- Create workspace directory with Python project files ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a realistic Python project structure
    src_dir = os.path.join(WORKSPACE_DIR, "src")
    os.makedirs(src_dir, exist_ok=True)

    # Main application file
    with open(os.path.join(WORKSPACE_DIR, "main.py"), "w") as f:
        f.write("""\
#!/usr/bin/env python3
\"\"\"Main entry point for the inventory management application.\"\"\"

import sys
from src.inventory import InventoryManager
from src.reports import generate_monthly_report


def main():
    manager = InventoryManager(database_path="data/inventory.db")
    manager.load_products()

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_monthly_report(manager)
        print(report)
    else:
        manager.run_interactive()


if __name__ == "__main__":
    main()
""")

    # Inventory module
    with open(os.path.join(src_dir, "__init__.py"), "w") as f:
        f.write('"""Inventory management package."""\n')

    with open(os.path.join(src_dir, "inventory.py"), "w") as f:
        f.write("""\
\"\"\"Inventory management core module.\"\"\"

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_price: float
    quantity_on_hand: int
    reorder_threshold: int = 10
    last_restocked: Optional[datetime] = None


class InventoryManager:
    def __init__(self, database_path: str = "data/inventory.db"):
        self.database_path = database_path
        self.products: List[Product] = []

    def load_products(self):
        \"\"\"Load products from the database.\"\"\"
        # Placeholder for database loading logic
        self.products = [
            Product("SKU-001", "Wireless Mouse", "Electronics", 29.99, 150, 20),
            Product("SKU-002", "USB-C Hub", "Electronics", 45.50, 85, 15),
            Product("SKU-003", "Standing Desk Mat", "Office", 34.95, 200, 25),
            Product("SKU-004", "Mechanical Keyboard", "Electronics", 89.99, 60, 10),
            Product("SKU-005", "Monitor Arm", "Office", 119.00, 45, 8),
        ]

    def find_low_stock(self) -> List[Product]:
        return [p for p in self.products if p.quantity_on_hand <= p.reorder_threshold]

    def get_total_value(self) -> float:
        return sum(p.unit_price * p.quantity_on_hand for p in self.products)

    def run_interactive(self):
        print("Inventory Management System v2.1")
        print(f"Loaded {len(self.products)} products")
        low_stock = self.find_low_stock()
        if low_stock:
            print(f"WARNING: {len(low_stock)} products below reorder threshold")
""")

    with open(os.path.join(src_dir, "reports.py"), "w") as f:
        f.write("""\
\"\"\"Report generation module.\"\"\"

from datetime import datetime


def generate_monthly_report(manager) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"Monthly Inventory Report - {datetime.now().strftime('%B %Y')}")
    lines.append("=" * 60)
    lines.append(f"Total Products: {len(manager.products)}")
    lines.append(f"Total Inventory Value: ${manager.get_total_value():,.2f}")
    lines.append("")
    lines.append("Low Stock Items:")
    for product in manager.find_low_stock():
        lines.append(f"  - {product.name} (SKU: {product.sku}): {product.quantity_on_hand} units")
    lines.append("")
    return "\\n".join(lines)
""")

    # Requirements file
    with open(os.path.join(WORKSPACE_DIR, "requirements.txt"), "w") as f:
        f.write("""\
flake8==7.0.0
pytest==8.1.1
black==24.3.0
mypy==1.9.0
""")

    # Create a .venv directory placeholder (simulating virtual environment)
    venv_bin = os.path.join(WORKSPACE_DIR, ".venv", "bin")
    os.makedirs(venv_bin, exist_ok=True)
    # Create a placeholder flake8 executable
    flake8_path = os.path.join(venv_bin, "flake8")
    with open(flake8_path, "w") as f:
        f.write("#!/usr/bin/env python3\n# flake8 placeholder\n")
    os.chmod(flake8_path, 0o755)

    # --- Ensure VSCode user settings are empty ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)
    print(f"Settings written (empty): {SETTINGS_PATH}")

    # --- Launch VSCode with the workspace folder ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with workspace folder with DISPLAY=:0")


create_initial()
