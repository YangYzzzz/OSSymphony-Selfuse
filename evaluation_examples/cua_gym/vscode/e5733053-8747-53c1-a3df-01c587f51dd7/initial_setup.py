"""
Initial Setup: Add pre-commit hook task chain to tasks.json
Task ID: vscode_td_033
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_033'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'typed-python')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASKS_JSON = os.path.join(VSCODE_DIR, 'tasks.json')


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
    # Create project directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # Create empty tasks.json (version + empty tasks array)
    tasks_config = {
        "version": "2.0.0",
        "tasks": []
    }
    with open(TASKS_JSON, 'w') as f:
        json.dump(tasks_config, f, indent=4)
    print(f'Created empty tasks.json: {TASKS_JSON}')

    # Create a realistic Python project with type annotations
    # pyproject.toml
    pyproject = """[project]
name = "typed-python"
version = "1.0.0"
description = "A typed Python project for data processing"
requires-python = ">=3.10"

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
"""
    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write(pyproject)

    # src/__init__.py
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('"""Typed Python data processing library."""\n')

    # src/models.py - realistic typed Python code
    models_py = '''"""Data models for customer analytics pipeline."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class CustomerTier(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "US"


@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    email: str
    tier: CustomerTier
    address: Address
    created_at: datetime
    lifetime_value: float = 0.0
    is_active: bool = True
    notes: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[dict[str, float]] = field(default_factory=list)
    order_date: date = field(default_factory=date.today)
    total: float = 0.0
    shipped: bool = False

    def calculate_total(self) -> float:
        self.total = sum(item.get("price", 0.0) for item in self.items)
        return self.total
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models.py'), 'w') as f:
        f.write(models_py)

    # src/processing.py
    processing_py = '''"""Data processing utilities for the analytics pipeline."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterator

from .models import Customer, CustomerTier, Address, Order


def load_customers(csv_path: Path) -> list[Customer]:
    """Load customer records from a CSV file."""
    customers: list[Customer] = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            address = Address(
                street=row["street"],
                city=row["city"],
                state=row["state"],
                zip_code=row["zip_code"],
            )
            customer = Customer(
                customer_id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                tier=CustomerTier(row["tier"]),
                address=address,
                created_at=datetime.fromisoformat(row["created_at"]),
                lifetime_value=float(row.get("ltv", 0)),
            )
            customers.append(customer)
    return customers


def filter_active_customers(
    customers: list[Customer], min_ltv: float = 0.0
) -> Iterator[Customer]:
    """Yield active customers with lifetime value above threshold."""
    for customer in customers:
        if customer.is_active and customer.lifetime_value >= min_ltv:
            yield customer


def summarize_orders(orders: list[Order]) -> dict[str, float]:
    """Aggregate order totals by customer ID."""
    summary: dict[str, float] = {}
    for order in orders:
        if order.customer_id in summary:
            summary[order.customer_id] += order.total
        else:
            summary[order.customer_id] = order.total
    return summary
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'processing.py'), 'w') as f:
        f.write(processing_py)

    # tests/__init__.py
    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    # tests/test_models.py
    test_models = '''"""Tests for data models."""

from datetime import datetime

from src.models import Address, Customer, CustomerTier


def test_customer_full_name() -> None:
    address = Address(
        street="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62704",
    )
    customer = Customer(
        customer_id="C001",
        first_name="Sarah",
        last_name="Chen",
        email="sarah.chen@example.com",
        tier=CustomerTier.GOLD,
        address=address,
        created_at=datetime(2024, 1, 15),
    )
    assert customer.full_name == "Sarah Chen"
'''
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_models.py'), 'w') as f:
        f.write(test_models)

    # Install tools (ensure they are available)
    subprocess.run(['pip3', 'install', 'black', 'isort', 'mypy'],
                   capture_output=True, timeout=120)
    print('Installed black, isort, mypy')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
