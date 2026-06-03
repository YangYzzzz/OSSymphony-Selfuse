"""
Initial Setup: Remove default Ctrl+W keybinding and reassign to close terminal
Task ID: vscode_rrt_069
Domain: vscode

Initial state: VSCode open with default keybindings, a workspace with sample
files, and no custom keybindings.json entries.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")
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
    # --- Create workspace with realistic sample files ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file
    main_py = os.path.join(WORKSPACE_DIR, "app.py")
    with open(main_py, "w") as f:
        f.write('''\
"""
Inventory Management System - Main Application
"""
import json
import os
from datetime import datetime


class InventoryManager:
    """Manages product inventory for a retail store."""

    def __init__(self, data_file="inventory.json"):
        self.data_file = data_file
        self.products = []
        self.load_data()

    def load_data(self):
        """Load inventory data from JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.products = json.load(f)
        else:
            self.products = self._get_default_inventory()
            self.save_data()

    def save_data(self):
        """Save inventory data to JSON file."""
        with open(self.data_file, "w") as f:
            json.dump(self.products, f, indent=2)

    def _get_default_inventory(self):
        return [
            {"sku": "WH-1001", "name": "Wireless Headphones", "quantity": 45, "price": 79.99},
            {"sku": "KB-2034", "name": "Mechanical Keyboard", "quantity": 32, "price": 129.50},
            {"sku": "MS-3012", "name": "Ergonomic Mouse", "quantity": 67, "price": 49.95},
            {"sku": "MN-4056", "name": "27-inch Monitor", "quantity": 12, "price": 349.00},
            {"sku": "WC-5078", "name": "USB-C Webcam", "quantity": 89, "price": 64.99},
        ]

    def add_product(self, sku, name, quantity, price):
        """Add a new product to the inventory."""
        product = {
            "sku": sku,
            "name": name,
            "quantity": quantity,
            "price": price,
        }
        self.products.append(product)
        self.save_data()
        return product

    def get_total_value(self):
        """Calculate total inventory value."""
        return sum(p["quantity"] * p["price"] for p in self.products)


if __name__ == "__main__":
    manager = InventoryManager()
    print(f"Total inventory value: ${manager.get_total_value():,.2f}")
    for product in manager.products:
        print(f"  {product['sku']}: {product['name']} x{product['quantity']} @ ${product['price']}")
''')

    # A utility module
    utils_py = os.path.join(WORKSPACE_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write('''\
"""
Utility functions for the inventory system.
"""
from datetime import datetime


def format_currency(amount):
    """Format a number as USD currency."""
    return f"${amount:,.2f}"


def generate_report_header():
    """Generate a report header with the current date."""
    now = datetime.now()
    return f"Inventory Report - {now.strftime('%B %d, %Y')}"


def validate_sku(sku):
    """Validate SKU format: XX-NNNN."""
    if len(sku) != 7:
        return False
    if sku[2] != "-":
        return False
    return sku[:2].isalpha() and sku[3:].isdigit()
''')

    # --- Ensure VSCode user config dir exists ---
    os.makedirs(VSCODE_USER, exist_ok=True)

    # --- Ensure keybindings.json is default (empty array) ---
    # This represents the default state: no custom keybindings
    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump([], f, indent=4)
    print(f"Keybindings reset to default (empty): {KEYBINDINGS_PATH}")

    # --- Ensure settings.json has reasonable defaults ---
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Don't override existing settings, just ensure a few basics
    defaults = {
        "editor.fontSize": 14,
        "terminal.integrated.defaultProfile.linux": "bash",
    }
    for k, v in defaults.items():
        if k not in settings:
            settings[k] = v

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings ensured: {SETTINGS_PATH}")

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)

    # Open the main file
    launch_gui(f'code "{main_py}"', delay_sec=2.0)

    print("GUI_READY: VSCode launched with workspace and default keybindings")


create_initial()
