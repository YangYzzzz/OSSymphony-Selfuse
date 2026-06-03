"""
Initial Setup: Create empty keybindings.json for VSCode keybinding task
Task ID: vscode_rrt_083
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

VSCODE_USER = os.path.join(os.path.expanduser("~"), ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")


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
    # Ensure the VSCode User config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write an empty keybindings.json array
    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump([], f, indent=4)
    print(f"Initial keybindings.json created: {KEYBINDINGS_PATH}")

    # Also create a small workspace with a sample file so the editor has something to show
    workspace_dir = "/home/user/workspace"
    os.makedirs(workspace_dir, exist_ok=True)

    sample_file = os.path.join(workspace_dir, "main.py")
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write('''"""
Inventory Management System - Main Module
"""
import os
import sys
from datetime import datetime


class InventoryItem:
    """Represents a single item in the warehouse inventory."""

    def __init__(self, sku: str, name: str, quantity: int, unit_price: float):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.last_updated = datetime.now()

    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_price

    def restock(self, amount: int) -> None:
        """Add stock to the inventory item."""
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self.quantity += amount
        self.last_updated = datetime.now()

    def sell(self, amount: int) -> float:
        """Remove stock and return the sale value."""
        if amount > self.quantity:
            raise ValueError(f"Insufficient stock: {self.quantity} available")
        self.quantity -= amount
        self.last_updated = datetime.now()
        return amount * self.unit_price


def load_inventory(filepath: str) -> list:
    """Load inventory data from a CSV file."""
    items = []
    # TODO: implement CSV parsing
    return items


if __name__ == "__main__":
    print("Inventory Management System v1.0")
''')
    print(f"Sample workspace created: {workspace_dir}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
