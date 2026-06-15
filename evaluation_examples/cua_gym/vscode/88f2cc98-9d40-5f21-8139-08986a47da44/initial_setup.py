"""
Initial Setup: Indent lines 10-20 of logic.py by one level
Task ID: vscode_stu_045
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_045'
OUTPUT = f'{WORKDIR}/logic.py'

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

# A realistic Python file where lines 10-20 are at base indentation (0 indent).
# The scenario: the user has written a module and now wants to wrap lines 10-20
# inside a new if-statement, so they need to indent that block by one level.
#
# Line numbers (1-indexed):
#  1-9:   imports, constants, docstring — stay as-is
# 10-20:  standalone statements at base level — these get indented
# 21+:    more code — stays as-is

LOGIC_PY = '''\
"""
Order processing logic for the warehouse management system.
Handles validation, pricing calculations, and inventory updates.
"""

import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional

TAX_RATE = Decimal("0.085")
DISCOUNT_THRESHOLDS = {500: Decimal("0.05"), 1000: Decimal("0.10"), 5000: Decimal("0.15")}
FREE_SHIPPING_MIN = Decimal("150.00")
EXPEDITED_FEE = Decimal("25.00")
HANDLING_FEE = Decimal("3.50")
WAREHOUSE_ZONES = ["A", "B", "C", "D"]
MAX_ITEMS_PER_ORDER = 200
BACKORDER_LIMIT = 50
CURRENCY_PRECISION = Decimal("0.01")
LOW_STOCK_ALERT = 10
REORDER_POINT = 25


def validate_order(order: Dict) -> bool:
    """Validate that an order has all required fields and correct types."""
    required_fields = ["customer_id", "items", "shipping_address"]
    for field in required_fields:
        if field not in order:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(order["items"], list) or len(order["items"]) == 0:
        raise ValueError("Order must contain at least one item")

    if len(order["items"]) > MAX_ITEMS_PER_ORDER:
        raise ValueError(f"Order exceeds max of {MAX_ITEMS_PER_ORDER} items")

    for item in order["items"]:
        if "sku" not in item or "quantity" not in item:
            raise ValueError("Each item must have sku and quantity")
        if item["quantity"] <= 0:
            raise ValueError("Item quantity must be positive")

    return True


def calculate_subtotal(items: List[Dict], price_catalog: Dict) -> Decimal:
    """Calculate the subtotal before tax and discounts."""
    subtotal = Decimal("0.00")
    for item in items:
        sku = item["sku"]
        qty = item["quantity"]
        if sku not in price_catalog:
            raise KeyError(f"SKU {sku} not found in price catalog")
        unit_price = Decimal(str(price_catalog[sku]))
        subtotal += unit_price * qty
    return subtotal.quantize(CURRENCY_PRECISION, rounding=ROUND_HALF_UP)


def apply_discount(subtotal: Decimal) -> Decimal:
    """Apply tiered discount based on order subtotal."""
    discount_rate = Decimal("0.00")
    for threshold, rate in sorted(DISCOUNT_THRESHOLDS.items(), reverse=True):
        if subtotal >= threshold:
            discount_rate = rate
            break
    discount_amount = (subtotal * discount_rate).quantize(
        CURRENCY_PRECISION, rounding=ROUND_HALF_UP
    )
    return subtotal - discount_amount
'''

def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(LOGIC_PY)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
