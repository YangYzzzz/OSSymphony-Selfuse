"""
Initial Setup: Configure type checking to recognize custom type aliases
Task ID: vscode_py_057
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_057'
PROJECT_DIR = os.path.join(WORKDIR, 'src')
PKG_DIR = os.path.join(PROJECT_DIR, 'mylib')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Create package directory structure
    os.makedirs(PKG_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, '.vscode'), exist_ok=True)
    os.makedirs(VSCODE_USER, exist_ok=True)

    # --- src/mylib/__init__.py ---
    init_content = '''"""mylib - A utility library for user management and data processing."""

__version__ = "0.3.1"

from mylib.types import UserID, ProductID, OrderID, EmailAddress, Quantity
'''
    with open(os.path.join(PKG_DIR, '__init__.py'), 'w') as f:
        f.write(init_content)

    # --- src/mylib/types.py --- custom type aliases
    types_content = '''"""Custom type definitions for mylib package."""

from typing import NewType, Dict, List, Optional, Tuple

# Core entity identifiers
UserID = NewType('UserID', int)
ProductID = NewType('ProductID', int)
OrderID = NewType('OrderID', str)

# Validated string types
EmailAddress = NewType('EmailAddress', str)

# Numeric domain types
Quantity = NewType('Quantity', int)
Price = NewType('Price', float)

# Composite types using the aliases
UserProfile = Dict[str, any]
OrderItem = Tuple[ProductID, Quantity, Price]
OrderManifest = List[OrderItem]


def validate_user_id(uid: UserID) -> bool:
    """Check that a UserID is positive."""
    return uid > 0


def validate_email(email: EmailAddress) -> bool:
    """Basic email validation."""
    return "@" in email and "." in email.split("@")[-1]
'''
    with open(os.path.join(PKG_DIR, 'types.py'), 'w') as f:
        f.write(types_content)

    # --- src/mylib/services.py --- uses the custom types
    services_content = '''"""Service layer that relies on custom types from mylib.types."""

from mylib.types import (
    UserID, ProductID, OrderID, EmailAddress,
    Quantity, Price, OrderManifest, validate_user_id,
)
from typing import Optional, List


class UserService:
    """Manage user accounts."""

    def __init__(self):
        self._users: dict[UserID, dict] = {}

    def create_user(self, uid: UserID, name: str, email: EmailAddress) -> bool:
        if not validate_user_id(uid):
            return False
        self._users[uid] = {"name": name, "email": email}
        return True

    def get_user_name(self, uid: UserID) -> Optional[str]:
        user = self._users.get(uid)
        return user["name"] if user else None


class OrderService:
    """Process product orders."""

    def __init__(self):
        self._orders: dict[OrderID, OrderManifest] = {}

    def place_order(
        self,
        order_id: OrderID,
        items: OrderManifest,
    ) -> float:
        self._orders[order_id] = items
        total: float = 0.0
        for product_id, qty, price in items:
            total += qty * price
        return total

    def get_order_total(self, order_id: OrderID) -> Optional[float]:
        items = self._orders.get(order_id)
        if items is None:
            return None
        return sum(qty * price for _, qty, price in items)
'''
    with open(os.path.join(PKG_DIR, 'services.py'), 'w') as f:
        f.write(services_content)

    # --- src/main.py --- entry point that uses the package
    main_content = '''"""Main application entry point demonstrating mylib usage."""

from mylib.types import UserID, ProductID, OrderID, EmailAddress, Quantity, Price
from mylib.services import UserService, OrderService


def run_demo():
    # User management
    user_svc = UserService()
    uid = UserID(1001)
    email = EmailAddress("sarah.chen@example.com")
    user_svc.create_user(uid, "Sarah Chen", email)

    # Order processing
    order_svc = OrderService()
    order_id = OrderID("ORD-2025-0042")
    items = [
        (ProductID(501), Quantity(2), Price(29.99)),
        (ProductID(502), Quantity(1), Price(149.50)),
    ]
    total = order_svc.place_order(order_id, items)
    print(f"Order {order_id} total: ${total:.2f}")

    name = user_svc.get_user_name(uid)
    print(f"Customer: {name}")


if __name__ == "__main__":
    run_demo()
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_content)

    # --- src/mylib/setup.py --- package metadata (no py.typed entry)
    setup_content = '''"""Package setup configuration."""

from setuptools import setup, find_packages

setup(
    name="mylib",
    version="0.3.1",
    packages=find_packages(),
    python_requires=">=3.8",
    description="Utility library for user management and data processing",
)
'''
    with open(os.path.join(PROJECT_DIR, 'setup.py'), 'w') as f:
        f.write(setup_content)

    # --- .vscode/settings.json (workspace settings) --- minimal, no type checking config
    vscode_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.trimTrailingWhitespace": True
    }
    with open(os.path.join(PROJECT_DIR, '.vscode', 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # --- User-level VSCode settings --- no Pylance type checking configured
    user_settings = {}
    try:
        with open(SETTINGS_PATH, 'r') as f:
            user_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_settings = {}

    # Ensure no type checking mode is set (remove if exists)
    user_settings.pop("python.analysis.typeCheckingMode", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(user_settings, f, indent=4)

    # Ensure py.typed does NOT exist
    py_typed_path = os.path.join(PKG_DIR, 'py.typed')
    if os.path.exists(py_typed_path):
        os.remove(py_typed_path)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Package at: {PKG_DIR}')
    print(f'Files: __init__.py, types.py, services.py, main.py, setup.py')
    print(f'No py.typed marker file exists')

    # GUI-ready startup: open VSCode with the src folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
