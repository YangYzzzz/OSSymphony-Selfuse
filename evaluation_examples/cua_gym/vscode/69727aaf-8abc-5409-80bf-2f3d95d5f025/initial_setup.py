"""
Initial Setup: Set up a compound debug configuration in launch.json
Task ID: vscode_py_034
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_034'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create main.py - FastAPI application
    main_py_content = '''"""FastAPI backend server for the inventory management system."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

app = FastAPI(title="Inventory Management API", version="1.0.0")


class Product(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float
    category: Optional[str] = None


# In-memory product store
products: dict[str, Product] = {}


@app.get("/")
async def root():
    return {"message": "Inventory Management API is running", "version": "1.0.0"}


@app.get("/products")
async def list_products():
    return {"products": list(products.values()), "count": len(products)}


@app.get("/products/{sku}")
async def get_product(sku: str):
    if sku not in products:
        raise HTTPException(status_code=404, detail=f"Product {sku} not found")
    return products[sku]


@app.post("/products")
async def create_product(product: Product):
    if product.sku in products:
        raise HTTPException(status_code=409, detail=f"Product {product.sku} already exists")
    products[product.sku] = product
    return {"message": "Product created", "product": product}


@app.put("/products/{sku}")
async def update_product(sku: str, product: Product):
    if sku not in products:
        raise HTTPException(status_code=404, detail=f"Product {sku} not found")
    products[sku] = product
    return {"message": "Product updated", "product": product}


@app.delete("/products/{sku}")
async def delete_product(sku: str):
    if sku not in products:
        raise HTTPException(status_code=404, detail=f"Product {sku} not found")
    deleted = products.pop(sku)
    return {"message": "Product deleted", "product": deleted}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
'''
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_py_content)

    # Create worker.py - Celery worker
    worker_py_content = '''"""Celery worker for background task processing."""

from celery import Celery
import time
import logging

logger = logging.getLogger(__name__)

app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@app.task(bind=True, max_retries=3)
def process_inventory_update(self, sku: str, quantity_change: int):
    """Process an inventory quantity update asynchronously."""
    try:
        logger.info(f"Processing inventory update for SKU {sku}: {quantity_change:+d}")
        time.sleep(0.5)  # Simulate processing time
        return {"sku": sku, "quantity_change": quantity_change, "status": "completed"}
    except Exception as exc:
        logger.error(f"Failed to process inventory update: {exc}")
        raise self.retry(exc=exc, countdown=5)


@app.task(bind=True, max_retries=2)
def generate_report(self, report_type: str, date_range: dict):
    """Generate an inventory report in the background."""
    try:
        logger.info(f"Generating {report_type} report for range: {date_range}")
        time.sleep(2)  # Simulate report generation
        return {
            "report_type": report_type,
            "date_range": date_range,
            "status": "generated",
            "row_count": 150,
        }
    except Exception as exc:
        logger.error(f"Report generation failed: {exc}")
        raise self.retry(exc=exc, countdown=10)


@app.task
def sync_external_warehouse(warehouse_id: str):
    """Sync inventory data with an external warehouse system."""
    logger.info(f"Syncing with warehouse {warehouse_id}")
    time.sleep(1)
    return {"warehouse_id": warehouse_id, "synced_items": 42, "status": "synced"}


@app.task
def cleanup_stale_entries(days_threshold: int = 90):
    """Remove inventory entries not updated within the threshold."""
    logger.info(f"Cleaning up entries older than {days_threshold} days")
    time.sleep(0.8)
    return {"removed_count": 7, "threshold_days": days_threshold}
'''
    with open(f'{PROJECT_DIR}/worker.py', 'w') as f:
        f.write(worker_py_content)

    # Create requirements.txt
    requirements_content = '''fastapi==0.109.0
uvicorn==0.27.0
celery==5.3.6
redis==5.0.1
pydantic==2.5.3
'''
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # Ensure NO .vscode/launch.json exists (this is what the task asks to create)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - main.py (FastAPI app)')
    print(f'  - worker.py (Celery worker)')
    print(f'  - requirements.txt')
    print(f'  - No .vscode/launch.json (task requires creating it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
