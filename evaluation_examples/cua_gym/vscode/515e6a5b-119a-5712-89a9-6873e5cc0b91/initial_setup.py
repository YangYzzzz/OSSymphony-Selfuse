"""
Initial Setup: Create VSCode workspace with Python and TypeScript files, no custom snippets.
Task ID: vscode_gf6_043
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_043'
PROJECT_DIR = f'{WORKDIR}/projects/vscode-snippets'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- Python source files ---
    with open(f'{PROJECT_DIR}/src/models.py', 'w') as f:
        f.write('''"""Domain models for the inventory management system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


class Product:
    def __init__(self, sku: str, name: str, price: float, category: str):
        self.sku = sku
        self.name = name
        self.price = price
        self.category = category
        self.created_at = datetime.now()

    def apply_discount(self, percent: float) -> float:
        discount = self.price * (percent / 100)
        return self.price - discount

    def __repr__(self):
        return f"Product(sku={self.sku!r}, name={self.name!r}, price={self.price})"


class Warehouse:
    def __init__(self, location: str, capacity: int):
        self.location = location
        self.capacity = capacity
        self.inventory: dict = {}

    def add_stock(self, product: Product, quantity: int):
        if product.sku in self.inventory:
            self.inventory[product.sku] += quantity
        else:
            self.inventory[product.sku] = quantity

    def get_stock_level(self, sku: str) -> int:
        return self.inventory.get(sku, 0)
''')

    with open(f'{PROJECT_DIR}/src/handlers.py', 'w') as f:
        f.write('''"""Request handlers for the inventory API."""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def handle_create_order(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Process a new order creation request."""
    try:
        order_id = payload.get("order_id")
        items = payload.get("items", [])
        if not order_id or not items:
            return {"status": "error", "message": "Missing required fields"}

        total = sum(item["price"] * item["quantity"] for item in items)
        logger.info(f"Order {order_id} created with total: ${total:.2f}")
        return {"status": "success", "order_id": order_id, "total": total}

    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        return {"status": "error", "message": str(e)}


def handle_update_inventory(warehouse, sku: str, delta: int) -> bool:
    """Update inventory levels for a specific SKU."""
    current = warehouse.get_stock_level(sku)
    if current + delta < 0:
        logger.warning(f"Insufficient stock for {sku}: have {current}, need {abs(delta)}")
        return False
    warehouse.add_stock_delta(sku, delta)
    return True
''')

    with open(f'{PROJECT_DIR}/tests/test_models.py', 'w') as f:
        f.write('''"""Tests for domain models."""

import pytest
from src.models import Product, Warehouse


class TestProduct:
    def test_apply_discount(self):
        p = Product("SKU001", "Widget", 100.0, "Hardware")
        assert p.apply_discount(10) == 90.0

    def test_repr(self):
        p = Product("SKU002", "Gadget", 49.99, "Electronics")
        assert "SKU002" in repr(p)


class TestWarehouse:
    def test_add_stock(self):
        wh = Warehouse("Building A", 1000)
        p = Product("SKU001", "Widget", 10.0, "Hardware")
        wh.add_stock(p, 50)
        assert wh.get_stock_level("SKU001") == 50

    def test_empty_stock(self):
        wh = Warehouse("Building B", 500)
        assert wh.get_stock_level("NONEXIST") == 0
''')

    # --- TypeScript / React source files ---
    with open(f'{PROJECT_DIR}/src/components/Dashboard.tsx', 'w') as f:
        f.write('''import React, { useState, useEffect } from "react";

interface DashboardProps {
  userId: string;
  refreshInterval?: number;
}

interface MetricsData {
  totalOrders: number;
  revenue: number;
  activeUsers: number;
}

const Dashboard: React.FC<DashboardProps> = ({ userId, refreshInterval = 30000 }) => {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch(`/api/metrics/${userId}`);
        const data = await response.json();
        setMetrics(data);
      } catch (error) {
        console.error("Failed to fetch metrics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, refreshInterval);
    return () => clearInterval(interval);
  }, [userId, refreshInterval]);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      {metrics && (
        <div className="metrics-grid">
          <div className="metric-card">
            <span className="label">Total Orders</span>
            <span className="value">{metrics.totalOrders}</span>
          </div>
          <div className="metric-card">
            <span className="label">Revenue</span>
            <span className="value">${metrics.revenue.toLocaleString()}</span>
          </div>
          <div className="metric-card">
            <span className="label">Active Users</span>
            <span className="value">{metrics.activeUsers}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
''')

    with open(f'{PROJECT_DIR}/src/components/ProductList.tsx', 'w') as f:
        f.write('''import React, { useState } from "react";

interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

interface ProductListProps {
  products: Product[];
  onSelect: (product: Product) => void;
}

const ProductList: React.FC<ProductListProps> = ({ products, onSelect }) => {
  const [filter, setFilter] = useState("");

  const filtered = products.filter(
    (p) =>
      p.name.toLowerCase().includes(filter.toLowerCase()) ||
      p.category.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="product-list">
      <input
        type="text"
        placeholder="Search products..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <ul>
        {filtered.map((product) => (
          <li key={product.id} onClick={() => onSelect(product)}>
            <span className="name">{product.name}</span>
            <span className="price">${product.price.toFixed(2)}</span>
            <span className={`stock ${product.inStock ? "in" : "out"}`}>
              {product.inStock ? "In Stock" : "Out of Stock"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;
''')

    # --- Config files ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump({
            "name": "vscode-snippets",
            "version": "1.0.0",
            "description": "Inventory management system",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "pytest tests/ && react-scripts test"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@reduxjs/toolkit": "^1.9.5"
            }
        }, f, indent=2)

    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump({
            "compilerOptions": {
                "target": "es2020",
                "module": "commonjs",
                "jsx": "react-jsx",
                "strict": True,
                "outDir": "./dist",
                "rootDir": "./src"
            },
            "include": ["src/**/*"]
        }, f, indent=2)

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('pytest>=7.0.0\ndataclasses-json>=0.5.7\naiohttp>=3.8.0\n')

    # Ensure NO custom snippets exist
    snippets_dir = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets')
    if os.path.exists(snippets_dir):
        import shutil
        shutil.rmtree(snippets_dir)

    # Ensure NO .vscode directory with snippets in the project
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial workspace created: {PROJECT_DIR}')
    print(f'Files:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fname in files:
            print(f'  {os.path.join(root, fname)}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
