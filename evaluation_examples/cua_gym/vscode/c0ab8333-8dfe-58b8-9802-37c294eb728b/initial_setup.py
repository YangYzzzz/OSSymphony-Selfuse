"""
Initial Setup: Select the entire function body of 'processOrder' in orders.py
Task ID: vscode_edit_080
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_080'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/orders.py'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # 70-line Python file where processOrder spans exactly lines 25-45
    # Line 35 is inside a nested if-block (if not items, lines 32-35)
    # Cursor will be placed at line 35 via --goto flag
    content = (
        '"""\n'
        'Order processing module for e-commerce platform.\n'
        'Handles order validation, inventory checks, and payment processing.\n'
        '"""\n'
        '\n'
        'import datetime\n'
        'import logging\n'
        '\n'
        'logger = logging.getLogger(__name__)\n'
        '\n'
        'ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]\n'
        'MAX_ORDER_QUANTITY = 100\n'
        'DISCOUNT_THRESHOLD = 500.0\n'
        '\n'
        '\n'
        'def validateCustomer(customer_id: str) -> bool:\n'
        '    """Check if customer account is active and verified."""\n'
        '    if not customer_id or len(customer_id) < 4:\n'
        '        return False\n'
        '    logger.info(f"Validating customer: {customer_id}")\n'
        '    return True\n'
        '\n'
        '\n'
        '\n'
        'def processOrder(order_id: str, customer_id: str, items: list, total: float) -> dict:\n'
        '    """Process a customer order through validation and payment pipeline."""\n'
        '    result = {"order_id": order_id, "status": "pending", "message": ""}\n'
        '    if not validateCustomer(customer_id):\n'
        '        result["status"] = "failed"\n'
        '        result["message"] = "Invalid customer account"\n'
        '        return result\n'
        '    if not items or len(items) == 0:\n'
        '        result["status"] = "failed"\n'
        '        result["message"] = "Order contains no items"\n'
        '        return result\n'
        '    for item in items:\n'
        '        if item.get("quantity", 0) > MAX_ORDER_QUANTITY:\n'
        '            result["status"] = "failed"\n'
        '            result["message"] = f"Quantity exceeds limit for {item.get(\'sku\')}"\n'
        '            return result\n'
        '    if total >= DISCOUNT_THRESHOLD:\n'
        '        total *= 0.95\n'
        '        result["message"] = "Loyalty discount applied"\n'
        '    result["status"] = "processing"\n'
        '    return result\n'
        '\n'
        '\n'
        'def cancelOrder(order_id: str, reason: str = "") -> bool:\n'
        '    """Cancel an existing order if it has not been shipped yet."""\n'
        '    if not order_id:\n'
        '        return False\n'
        '    logger.warning(f"Cancelling order {order_id}: {reason}")\n'
        '    return True\n'
        '\n'
        '\n'
        'def getOrderHistory(customer_id: str, limit: int = 10) -> list:\n'
        '    """Retrieve the most recent orders for a given customer."""\n'
        '    if not validateCustomer(customer_id):\n'
        '        return []\n'
        '    logger.info(f"Fetching order history for {customer_id}, limit={limit}")\n'
        '    return []\n'
        '\n'
        '\n'
        'def calculateShipping(weight_kg: float, destination: str) -> float:\n'
        '    """Calculate shipping cost based on package weight and destination zone."""\n'
        '    base_rate = 3.50\n'
        '    if destination.startswith("US"):\n'
        '        return round(base_rate + weight_kg * 1.20, 2)\n'
        '    return round(base_rate + weight_kg * 2.85, 2)\n'
        '\n'
    )

    with open(OUTPUT, 'w') as f:
        f.write(content)

    # Verify line count and key lines
    lines = content.splitlines()
    assert len(lines) == 70, f"Expected 70 lines, got {len(lines)}"
    assert lines[24].startswith('def processOrder'), f"Line 25 should be def processOrder: {lines[24]}"
    assert lines[44].strip() == 'return result', f"Line 45 should be return result: {lines[44]}"
    assert '        return result' in lines[34], f"Line 35 should be nested return result: {lines[34]}"
    print(f'Initial file created: {OUTPUT} ({len(lines)} lines)')
    print(f'  Line 25: {lines[24]}')
    print(f'  Line 35: {lines[34]}')
    print(f'  Line 45: {lines[44]}')

    # GUI-ready startup: open VSCode with the file at line 35, column 1
    # --goto places the cursor at the specified line:column
    launch_gui(f'code --goto "{OUTPUT}:35:1"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with orders.py at line 35 with DISPLAY=:0')


create_initial()
