"""
Initial Setup: Git repo with 3 poorly organized commits to be reorganized
Task ID: vscode_git_066
Domain: vs_code

Creates a git repo at /home/user/project with:
- api.py, tests/test_api.py, docs/README.md
- A base commit + 3 poorly-organized commits:
    commit 1: 'misc changes' (modified api.py + tests/test_api.py)
    commit 2: 'more updates' (modified api.py + docs/README.md)
    commit 3: 'final fixes'  (modified tests/test_api.py + docs/README.md)
The agent must soft-reset HEAD~3, then re-commit in 2 logical groups.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, env=None):
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        shlex.split(cmd) if isinstance(cmd, str) else cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def git(cmd, cwd=PROJECT_DIR, env=None):
    full_cmd = f'git {cmd}'
    out, err, rc = run(full_cmd, cwd=cwd, env=env)
    if rc != 0:
        print(f'[git {cmd}] ERROR: {err.strip()}')
    return out.strip()


def create_initial():
    # ------------------------------------------------------------------
    # 0. Clean up any previous run
    # ------------------------------------------------------------------
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Git identity env (needed in headless VM environments)
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git_e(cmd):
        return git(cmd, env=git_env)

    # ------------------------------------------------------------------
    # 1. Initialize repo
    # ------------------------------------------------------------------
    git_e('init')
    git_e('config user.email "dev@example.com"')
    git_e('config user.name "Dev User"')

    # ------------------------------------------------------------------
    # 2. Base commit — initial project files
    # ------------------------------------------------------------------
    write_file(f'{PROJECT_DIR}/api.py', '''\
"""
API Endpoint Handlers for the CRM Service.
"""

import json
from typing import Optional


BASE_URL = "/api/v1"


def get_customer(customer_id: int) -> dict:
    """Retrieve a customer record by ID."""
    # TODO: replace with database query
    return {
        "id": customer_id,
        "name": "Alice Martinez",
        "email": "alice@example.com",
        "tier": "premium",
    }


def list_orders(customer_id: int, limit: int = 10) -> list:
    """List recent orders for a customer."""
    # TODO: replace with database query
    return [
        {"order_id": 1001, "amount": 249.99, "status": "shipped"},
        {"order_id": 1002, "amount": 89.50,  "status": "processing"},
    ][:limit]


def create_order(customer_id: int, items: list) -> dict:
    """Create a new order for a customer."""
    total = sum(item.get("price", 0) * item.get("qty", 1) for item in items)
    return {
        "order_id": 9999,
        "customer_id": customer_id,
        "total": total,
        "status": "pending",
    }
''')

    write_file(f'{PROJECT_DIR}/tests/test_api.py', '''\
"""
Unit tests for the CRM API endpoint handlers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from api import get_customer, list_orders, create_order


class TestGetCustomer(unittest.TestCase):
    def test_returns_dict(self):
        result = get_customer(42)
        self.assertIsInstance(result, dict)

    def test_has_id_field(self):
        result = get_customer(7)
        self.assertIn("id", result)

    def test_id_matches(self):
        result = get_customer(100)
        self.assertEqual(result["id"], 100)


class TestListOrders(unittest.TestCase):
    def test_returns_list(self):
        result = list_orders(1)
        self.assertIsInstance(result, list)

    def test_limit_param(self):
        result = list_orders(1, limit=1)
        self.assertLessEqual(len(result), 1)


class TestCreateOrder(unittest.TestCase):
    def test_returns_order(self):
        items = [{"price": 19.99, "qty": 2}]
        result = create_order(1, items)
        self.assertIn("order_id", result)

    def test_status_pending(self):
        result = create_order(1, [])
        self.assertEqual(result["status"], "pending")


if __name__ == "__main__":
    unittest.main()
''')

    write_file(f'{PROJECT_DIR}/tests/__init__.py', '')

    write_file(f'{PROJECT_DIR}/docs/README.md', '''\
# CRM Service API

A lightweight Python API layer for the CRM service.

## Overview

This module provides endpoint handlers for:
- Customer records management
- Order creation and retrieval

## Endpoints

| Function | Description |
|---|---|
| `get_customer(id)` | Fetch a customer record |
| `list_orders(id, limit)` | List recent orders |
| `create_order(id, items)` | Create a new order |

## Usage

```python
from api import get_customer, list_orders, create_order

customer = get_customer(42)
orders = list_orders(42, limit=5)
new_order = create_order(42, [{"price": 29.99, "qty": 1}])
```

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
''')

    write_file(f'{PROJECT_DIR}/requirements.txt', 'pytest>=7.0\n')

    git_e('add .')
    git_e('commit -m "Initial project structure: CRM API service"')

    # ------------------------------------------------------------------
    # 3. Commit A — "misc changes" (api.py + tests/test_api.py)
    # ------------------------------------------------------------------
    write_file(f'{PROJECT_DIR}/api.py', '''\
"""
API Endpoint Handlers for the CRM Service.
"""

import json
from typing import Optional, List


BASE_URL = "/api/v1"
API_VERSION = "1.0.0"


def get_customer(customer_id: int) -> dict:
    """Retrieve a customer record by ID from the database."""
    # TODO: replace with actual database query
    return {
        "id": customer_id,
        "name": "Alice Martinez",
        "email": "alice@example.com",
        "tier": "premium",
        "active": True,
    }


def list_orders(customer_id: int, limit: int = 10) -> list:
    """List recent orders for a customer."""
    # TODO: replace with database query
    return [
        {"order_id": 1001, "amount": 249.99, "status": "shipped"},
        {"order_id": 1002, "amount": 89.50,  "status": "processing"},
    ][:limit]


def create_order(customer_id: int, items: list) -> dict:
    """Create a new order for a customer."""
    total = sum(item.get("price", 0) * item.get("qty", 1) for item in items)
    return {
        "order_id": 9999,
        "customer_id": customer_id,
        "total": round(total, 2),
        "status": "pending",
    }


def delete_customer(customer_id: int) -> bool:
    """Soft-delete a customer record."""
    # TODO: replace with actual database operation
    return True
''')

    write_file(f'{PROJECT_DIR}/tests/test_api.py', '''\
"""
Unit tests for the CRM API endpoint handlers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from api import get_customer, list_orders, create_order, delete_customer


class TestGetCustomer(unittest.TestCase):
    def test_returns_dict(self):
        result = get_customer(42)
        self.assertIsInstance(result, dict)

    def test_has_id_field(self):
        result = get_customer(7)
        self.assertIn("id", result)

    def test_id_matches(self):
        result = get_customer(100)
        self.assertEqual(result["id"], 100)

    def test_has_active_field(self):
        result = get_customer(1)
        self.assertIn("active", result)


class TestListOrders(unittest.TestCase):
    def test_returns_list(self):
        result = list_orders(1)
        self.assertIsInstance(result, list)

    def test_limit_param(self):
        result = list_orders(1, limit=1)
        self.assertLessEqual(len(result), 1)


class TestCreateOrder(unittest.TestCase):
    def test_returns_order(self):
        items = [{"price": 19.99, "qty": 2}]
        result = create_order(1, items)
        self.assertIn("order_id", result)

    def test_status_pending(self):
        result = create_order(1, [])
        self.assertEqual(result["status"], "pending")

    def test_total_rounded(self):
        items = [{"price": 1.005, "qty": 2}]
        result = create_order(1, items)
        self.assertAlmostEqual(result["total"], round(1.005 * 2, 2), places=2)


class TestDeleteCustomer(unittest.TestCase):
    def test_delete_returns_true(self):
        self.assertTrue(delete_customer(1))


if __name__ == "__main__":
    unittest.main()
''')

    git_e('add api.py tests/test_api.py')
    git_e('commit -m "misc changes"')

    # ------------------------------------------------------------------
    # 4. Commit B — "more updates" (api.py + docs/README.md)
    # ------------------------------------------------------------------
    write_file(f'{PROJECT_DIR}/api.py', '''\
"""
API Endpoint Handlers for the CRM Service.
"""

import json
from typing import Optional, List


BASE_URL = "/api/v1"
API_VERSION = "1.1.0"


def get_customer(customer_id: int) -> dict:
    """Retrieve a customer record by ID from the database."""
    # TODO: replace with actual database query
    return {
        "id": customer_id,
        "name": "Alice Martinez",
        "email": "alice@example.com",
        "tier": "premium",
        "active": True,
    }


def list_orders(customer_id: int, limit: int = 10, status_filter: str = None) -> list:
    """List recent orders for a customer, optionally filtered by status."""
    orders = [
        {"order_id": 1001, "amount": 249.99, "status": "shipped"},
        {"order_id": 1002, "amount": 89.50,  "status": "processing"},
        {"order_id": 1003, "amount": 15.00,  "status": "delivered"},
    ]
    if status_filter:
        orders = [o for o in orders if o["status"] == status_filter]
    return orders[:limit]


def create_order(customer_id: int, items: list) -> dict:
    """Create a new order for a customer."""
    total = sum(item.get("price", 0) * item.get("qty", 1) for item in items)
    return {
        "order_id": 9999,
        "customer_id": customer_id,
        "total": round(total, 2),
        "status": "pending",
    }


def delete_customer(customer_id: int) -> bool:
    """Soft-delete a customer record."""
    # TODO: replace with actual database operation
    return True


def update_customer_tier(customer_id: int, tier: str) -> dict:
    """Update the service tier for a customer."""
    valid_tiers = ["standard", "premium", "enterprise"]
    if tier not in valid_tiers:
        raise ValueError(f"Invalid tier: {tier}. Must be one of {valid_tiers}")
    return {"id": customer_id, "tier": tier, "updated": True}
''')

    write_file(f'{PROJECT_DIR}/docs/README.md', '''\
# CRM Service API

A lightweight Python API layer for the CRM service.

## Overview

This module provides endpoint handlers for:
- Customer records management (create, read, update, delete)
- Order creation and retrieval with status filtering

## Endpoints

| Function | Description |
|---|---|
| `get_customer(id)` | Fetch a customer record |
| `list_orders(id, limit, status_filter)` | List recent orders with optional filtering |
| `create_order(id, items)` | Create a new order |
| `delete_customer(id)` | Soft-delete a customer record |
| `update_customer_tier(id, tier)` | Update the customer service tier |

## Usage

```python
from api import get_customer, list_orders, create_order

customer = get_customer(42)
orders = list_orders(42, limit=5, status_filter="shipped")
new_order = create_order(42, [{"price": 29.99, "qty": 1}])
```

## Customer Tiers

- `standard` — basic features
- `premium` — priority support and higher rate limits
- `enterprise` — SLA guarantees and dedicated support

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
''')

    git_e('add api.py docs/README.md')
    git_e('commit -m "more updates"')

    # ------------------------------------------------------------------
    # 5. Commit C — "final fixes" (tests/test_api.py + docs/README.md)
    # ------------------------------------------------------------------
    write_file(f'{PROJECT_DIR}/tests/test_api.py', '''\
"""
Unit tests for the CRM API endpoint handlers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from api import (
    get_customer, list_orders, create_order,
    delete_customer, update_customer_tier,
)


class TestGetCustomer(unittest.TestCase):
    def test_returns_dict(self):
        result = get_customer(42)
        self.assertIsInstance(result, dict)

    def test_has_id_field(self):
        result = get_customer(7)
        self.assertIn("id", result)

    def test_id_matches(self):
        result = get_customer(100)
        self.assertEqual(result["id"], 100)

    def test_has_active_field(self):
        result = get_customer(1)
        self.assertIn("active", result)


class TestListOrders(unittest.TestCase):
    def test_returns_list(self):
        result = list_orders(1)
        self.assertIsInstance(result, list)

    def test_limit_param(self):
        result = list_orders(1, limit=1)
        self.assertLessEqual(len(result), 1)

    def test_status_filter(self):
        result = list_orders(1, status_filter="shipped")
        for order in result:
            self.assertEqual(order["status"], "shipped")


class TestCreateOrder(unittest.TestCase):
    def test_returns_order(self):
        items = [{"price": 19.99, "qty": 2}]
        result = create_order(1, items)
        self.assertIn("order_id", result)

    def test_status_pending(self):
        result = create_order(1, [])
        self.assertEqual(result["status"], "pending")

    def test_total_rounded(self):
        items = [{"price": 1.005, "qty": 2}]
        result = create_order(1, items)
        self.assertAlmostEqual(result["total"], round(1.005 * 2, 2), places=2)


class TestDeleteCustomer(unittest.TestCase):
    def test_delete_returns_true(self):
        self.assertTrue(delete_customer(1))


class TestUpdateCustomerTier(unittest.TestCase):
    def test_update_to_enterprise(self):
        result = update_customer_tier(1, "enterprise")
        self.assertEqual(result["tier"], "enterprise")

    def test_invalid_tier_raises(self):
        with self.assertRaises(ValueError):
            update_customer_tier(1, "vip")


if __name__ == "__main__":
    unittest.main()
''')

    write_file(f'{PROJECT_DIR}/docs/README.md', '''\
# CRM Service API

A lightweight Python API layer for the CRM service.

## Overview

This module provides endpoint handlers for:
- Customer records management (create, read, update, soft-delete)
- Order creation and retrieval with status filtering

## Endpoints

| Function | Description |
|---|---|
| `get_customer(id)` | Fetch a customer record |
| `list_orders(id, limit, status_filter)` | List recent orders with optional filtering |
| `create_order(id, items)` | Create a new order |
| `delete_customer(id)` | Soft-delete a customer record |
| `update_customer_tier(id, tier)` | Update the customer service tier |

## Usage

```python
from api import get_customer, list_orders, create_order, update_customer_tier

customer = get_customer(42)
orders = list_orders(42, limit=5, status_filter="shipped")
new_order = create_order(42, [{"price": 29.99, "qty": 1}])
update_customer_tier(42, "enterprise")
```

## Customer Tiers

- `standard` — basic features
- `premium` — priority support and higher rate limits
- `enterprise` — SLA guarantees, dedicated support, and custom integrations

## Running Tests

```bash
python -m pytest tests/ -v
```

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
''')

    git_e('add tests/test_api.py docs/README.md')
    git_e('commit -m "final fixes"')

    # ------------------------------------------------------------------
    # 6. Verify the 3 commits are in history
    # ------------------------------------------------------------------
    log = git_e('log --oneline -5')
    print(f'Git log:\n{log}')

    # ------------------------------------------------------------------
    # 7. GUI: open VSCode with the project folder
    # ------------------------------------------------------------------
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'Initial project created at: {PROJECT_DIR}')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
