"""
Initial Setup: Enable JavaScript type checking via jsconfig.json
Task ID: vscode_lp_006
Domain: vscode

Creates a realistic JS project workspace ~/projects/js-app/ with several .js files.
No jsconfig.json exists. VSCode is opened with the workspace folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'js-app')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # --- package.json ---
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write("""{
  "name": "js-app",
  "version": "1.2.0",
  "description": "Inventory management dashboard for warehouse operations",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "node tests/run.js"
  },
  "author": "Elena Rodriguez",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3"
  }
}
""")

    # --- src/index.js (main entry with intentional type issues) ---
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write("""const express = require('express');
const { connectDatabase } = require('./database');
const { InventoryService } = require('./services/inventoryService');

const app = express();
const PORT = process.env.PORT || 3200;

app.use(express.json());

async function startServer() {
    const db = await connectDatabase();
    const inventoryService = new InventoryService(db);

    app.get('/api/products', async (req, res) => {
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 25;
        const products = await inventoryService.listProducts(page, limit);
        res.json({ data: products, page: page, totalPages: 10 });
    });

    app.post('/api/products', async (req, res) => {
        const { name, sku, quantity, price } = req.body;
        // Type issue: quantity could be string from request body
        const total = quantity * price;
        const product = await inventoryService.addProduct(name, sku, quantity, price, total);
        res.status(201).json(product);
    });

    app.put('/api/products/:id/restock', async (req, res) => {
        const productId = req.params.id;
        const additionalQty = req.body.quantity;
        // Type issue: mixing number and potentially undefined
        const updated = await inventoryService.restock(productId, additionalQty);
        res.json(updated);
    });

    app.listen(PORT, () => {
        console.log(`Warehouse API running on port ${PORT}`);
    });
}

startServer().catch(err => {
    console.error('Failed to start server:', err);
    process.exit(1);
});
""")

    # --- src/database.js ---
    with open(os.path.join(PROJECT_DIR, 'src', 'database.js'), 'w') as f:
        f.write("""const { Pool } = require('pg');

const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME || 'warehouse',
    user: process.env.DB_USER || 'admin',
    password: process.env.DB_PASS || 'secret',
});

async function connectDatabase() {
    try {
        const client = await pool.connect();
        console.log('Connected to warehouse database');
        return client;
    } catch (error) {
        console.error('Database connection failed:', error.message);
        throw error;
    }
}

async function runQuery(query, params) {
    const result = await pool.query(query, params);
    return result.rows;
}

module.exports = { connectDatabase, runQuery, pool };
""")

    # --- src/services/inventoryService.js ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'inventoryService.js'), 'w') as f:
        f.write("""class InventoryService {
    constructor(dbClient) {
        this.db = dbClient;
        this.lowStockThreshold = 10;
    }

    async listProducts(page, limit) {
        const offset = (page - 1) * limit;
        const query = 'SELECT * FROM products ORDER BY name LIMIT $1 OFFSET $2';
        return await this.db.query(query, [limit, offset]);
    }

    async addProduct(name, sku, quantity, price, total) {
        const query = `
            INSERT INTO products (name, sku, quantity, price, total_value)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *`;
        const result = await this.db.query(query, [name, sku, quantity, price, total]);
        return result.rows[0];
    }

    async restock(productId, additionalQty) {
        const query = `
            UPDATE products
            SET quantity = quantity + $1, updated_at = NOW()
            WHERE id = $2
            RETURNING *`;
        const result = await this.db.query(query, [additionalQty, productId]);
        if (result.rows.length === 0) {
            throw new Error('Product not found: ' + productId);
        }
        return result.rows[0];
    }

    async getLowStockItems() {
        const query = 'SELECT * FROM products WHERE quantity < $1 ORDER BY quantity ASC';
        return await this.db.query(query, [this.lowStockThreshold]);
    }

    calculateReorderCost(items) {
        // Type issue: items might not have the expected shape
        let totalCost = 0;
        for (const item of items) {
            const reorderQty = this.lowStockThreshold * 2 - item.quantity;
            totalCost += reorderQty * item.price;
        }
        return totalCost;
    }
}

module.exports = { InventoryService };
""")

    # --- src/utils/formatter.js ---
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'formatter.js'), 'w') as f:
        f.write("""/**
 * Format currency values for display
 * @param {number} amount
 * @param {string} currency
 * @returns {string}
 */
function formatCurrency(amount, currency) {
    // Type issue: amount could be string
    const formatted = amount.toFixed(2);
    const symbols = { USD: '$', EUR: '\\u20ac', GBP: '\\u00a3' };
    const symbol = symbols[currency] || currency;
    return symbol + formatted;
}

/**
 * Format date for warehouse reports
 * @param {Date} date
 * @returns {string}
 */
function formatReportDate(date) {
    const options = { year: 'numeric', month: 'short', day: '2-digit' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Generate SKU from product details
 * @param {string} category
 * @param {number} id
 */
function generateSku(category, id) {
    const prefix = category.substring(0, 3).toUpperCase();
    const padded = String(id).padStart(6, '0');
    return prefix + '-' + padded;
}

module.exports = { formatCurrency, formatReportDate, generateSku };
""")

    # --- tests/run.js ---
    with open(os.path.join(PROJECT_DIR, 'tests', 'run.js'), 'w') as f:
        f.write("""const { formatCurrency, generateSku } = require('../src/utils/formatter');

function assertEqual(actual, expected, label) {
    if (actual !== expected) {
        console.error(`FAIL: ${label} - expected "${expected}", got "${actual}"`);
        return false;
    }
    console.log(`PASS: ${label}`);
    return true;
}

let passed = 0;
let total = 0;

total++;
if (assertEqual(formatCurrency(49.99, 'USD'), '$49.99', 'formatCurrency USD')) passed++;

total++;
if (assertEqual(generateSku('Electronics', 42), 'ELE-000042', 'generateSku')) passed++;

total++;
if (assertEqual(formatCurrency(1200, 'EUR'), '\\u20ac1200.00', 'formatCurrency EUR')) passed++;

console.log(`\\nResults: ${passed}/${total} tests passed`);
process.exit(passed === total ? 0 : 1);
""")

    # --- .gitignore ---
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("""node_modules/
.env
*.log
dist/
""")

    # Ensure NO jsconfig.json exists (negative constraint)
    jsconfig_path = os.path.join(PROJECT_DIR, 'jsconfig.json')
    if os.path.exists(jsconfig_path):
        os.remove(jsconfig_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print('Files created:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), PROJECT_DIR)
            print(f'  {rel}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
