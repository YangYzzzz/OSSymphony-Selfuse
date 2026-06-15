"""
Initial Setup: Create Python project with legacy_api.py (no type hints)
Task ID: vscode_lp_034
Domain: vscode / os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_034'
PROJECT_DIR = f'{WORKDIR}/python_project'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create legacy_api.py - a realistic Python module with 3 public functions, NO type hints
    legacy_api_content = '''\
"""
Legacy API module for user management, order processing, and payments.

This module provides core business logic functions for the e-commerce
platform. Originally written before type hints were standard practice.
"""

import datetime
import uuid


# In-memory data stores (simulating database)
_users_db = [
    {"id": "u001", "name": "Sarah Chen", "email": "sarah.chen@techcorp.io", "active": True},
    {"id": "u002", "name": "Marcus Johnson", "email": "marcus.j@dataflow.com", "active": True},
    {"id": "u003", "name": "Priya Sharma", "email": "priya.s@cloudnine.dev", "active": False},
    {"id": "u004", "name": "James O\'Brien", "email": "jobrien@startup.co", "active": True},
    {"id": "u005", "name": "Aisha Patel", "email": "aisha.p@enterprise.org", "active": True},
]

_orders_db = []
_payments_db = []


def get_users(limit):
    """Retrieve a list of active users from the database.

    Returns up to `limit` active user records as a list of dictionaries.
    Each dictionary contains id, name, email, and active status.
    """
    active_users = [u for u in _users_db if u["active"]]
    return active_users[:limit]


def create_order(user_id, items):
    """Create a new order for the specified user.

    Validates the user exists and items list is non-empty,
    then creates an order record with a generated ID and timestamp.
    Returns the complete order dictionary or None if validation fails.
    """
    user = next((u for u in _users_db if u["id"] == user_id), None)
    if user is None:
        return None

    if not items or not isinstance(items, list):
        return None

    order = {
        "order_id": f"ord-{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "items": items,
        "total": sum(item.get("price", 0) * item.get("quantity", 1) for item in items),
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat(),
    }
    _orders_db.append(order)
    return order


def process_payment(order_id, amount):
    """Process payment for an existing order.

    Looks up the order by ID, validates the payment amount matches
    the order total, and records the payment transaction.
    Returns True if payment succeeds, False otherwise.
    """
    order = next((o for o in _orders_db if o["order_id"] == order_id), None)
    if order is None:
        return False

    if amount <= 0:
        return False

    payment = {
        "payment_id": f"pay-{uuid.uuid4().hex[:8]}",
        "order_id": order_id,
        "amount": amount,
        "status": "completed",
        "processed_at": datetime.datetime.now().isoformat(),
    }
    _payments_db.append(payment)
    order["status"] = "paid"
    return True
'''

    legacy_api_path = os.path.join(PROJECT_DIR, 'legacy_api.py')
    with open(legacy_api_path, 'w') as f:
        f.write(legacy_api_content)
    print(f'Created: {legacy_api_path}')

    # Create a small main.py that imports from legacy_api (shows why stubs matter)
    main_content = '''\
"""Main application entry point demonstrating legacy_api usage."""

from legacy_api import get_users, create_order, process_payment


def run():
    # Fetch first 3 active users
    users = get_users(3)
    print(f"Found {len(users)} users")

    if users:
        # Create an order for the first user
        order = create_order(
            users[0]["id"],
            [
                {"name": "Widget Pro", "price": 29.99, "quantity": 2},
                {"name": "Cable Kit", "price": 12.50, "quantity": 1},
            ],
        )
        if order:
            print(f"Order created: {order['order_id']} - Total: ${order['total']:.2f}")

            # Process payment
            success = process_payment(order["order_id"], order["total"])
            print(f"Payment {'succeeded' if success else 'failed'}")


if __name__ == "__main__":
    run()
'''

    main_path = os.path.join(PROJECT_DIR, 'main.py')
    with open(main_path, 'w') as f:
        f.write(main_content)
    print(f'Created: {main_path}')

    # Ensure NO .pyi file exists (the task is to create it)
    pyi_path = os.path.join(PROJECT_DIR, 'legacy_api.pyi')
    if os.path.exists(pyi_path):
        os.remove(pyi_path)
        print(f'Removed pre-existing stub: {pyi_path}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open the legacy_api.py file specifically
    launch_gui(f'code "{legacy_api_path}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
