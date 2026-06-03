"""
Initial Setup: Python monorepo with broken cross-package imports
Task ID: vscode_fix_046
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_046'
MONOREPO = f'{WORKDIR}/monorepo'

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
    # ---- Directory structure ----
    dirs = [
        f'{MONOREPO}/packages/core/src/core',
        f'{MONOREPO}/packages/core/tests',
        f'{MONOREPO}/packages/api/src/api',
        f'{MONOREPO}/packages/api/tests',
        f'{MONOREPO}/.vscode',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # ---- packages/core/src/core/__init__.py ----
    with open(f'{MONOREPO}/packages/core/src/core/__init__.py', 'w') as f:
        f.write('"""Core package - shared utilities and data models."""\n\n'
                'from core.models import User, Product, Order\n'
                'from core.utils import format_currency, validate_email\n')

    # ---- packages/core/src/core/models.py ----
    with open(f'{MONOREPO}/packages/core/src/core/models.py', 'w') as f:
        f.write('''\
"""Data models for the inventory management system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class User:
    user_id: str
    name: str
    email: str
    role: str = "viewer"
    created_at: datetime = field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        return self.role == "admin"


@dataclass
class Product:
    product_id: str
    name: str
    price: float
    category: str
    stock_quantity: int = 0
    description: Optional[str] = None

    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0

    def apply_discount(self, percentage: float) -> float:
        """Return the discounted price."""
        return self.price * (1 - percentage / 100)


@dataclass
class Order:
    order_id: str
    user_id: str
    items: List[dict] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)

    def total_amount(self) -> float:
        return sum(item.get("price", 0) * item.get("quantity", 1) for item in self.items)

    def add_item(self, product_id: str, price: float, quantity: int = 1):
        self.items.append({
            "product_id": product_id,
            "price": price,
            "quantity": quantity,
        })
''')

    # ---- packages/core/src/core/utils.py ----
    with open(f'{MONOREPO}/packages/core/src/core/utils.py', 'w') as f:
        f.write('''\
"""Shared utility functions used across all packages."""

import re
from typing import Optional


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a numeric amount as a currency string."""
    symbols = {"USD": "$", "EUR": "\\u20ac", "GBP": "\\u00a3", "JPY": "\\u00a5"}
    symbol = symbols.get(currency, currency + " ")
    if currency == "JPY":
        return f"{symbol}{amount:,.0f}"
    return f"{symbol}{amount:,.2f}"


def validate_email(email: str) -> bool:
    """Validate an email address using a simple regex pattern."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\\w\\s-]", "", text)
    text = re.sub(r"[\\s_]+", "-", text)
    return text.strip("-")


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_length, appending suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def parse_int(value: str, default: Optional[int] = None) -> Optional[int]:
    """Safely parse an integer from a string."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
''')

    # ---- packages/api/src/api/__init__.py ----
    with open(f'{MONOREPO}/packages/api/src/api/__init__.py', 'w') as f:
        f.write('"""API package - REST endpoints for inventory management."""\n\n'
                'from api.routes import create_app\n')

    # ---- packages/api/src/api/routes.py ----
    # This file imports from core, which Pylance cannot resolve without extraPaths
    with open(f'{MONOREPO}/packages/api/src/api/routes.py', 'w') as f:
        f.write('''\
"""API route handlers for the inventory management system."""

from typing import Dict, List, Optional

# These imports trigger Pylance errors without proper extraPaths configuration
from core.models import User, Product, Order
from core.utils import format_currency, validate_email


class InventoryAPI:
    """REST API handler for inventory operations."""

    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._orders: Dict[str, Order] = {}
        self._users: Dict[str, User] = {}

    def add_product(self, product_id: str, name: str, price: float,
                    category: str, stock: int = 0) -> Product:
        """Register a new product in the inventory."""
        product = Product(
            product_id=product_id,
            name=name,
            price=price,
            category=category,
            stock_quantity=stock,
        )
        self._products[product_id] = product
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def list_products(self, category: Optional[str] = None) -> List[Product]:
        products = list(self._products.values())
        if category:
            products = [p for p in products if p.category == category]
        return products

    def create_order(self, order_id: str, user_id: str,
                     items: List[dict]) -> Order:
        """Create a new order after validating user and products."""
        user = self._users.get(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")

        order = Order(order_id=order_id, user_id=user_id)
        for item in items:
            pid = item["product_id"]
            qty = item.get("quantity", 1)
            product = self._products.get(pid)
            if product is None:
                raise ValueError(f"Product {pid} not found")
            if product.stock_quantity < qty:
                raise ValueError(f"Insufficient stock for {pid}")
            order.add_item(pid, product.price, qty)
            product.stock_quantity -= qty
        self._orders[order_id] = order
        return order

    def get_order_summary(self, order_id: str) -> dict:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order {order_id} not found")
        return {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "total": format_currency(order.total_amount()),
            "status": order.status,
            "item_count": len(order.items),
        }

    def register_user(self, user_id: str, name: str, email: str,
                      role: str = "viewer") -> User:
        if not validate_email(email):
            raise ValueError(f"Invalid email: {email}")
        user = User(user_id=user_id, name=name, email=email, role=role)
        self._users[user_id] = user
        return user


def create_app() -> InventoryAPI:
    """Factory function to create and return an API instance."""
    return InventoryAPI()
''')

    # ---- packages/api/src/api/middleware.py ----
    with open(f'{MONOREPO}/packages/api/src/api/middleware.py', 'w') as f:
        f.write('''\
"""Request middleware and authentication helpers."""

from core.models import User
from core.utils import validate_email


def authenticate_request(headers: dict, users: dict) -> User:
    """Validate auth token and return the corresponding User."""
    token = headers.get("Authorization", "")
    if not token.startswith("Bearer "):
        raise PermissionError("Missing or invalid Authorization header")
    user_id = token.split(" ", 1)[1]
    user = users.get(user_id)
    if user is None:
        raise PermissionError(f"Unknown user: {user_id}")
    return user


def require_admin(user: User):
    """Raise if user is not an admin."""
    if not user.is_admin():
        raise PermissionError(f"Admin access required; {user.name} has role '{user.role}'")
''')

    # ---- packages/core/tests/test_models.py ----
    with open(f'{MONOREPO}/packages/core/tests/test_models.py', 'w') as f:
        f.write('''\
"""Unit tests for core data models."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.models import User, Product, Order


def test_user_admin():
    admin = User(user_id="u1", name="Alice", email="alice@example.com", role="admin")
    viewer = User(user_id="u2", name="Bob", email="bob@example.com")
    assert admin.is_admin()
    assert not viewer.is_admin()


def test_product_stock():
    p = Product(product_id="p1", name="Widget", price=9.99, category="hardware", stock_quantity=5)
    assert p.is_in_stock()
    p.stock_quantity = 0
    assert not p.is_in_stock()


def test_product_discount():
    p = Product(product_id="p2", name="Gadget", price=100.0, category="electronics")
    assert abs(p.apply_discount(20) - 80.0) < 0.01


def test_order_total():
    o = Order(order_id="o1", user_id="u1")
    o.add_item("p1", 10.0, 2)
    o.add_item("p2", 25.0, 1)
    assert abs(o.total_amount() - 45.0) < 0.01


if __name__ == "__main__":
    test_user_admin()
    test_product_stock()
    test_product_discount()
    test_order_total()
    print("All core tests passed.")
''')

    # ---- packages/api/tests/test_routes.py ----
    with open(f'{MONOREPO}/packages/api/tests/test_routes.py', 'w') as f:
        f.write('''\
"""Unit tests for API route handlers."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "core", "src"))

from api.routes import create_app


def test_register_and_order():
    app = create_app()
    app.register_user("u1", "Sarah Chen", "sarah@techcorp.io", role="admin")
    app.add_product("p1", "Mechanical Keyboard", 149.99, "peripherals", stock=10)
    app.add_product("p2", "USB-C Hub", 59.99, "peripherals", stock=25)

    order = app.create_order("o1", "u1", [
        {"product_id": "p1", "quantity": 1},
        {"product_id": "p2", "quantity": 2},
    ])
    summary = app.get_order_summary("o1")
    assert summary["item_count"] == 2
    assert summary["status"] == "pending"
    print(f"Order total: {summary[\'total\']}")


if __name__ == "__main__":
    test_register_and_order()
    print("All API tests passed.")
''')

    # ---- Root files ----
    with open(f'{MONOREPO}/README.md', 'w') as f:
        f.write('''\
# Inventory Management Monorepo

A Python monorepo for the Inventory Management System.

## Structure

```
packages/
  core/     - Shared models and utilities
  api/      - REST API endpoints
```

## Development

Each package has its own `src/` and `tests/` directories.
Cross-package imports use absolute imports (e.g., `from core.models import User`).
''')

    with open(f'{MONOREPO}/pyproject.toml', 'w') as f:
        f.write('''\
[project]
name = "inventory-monorepo"
version = "0.1.0"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["packages/core/src", "packages/api/src"]
''')

    # ---- .vscode/settings.json (initial state: empty extraPaths) ----
    vscode_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.analysis.autoImportCompletions": True,
        "python.analysis.extraPaths": [],
        "editor.formatOnSave": True,
        "editor.rulers": [88, 120],
        "files.trimTrailingWhitespace": True,
        "files.insertFinalNewline": True,
    }
    with open(f'{MONOREPO}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # ---- NO pyrightconfig.json (as per task context) ----

    print(f'Monorepo created at: {MONOREPO}')
    print(f'.vscode/settings.json has empty python.analysis.extraPaths')
    print(f'No pyrightconfig.json exists')

    # GUI-ready: open VSCode with the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
