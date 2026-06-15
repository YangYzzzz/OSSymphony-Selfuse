"""
Initial Setup: Stage specific hunks from app.py using VSCode Source Control
Task ID: vscode_gf1_023
Domain: vscode (git partial staging)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_023'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'

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


def run(cmd, cwd=None):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result


# ── 1. Create project directory ──────────────────────────────────────
os.makedirs(PROJECT_DIR, exist_ok=True)

# ── 2. Write the BASE version of app.py (pre-changes) ───────────────
BASE_APP_PY = '''\
"""
WebApp - Order Processing Application
Version 2.1.3
"""

import datetime
from decimal import Decimal
from typing import Optional, List, Dict


class OrderValidationError(Exception):
    """Raised when order validation fails."""
    pass


class Product:
    def __init__(self, product_id: str, name: str, price: Decimal, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity: int) -> bool:
        return self.stock >= quantity


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = "pending"
        self.created_at = datetime.datetime.now()
        self.discount_pct = Decimal("0")

    def add_item(self, item: OrderItem):
        self.items.append(item)

    @property
    def total(self) -> Decimal:
        raw = sum(item.subtotal for item in self.items)
        discount = raw * self.discount_pct / Decimal("100")
        return raw - discount


def process_order(order: Order, inventory: Dict[str, Product]) -> dict:
    """
    Validate and process an incoming order.
    Returns a summary dict with order details.
    """
    if not order.items:
        raise OrderValidationError("Order must contain at least one item")

    if order.discount_pct < 0:
        raise OrderValidationError("Discount cannot be negative")

    for item in order.items:
        product = inventory.get(item.product.product_id)
        if product is None:
            raise OrderValidationError(
                f"Product {item.product.product_id} not found in inventory"
            )
        if not product.is_available(item.quantity):
            raise OrderValidationError(
                f"Insufficient stock for {product.name}"
            )

    # Update inventory
    for item in order.items:
        product = inventory[item.product.product_id]
        product.stock -= item.quantity

    order.status = "confirmed"

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "total": str(order.total),
        "item_count": len(order.items),
        "status": order.status,
    }


def get_order_history(customer_id: str, orders: List[Order]) -> List[dict]:
    """Retrieve order history for a customer."""
    history = []
    for order in orders:
        if order.customer_id == customer_id:
            history.append({
                "order_id": order.order_id,
                "total": str(order.total),
                "status": order.status,
                "date": order.created_at.isoformat(),
            })
    return sorted(history, key=lambda x: x["date"], reverse=True)


def calculate_shipping(order: Order, region: str) -> Decimal:
    """Calculate shipping cost based on order total and region."""
    base_rates = {
        "domestic": Decimal("5.99"),
        "international": Decimal("15.99"),
        "express": Decimal("25.99"),
    }
    rate = base_rates.get(region, Decimal("10.99"))

    if order.total > Decimal("100"):
        rate = rate * Decimal("0.5")

    return rate


def format_receipt(order: Order, shipping: Decimal) -> str:
    """Generate a formatted receipt string."""
    lines = [
        f"Order Receipt - {order.order_id}",
        f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"Customer: {order.customer_id}",
        "-" * 40,
    ]

    for item in order.items:
        lines.append(
            f"  {item.product.name:.<30} ${item.subtotal:>8.2f}"
        )

    lines.extend([
        "-" * 40,
        f"  {'Subtotal':.<30} ${order.total:>8.2f}",
        f"  {'Shipping':.<30} ${shipping:>8.2f}",
        f"  {'Total':.<30} ${order.total + shipping:>8.2f}",
    ])

    return "\\n".join(lines)
'''

# ── 3. Write the MODIFIED version (with 3 change hunks) ─────────────
MODIFIED_APP_PY = '''\
"""
WebApp - Order Processing Application
Version 2.1.3
"""

import datetime
import logging
from decimal import Decimal
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class OrderValidationError(Exception):
    """Raised when order validation fails."""
    pass


class Product:
    def __init__(self, product_id: str, name: str, price: Decimal, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity: int) -> bool:
        return self.stock >= quantity


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = "pending"
        self.created_at = datetime.datetime.now()
        self.discount_pct = Decimal("0")

    def add_item(self, item: OrderItem):
        self.items.append(item)

    @property
    def total(self) -> Decimal:
        raw = sum(item.subtotal for item in self.items)
        discount = raw * self.discount_pct / Decimal("100")
        return raw - discount


def process_order(order: Order, inventory: Dict[str, Product]) -> dict:
    """
    Validate and process an incoming order.
    Returns a summary dict with order details.
    """
    if not order.items:
        raise OrderValidationError("Order must contain at least one item")

    if order.discount_pct < 0 or order.discount_pct > 100:
        raise OrderValidationError("Discount must be between 0 and 100")

    for item in order.items:
        if item.quantity <= 0:
            raise OrderValidationError(
                f"Quantity must be positive for {item.product.name}"
            )
        product = inventory.get(item.product.product_id)
        if product is None:
            raise OrderValidationError(
                f"Product {item.product.product_id} not found in inventory"
            )
        if not product.is_available(item.quantity):
            raise OrderValidationError(
                f"Insufficient stock for {product.name}"
            )

    # Update inventory
    for item in order.items:
        product = inventory[item.product.product_id]
        product.stock -= item.quantity

    order.status = "confirmed"

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "total": str(order.total),
        "item_count": len(order.items),
        "status": order.status,
    }


def get_order_history(customer_id: str, orders: List[Order]) -> List[dict]:
    """Retrieve order history for a customer."""
    logger.info(f"Fetching order history for customer {customer_id}")
    history = []
    for order in orders:
        if order.customer_id == customer_id:
            history.append({
                "order_id": order.order_id,
                "total": str(order.total),
                "status": order.status,
                "date": order.created_at.isoformat(),
            })
    return sorted(history, key=lambda x: x["date"], reverse=True)


def calculate_shipping(order: Order, region: str) -> Decimal:
    """Calculate shipping cost based on order total and region."""
    base_rates = {
        "domestic": Decimal("5.99"),
        "international": Decimal("15.99"),
        "express": Decimal("25.99"),
    }
    rate = base_rates.get(region, Decimal("10.99"))

    if order.total > Decimal("100"):
        rate = rate * Decimal("0.5")

    # print(f"DEBUG: shipping rate={rate}, region={region}, total={order.total}")
    # print(f"DEBUG: base_rates={base_rates}")

    return rate


def format_receipt(order: Order, shipping: Decimal) -> str:
    """Generate a formatted receipt string."""
    lines = [
        f"Order Receipt - {order.order_id}",
        f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"Customer: {order.customer_id}",
        "-" * 40,
    ]

    for item in order.items:
        lines.append(
            f"  {item.product.name:.<30} ${item.subtotal:>8.2f}"
        )

    lines.extend([
        "-" * 40,
        f"  {'Subtotal':.<30} ${order.total:>8.2f}",
        f"  {'Shipping':.<30} ${shipping:>8.2f}",
        f"  {'Total':.<30} ${order.total + shipping:>8.2f}",
    ])

    return "\\n".join(lines)
'''

# ── 4. Initialize git repo with base version, then apply modifications ──
with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
    f.write(BASE_APP_PY)

# Create a .gitignore
with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
    f.write("__pycache__/\n*.pyc\n.env\n*.egg-info/\n")

# Create a simple README
with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
    f.write("# WebApp\n\nOrder processing web application.\n\n## Setup\n\n```bash\npip install -r requirements.txt\n```\n")

# Create requirements.txt
with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
    f.write("flask>=2.3.0\ngunicorn>=21.2.0\npsycopg2-binary>=2.9.0\n")

# Initialize git and make initial commit
run('git init', cwd=PROJECT_DIR)
run('git config user.email "developer@webapp.io"', cwd=PROJECT_DIR)
run('git config user.name "Alex Rivera"', cwd=PROJECT_DIR)
run('git add -A', cwd=PROJECT_DIR)
run('git commit -m "Initial project structure with order processing module"', cwd=PROJECT_DIR)

# ── 5. Now write the modified version (with 3 change hunks) ─────────
with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
    f.write(MODIFIED_APP_PY)

print(f"Project created at: {PROJECT_DIR}")
print("Git status should show app.py as modified with 3 change areas:")
print("  1. Bug fix: added discount upper bound check + quantity validation in process_order")
print("  2. Logging: added logger import/setup + logging call in get_order_history")
print("  3. Debug: commented-out debug print statements in calculate_shipping")

result = run('git diff --stat', cwd=PROJECT_DIR)
print(f"Git diff stat:\n{result.stdout}")

# ── 6. Open VSCode with the project folder ──────────────────────────
launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
print('GUI_READY: launched VSCode with DISPLAY=:0')
