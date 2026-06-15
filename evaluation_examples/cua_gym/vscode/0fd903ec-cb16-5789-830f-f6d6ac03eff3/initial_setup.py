"""
Initial Setup: Customize the editor appearance settings in VSCode
Task ID: vscode_we_042
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_042'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # Create workspace directory with some sample files
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample project file so VSCode has something to show
    sample_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(sample_py, 'w') as f:
        f.write('''"""
Inventory Management System
"""

class Product:
    def __init__(self, name, sku, price, quantity):
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

    def restock(self, amount):
        self.quantity += amount

    def sell(self, amount):
        if amount > self.quantity:
            raise ValueError(f"Insufficient stock for {self.name}")
        self.quantity -= amount
        return self.price * amount


class Warehouse:
    def __init__(self, location):
        self.location = location
        self.products = {}

    def add_product(self, product):
        self.products[product.sku] = product

    def get_inventory_report(self):
        report = []
        for sku, product in sorted(self.products.items()):
            report.append({
                "sku": sku,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "value": product.total_value()
            })
        return report


if __name__ == "__main__":
    warehouse = Warehouse("Building A")
    warehouse.add_product(Product("Wireless Mouse", "WM-001", 29.99, 150))
    warehouse.add_product(Product("Mechanical Keyboard", "MK-002", 89.99, 75))
    warehouse.add_product(Product("USB-C Hub", "UH-003", 45.50, 200))
    warehouse.add_product(Product("Monitor Stand", "MS-004", 34.99, 120))

    for item in warehouse.get_inventory_report():
        print(f"{item['name']:25s} | {item['sku']:8s} | ${item['price']:8.2f} | Qty: {item['quantity']:4d}")
''')

    readme = os.path.join(WORKSPACE_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('# Inventory Management System\n\nA simple product inventory tracking tool.\n')

    # Ensure VSCode user config directory exists with empty settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Initial settings created: {SETTINGS_PATH}')
    print(f'Workspace created: {WORKSPACE_DIR}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
