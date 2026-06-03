"""
Initial Setup: Create a JavaScript project for TypeScript migration workflow
Task ID: vscode_wf_074
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_074'
PROJECT_DIR = f'{WORKDIR}/project'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # --- package.json (no typescript, no @types) ---
    package_json = {
        "name": "inventory-tracker",
        "version": "1.0.0",
        "description": "Product inventory tracking system with REST API",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "node --watch src/index.js"
        },
        "keywords": ["inventory", "tracker", "api"],
        "author": "Sarah Chen",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/index.js (plain JavaScript, no type annotations) ---
    index_js = '''\
const express = require('express');
const cors = require('cors');
const { formatCurrency, calculateDiscount, validateProduct } = require('./utils');
const { fetchProducts, updateInventory, getProductStats } = require('./api');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

let inventory = [];

app.get('/products', async (req, res) => {
    try {
        const products = await fetchProducts();
        const formatted = products.map(p => ({
            ...p,
            price: formatCurrency(p.price),
            discountedPrice: formatCurrency(calculateDiscount(p.price, p.discount))
        }));
        res.json(formatted);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.post('/products', (req, res) => {
    const product = req.body;
    const validation = validateProduct(product);
    if (!validation.valid) {
        return res.status(400).json({ errors: validation.errors });
    }
    inventory.push({ ...product, id: inventory.length + 1, createdAt: new Date() });
    res.status(201).json(product);
});

app.put('/inventory/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const { quantity } = req.body;
    try {
        const result = await updateInventory(id, quantity);
        res.json(result);
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
});

app.get('/stats', async (req, res) => {
    const stats = await getProductStats();
    res.json(stats);
});

app.listen(PORT, () => {
    console.log(`Inventory tracker running on port ${PORT}`);
});

module.exports = app;
'''
    with open(f'{SRC_DIR}/index.js', 'w') as f:
        f.write(index_js)

    # --- src/utils.js (plain JavaScript utility functions) ---
    utils_js = '''\
function formatCurrency(amount) {
    if (typeof amount !== 'number' || isNaN(amount)) {
        return '$0.00';
    }
    return '$' + amount.toFixed(2);
}

function calculateDiscount(price, discountPercent) {
    if (!discountPercent || discountPercent < 0 || discountPercent > 100) {
        return price;
    }
    return price * (1 - discountPercent / 100);
}

function validateProduct(product) {
    const errors = [];

    if (!product.name || product.name.trim().length === 0) {
        errors.push('Product name is required');
    }

    if (typeof product.price !== 'number' || product.price <= 0) {
        errors.push('Price must be a positive number');
    }

    if (product.quantity !== undefined && (!Number.isInteger(product.quantity) || product.quantity < 0)) {
        errors.push('Quantity must be a non-negative integer');
    }

    if (product.category && typeof product.category !== 'string') {
        errors.push('Category must be a string');
    }

    return {
        valid: errors.length === 0,
        errors: errors
    };
}

function generateSKU(category, id) {
    const prefix = category ? category.substring(0, 3).toUpperCase() : 'GEN';
    return prefix + '-' + String(id).padStart(6, '0');
}

module.exports = {
    formatCurrency,
    calculateDiscount,
    validateProduct,
    generateSKU
};
'''
    with open(f'{SRC_DIR}/utils.js', 'w') as f:
        f.write(utils_js)

    # --- src/api.js (plain JavaScript API functions) ---
    api_js = '''\
const MOCK_PRODUCTS = [
    { id: 1, name: 'Wireless Keyboard', price: 79.99, quantity: 150, category: 'Electronics', discount: 10 },
    { id: 2, name: 'Ergonomic Mouse', price: 45.50, quantity: 230, category: 'Electronics', discount: 0 },
    { id: 3, name: 'USB-C Hub', price: 34.99, quantity: 89, category: 'Accessories', discount: 15 },
    { id: 4, name: 'Monitor Stand', price: 62.00, quantity: 45, category: 'Furniture', discount: 5 },
    { id: 5, name: 'Desk Lamp', price: 28.75, quantity: 312, category: 'Furniture', discount: 0 },
    { id: 6, name: 'Webcam HD', price: 95.00, quantity: 67, category: 'Electronics', discount: 20 },
    { id: 7, name: 'Cable Organizer', price: 12.99, quantity: 500, category: 'Accessories', discount: 0 },
    { id: 8, name: 'Laptop Stand', price: 55.00, quantity: 178, category: 'Furniture', discount: 10 },
];

async function fetchProducts() {
    return new Promise((resolve) => {
        setTimeout(() => resolve(MOCK_PRODUCTS), 100);
    });
}

async function updateInventory(productId, newQuantity) {
    return new Promise((resolve, reject) => {
        const product = MOCK_PRODUCTS.find(p => p.id === productId);
        if (!product) {
            reject(new Error('Product not found with id: ' + productId));
            return;
        }
        product.quantity = newQuantity;
        resolve({ ...product, updatedAt: new Date().toISOString() });
    });
}

async function getProductStats() {
    const products = await fetchProducts();
    const totalValue = products.reduce((sum, p) => sum + p.price * p.quantity, 0);
    const avgPrice = products.reduce((sum, p) => sum + p.price, 0) / products.length;
    const lowStock = products.filter(p => p.quantity < 100);
    const categoryCount = {};
    products.forEach(p => {
        categoryCount[p.category] = (categoryCount[p.category] || 0) + 1;
    });

    return {
        totalProducts: products.length,
        totalInventoryValue: totalValue,
        averagePrice: avgPrice,
        lowStockItems: lowStock.length,
        categorySummary: categoryCount
    };
}

module.exports = {
    fetchProducts,
    updateInventory,
    getProductStats
};
'''
    with open(f'{SRC_DIR}/api.js', 'w') as f:
        f.write(api_js)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: package.json, src/index.js, src/utils.js, src/api.js')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
