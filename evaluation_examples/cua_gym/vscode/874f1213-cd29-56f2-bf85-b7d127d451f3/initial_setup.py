"""
Initial Setup: Configure workspace-level extension recommendations
Task ID: vscode_prod_017
Domain: vscode

Creates a Python API project with a .vscode folder but NO extensions.json.
Installs the three Python extensions. Opens VSCode with the project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_017'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-api')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'app'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'app', 'routers'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # .vscode/settings.json (basic workspace settings, NO extensions.json)
    settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.formatOnSave": True,
        "editor.tabSize": 4,
        "python.analysis.typeCheckingMode": "basic"
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(settings, f, indent=4)

    # Ensure NO extensions.json exists
    ext_json_path = os.path.join(VSCODE_DIR, 'extensions.json')
    if os.path.exists(ext_json_path):
        os.remove(ext_json_path)

    # Main application file
    with open(os.path.join(PROJECT_DIR, 'app', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'app', 'main.py'), 'w') as f:
        f.write('''"""
FastAPI application for inventory management.
Handles product catalog, stock levels, and order processing.
"""

from fastapi import FastAPI
from app.routers import products, orders

app = FastAPI(
    title="Inventory Management API",
    description="REST API for warehouse inventory tracking",
    version="2.1.0",
)

app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.1.0"}
''')

    with open(os.path.join(PROJECT_DIR, 'app', 'models.py'), 'w') as f:
        f.write('''"""Database models for inventory management."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_price: float
    quantity_in_stock: int
    reorder_level: int = 10
    supplier_id: Optional[str] = None
    last_restocked: Optional[datetime] = None


@dataclass
class Order:
    order_id: str
    customer_email: str
    items: list = field(default_factory=list)
    total_amount: float = 0.0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
''')

    with open(os.path.join(PROJECT_DIR, 'app', 'routers', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'app', 'routers', 'products.py'), 'w') as f:
        f.write('''"""Product management endpoints."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

# In-memory store for demo purposes
_products = {}


@router.get("/")
async def list_products(category: str = None, in_stock: bool = None):
    results = list(_products.values())
    if category:
        results = [p for p in results if p["category"] == category]
    if in_stock is not None:
        results = [p for p in results if (p["quantity_in_stock"] > 0) == in_stock]
    return {"products": results, "count": len(results)}


@router.get("/{sku}")
async def get_product(sku: str):
    if sku not in _products:
        raise HTTPException(status_code=404, detail=f"Product {sku} not found")
    return _products[sku]


@router.post("/")
async def create_product(product: dict):
    sku = product.get("sku")
    if not sku:
        raise HTTPException(status_code=400, detail="SKU is required")
    _products[sku] = product
    return {"message": f"Product {sku} created", "product": product}
''')

    with open(os.path.join(PROJECT_DIR, 'app', 'routers', 'orders.py'), 'w') as f:
        f.write('''"""Order processing endpoints."""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

router = APIRouter()

_orders = {}


@router.post("/")
async def create_order(order_data: dict):
    order_id = str(uuid.uuid4())[:8]
    order = {
        "order_id": order_id,
        "customer_email": order_data.get("customer_email", ""),
        "items": order_data.get("items", []),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    _orders[order_id] = order
    return {"message": "Order created", "order": order}


@router.get("/{order_id}")
async def get_order(order_id: str):
    if order_id not in _orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return _orders[order_id]
''')

    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'tests', 'test_products.py'), 'w') as f:
        f.write('''"""Tests for product endpoints."""

import pytest


def test_list_products_empty():
    """Verify empty product list returns correct structure."""
    # Placeholder for actual test implementation with TestClient
    assert True


def test_create_product_missing_sku():
    """Verify 400 error when SKU is missing."""
    assert True
''')

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''fastapi==0.109.2
uvicorn==0.27.1
pydantic==2.6.1
httpx==0.27.0
pytest==8.0.1
black==24.2.0
pylint==3.0.3
''')

    # pyproject.toml
    with open(os.path.join(PROJECT_DIR, 'pyproject.toml'), 'w') as f:
        f.write('''[tool.black]
line-length = 88
target-version = ["py311"]

[tool.pylint.messages_control]
disable = ["C0114", "C0115", "C0116"]

[tool.pytest.ini_options]
testpaths = ["tests"]
''')

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# Inventory Management API

REST API for warehouse inventory tracking built with FastAPI.

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health` - Health check
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/orders/{id}` - Get order
- `POST /api/v1/orders/` - Create order
''')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'.vscode/ exists: {os.path.isdir(VSCODE_DIR)}')
    print(f'extensions.json exists: {os.path.exists(os.path.join(VSCODE_DIR, "extensions.json"))}')

    # Install the three Python extensions
    extensions = [
        'ms-python.python',
        'ms-python.pylint',
        'ms-python.black-formatter',
    ]
    for ext_id in extensions:
        print(f'Installing extension: {ext_id}')
        subprocess.run(['code', '--install-extension', ext_id],
                       capture_output=True, text=True, timeout=60)

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
