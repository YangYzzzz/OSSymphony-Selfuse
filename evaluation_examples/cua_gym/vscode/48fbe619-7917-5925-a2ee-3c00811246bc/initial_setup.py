"""
Initial Setup: Set up EditorConfig for ~/project
Task ID: vscode_wf_029
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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

    # Create realistic JavaScript files
    with open(os.path.join(PROJECT_DIR, 'app.js'), 'w') as f:
        f.write("""const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to the Inventory Management API',
        version: '1.2.0',
        endpoints: ['/products', '/orders', '/customers']
    });
});

app.get('/products', (req, res) => {
    const products = [
        { id: 1, name: 'Wireless Keyboard', price: 49.99, stock: 150 },
        { id: 2, name: 'USB-C Hub', price: 34.50, stock: 230 },
        { id: 3, name: 'Monitor Stand', price: 79.00, stock: 85 },
    ];
    res.json(products);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
""")

    # Create a TypeScript file
    with open(os.path.join(PROJECT_DIR, 'types.ts'), 'w') as f:
        f.write("""export interface Product {
    id: number;
    name: string;
    price: number;
    stock: number;
    category: string;
}

export interface Order {
    orderId: string;
    customerId: number;
    products: OrderItem[];
    totalAmount: number;
    status: 'pending' | 'shipped' | 'delivered' | 'cancelled';
    createdAt: Date;
}

export interface OrderItem {
    productId: number;
    quantity: number;
    unitPrice: number;
}

export interface Customer {
    id: number;
    firstName: string;
    lastName: string;
    email: string;
    registeredAt: Date;
}

export type SortDirection = 'asc' | 'desc';

export function formatCurrency(amount: number): string {
    return `$${amount.toFixed(2)}`;
}
""")

    # Create Python files
    with open(os.path.join(PROJECT_DIR, 'analytics.py'), 'w') as f:
        f.write("""import csv
import statistics
from datetime import datetime, timedelta
from collections import defaultdict


class SalesAnalytics:
    \"\"\"Analyze sales data for quarterly reports.\"\"\"

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.records = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append({
                    'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                    'product': row['product'],
                    'quantity': int(row['quantity']),
                    'revenue': float(row['revenue']),
                    'region': row['region'],
                })

    def total_revenue(self) -> float:
        return sum(r['revenue'] for r in self.records)

    def revenue_by_region(self) -> dict:
        result = defaultdict(float)
        for r in self.records:
            result[r['region']] += r['revenue']
        return dict(result)

    def top_products(self, n: int = 5) -> list:
        product_revenue = defaultdict(float)
        for r in self.records:
            product_revenue[r['product']] += r['revenue']
        sorted_products = sorted(
            product_revenue.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_products[:n]

    def average_daily_revenue(self) -> float:
        daily = defaultdict(float)
        for r in self.records:
            daily[r['date'].date()] += r['revenue']
        return statistics.mean(daily.values()) if daily else 0.0


if __name__ == '__main__':
    analyzer = SalesAnalytics('sales_data.csv')
    print(f"Total Revenue: ${analyzer.total_revenue():,.2f}")
    print(f"Average Daily Revenue: ${analyzer.average_daily_revenue():,.2f}")
    print("\\nTop 5 Products:")
    for product, revenue in analyzer.top_products():
        print(f"  {product}: ${revenue:,.2f}")
""")

    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write("""import os
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def compute_file_hash(filepath: str, algorithm: str = 'sha256') -> str:
    \"\"\"Compute the hash of a file using the specified algorithm.\"\"\"
    hasher = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def ensure_directory(path: str) -> Path:
    \"\"\"Create directory if it doesn't exist, return Path object.\"\"\"
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_read_file(filepath: str, default: str = '') -> str:
    \"\"\"Read a file, returning default if it doesn't exist.\"\"\"
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"File not found: {filepath}")
        return default


def format_filesize(size_bytes: int) -> str:
    \"\"\"Format file size in human-readable format.\"\"\"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
""")

    # Create a package.json for realism
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write("""{
    "name": "inventory-management-api",
    "version": "1.2.0",
    "description": "REST API for inventory management system",
    "main": "app.js",
    "scripts": {
        "start": "node app.js",
        "dev": "nodemon app.js",
        "test": "jest"
    },
    "dependencies": {
        "express": "^4.18.2"
    },
    "devDependencies": {
        "jest": "^29.7.0",
        "nodemon": "^3.0.1"
    }
}
""")

    # Ensure NO .editorconfig exists (negative constraint)
    editorconfig_path = os.path.join(PROJECT_DIR, '.editorconfig')
    if os.path.exists(editorconfig_path):
        os.remove(editorconfig_path)

    # Ensure EditorConfig extension is NOT installed
    subprocess.run(
        ['code', '--uninstall-extension', 'editorconfig.editorconfig'],
        capture_output=True, text=True
    )

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: app.js, types.ts, analytics.py, utils.py, package.json')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
