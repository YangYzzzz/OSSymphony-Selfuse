"""
Initial Setup: Configure JavaScript import suggestions and auto-import updates
Task ID: vscode_lp_052
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_052'
WORKSPACE = f'{WORKDIR}/workspace'
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


def create_workspace():
    """Create a realistic JavaScript project workspace."""
    # Create directory structure
    dirs = [
        f'{WORKSPACE}/src',
        f'{WORKSPACE}/src/components',
        f'{WORKSPACE}/src/utils',
        f'{WORKSPACE}/src/services',
        f'{WORKSPACE}/src/models',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.2.0",
        "description": "Warehouse inventory tracking dashboard",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "lodash": "^4.17.21",
            "moment": "^2.29.4"
        }
    }
    with open(f'{WORKSPACE}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js - main entry point with absolute-style imports
    with open(f'{WORKSPACE}/src/index.js', 'w') as f:
        f.write("""const express = require('express');
const { formatCurrency, calculateDiscount } = require('./utils/helper');
const { InventoryService } = require('./services/inventoryService');
const { Product } = require('./models/product');

const app = express();
const PORT = 3000;

app.get('/api/products', async (req, res) => {
    const service = new InventoryService();
    const products = await service.getAllProducts();
    const formatted = products.map(p => ({
        ...p,
        price: formatCurrency(p.price),
        discountedPrice: formatCurrency(calculateDiscount(p.price, p.discount))
    }));
    res.json(formatted);
});

app.get('/api/products/:id', async (req, res) => {
    const service = new InventoryService();
    const product = await service.getProductById(req.params.id);
    if (!product) {
        return res.status(404).json({ error: 'Product not found' });
    }
    res.json(product);
});

app.listen(PORT, () => {
    console.log(`Inventory dashboard running on port ${PORT}`);
});
""")

    # src/utils/helper.js
    with open(f'{WORKSPACE}/src/utils/helper.js', 'w') as f:
        f.write("""/**
 * Utility functions for the inventory dashboard
 */

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function calculateDiscount(price, discountPercent) {
    if (!discountPercent || discountPercent <= 0) return price;
    return price * (1 - discountPercent / 100);
}

function generateSKU(category, id) {
    const prefix = category.substring(0, 3).toUpperCase();
    return `${prefix}-${String(id).padStart(6, '0')}`;
}

function validateQuantity(qty) {
    return Number.isInteger(qty) && qty >= 0;
}

module.exports = {
    formatCurrency,
    calculateDiscount,
    generateSKU,
    validateQuantity
};
""")

    # src/services/inventoryService.js
    with open(f'{WORKSPACE}/src/services/inventoryService.js', 'w') as f:
        f.write("""const { generateSKU, validateQuantity } = require('../utils/helper');
const { Product } = require('../models/product');

class InventoryService {
    constructor() {
        this.products = [
            new Product(1, 'Wireless Keyboard', 'Electronics', 49.99, 150, 10),
            new Product(2, 'Ergonomic Mouse', 'Electronics', 34.95, 230, 0),
            new Product(3, 'Standing Desk Mat', 'Office', 28.50, 75, 15),
            new Product(4, 'USB-C Hub', 'Electronics', 65.00, 42, 5),
            new Product(5, 'Monitor Arm', 'Office', 89.99, 18, 20),
        ];
    }

    async getAllProducts() {
        return this.products.map(p => ({
            id: p.id,
            name: p.name,
            sku: generateSKU(p.category, p.id),
            price: p.price,
            stock: p.stock,
            discount: p.discount
        }));
    }

    async getProductById(id) {
        return this.products.find(p => p.id === parseInt(id));
    }

    async updateStock(id, quantity) {
        if (!validateQuantity(quantity)) {
            throw new Error('Invalid quantity');
        }
        const product = this.products.find(p => p.id === parseInt(id));
        if (product) {
            product.stock = quantity;
            return product;
        }
        return null;
    }
}

module.exports = { InventoryService };
""")

    # src/models/product.js
    with open(f'{WORKSPACE}/src/models/product.js', 'w') as f:
        f.write("""class Product {
    constructor(id, name, category, price, stock, discount = 0) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.price = price;
        this.stock = stock;
        this.discount = discount;
        this.createdAt = new Date();
    }

    isLowStock(threshold = 20) {
        return this.stock <= threshold;
    }

    getDiscountedPrice() {
        if (this.discount <= 0) return this.price;
        return this.price * (1 - this.discount / 100);
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            category: this.category,
            price: this.price,
            stock: this.stock,
            discount: this.discount,
            lowStock: this.isLowStock()
        };
    }
}

module.exports = { Product };
""")

    # src/components/dashboard.js
    with open(f'{WORKSPACE}/src/components/dashboard.js', 'w') as f:
        f.write("""const { InventoryService } = require('../services/inventoryService');
const { formatCurrency } = require('../utils/helper');

class Dashboard {
    constructor() {
        this.service = new InventoryService();
    }

    async renderSummary() {
        const products = await this.service.getAllProducts();
        const totalValue = products.reduce((sum, p) => sum + (p.price * p.stock), 0);
        const lowStockCount = products.filter(p => p.stock < 20).length;

        return {
            totalProducts: products.length,
            totalInventoryValue: formatCurrency(totalValue),
            lowStockAlerts: lowStockCount,
            lastUpdated: new Date().toISOString()
        };
    }
}

module.exports = { Dashboard };
""")

    print(f'Workspace created at: {WORKSPACE}')


def setup_vscode_settings():
    """Set up VSCode with default settings (without the target settings)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Set some baseline settings that do NOT include the target settings
    # Make sure the target settings are NOT present
    settings.pop('javascript.preferences.importModuleSpecifier', None)
    settings.pop('javascript.updateImportsOnFileMove.enabled', None)

    # Add some reasonable defaults for a JS development environment
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": False,
        "files.autoSave": "off",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern"
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written to: {SETTINGS_PATH}')


def main():
    create_workspace()
    setup_vscode_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
