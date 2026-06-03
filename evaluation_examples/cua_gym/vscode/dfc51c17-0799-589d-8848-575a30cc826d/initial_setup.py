"""
Initial Setup: Configure a code review checklist workflow in ~/project
Task ID: vscode_wf_069
Domain: vscode

Creates a JavaScript project with scattered code quality issues but
NO review tooling (no tasks.json, no review.sh, no todo-tree extension).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_069'
PROJECT = os.path.join(WORKDIR, 'project')


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


def create_text_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def create_project():
    # ── package.json ──
    pkg = {
        "name": "inventory-tracker",
        "version": "1.0.0",
        "description": "Product inventory management system",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "lint": "eslint src/",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "eslint": "^8.52.0",
            "jest": "^29.7.0"
        }
    }
    create_text_file(os.path.join(PROJECT, "package.json"), json.dumps(pkg, indent=2))

    # ── .eslintrc.json ──
    eslint_cfg = {
        "env": {"node": True, "es2021": True, "jest": True},
        "extends": "eslint:recommended",
        "parserOptions": {"ecmaVersion": "latest"},
        "rules": {
            "no-console": "warn",
            "no-unused-vars": "warn"
        }
    }
    create_text_file(os.path.join(PROJECT, ".eslintrc.json"), json.dumps(eslint_cfg, indent=2))

    # ── src/index.js ── (has console.log, TODO)
    create_text_file(os.path.join(PROJECT, "src", "index.js"), '''\
const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(express.json());

// TODO: Add authentication middleware
const PORT = process.env.PORT || 3000;

// Import routes
const productRoutes = require('./routes/products');
const categoryRoutes = require('./routes/categories');

app.use('/api/products', productRoutes);
app.use('/api/categories', categoryRoutes);

console.log('Starting inventory tracker server...');

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
''')

    # ── src/routes/products.js ── (has console.log, FIXME)
    create_text_file(os.path.join(PROJECT, "src", "routes", "products.js"), '''\
const express = require('express');
const router = express.Router();
const Product = require('../models/product');

// FIXME: Add input validation for all routes

router.get('/', async (req, res) => {
    try {
        const products = await Product.find();
        console.log('Fetched products:', products.length);
        res.json(products);
    } catch (err) {
        console.log('Error fetching products:', err.message);
        res.status(500).json({ error: err.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const { name, sku, price, quantity, category } = req.body;
        // TODO: Validate required fields before creating
        const product = new Product({ name, sku, price, quantity, category });
        await product.save();
        console.log('Created product:', product.sku);
        res.status(201).json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.put('/:id', async (req, res) => {
    try {
        const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!product) return res.status(404).json({ error: 'Product not found' });
        res.json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        // HACK: Should soft-delete instead of hard delete
        const product = await Product.findByIdAndDelete(req.params.id);
        if (!product) return res.status(404).json({ error: 'Product not found' });
        console.log('Deleted product:', req.params.id);
        res.json({ message: 'Product deleted' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
''')

    # ── src/routes/categories.js ── (has BUG tag)
    create_text_file(os.path.join(PROJECT, "src", "routes", "categories.js"), '''\
const express = require('express');
const router = express.Router();
const Category = require('../models/category');

router.get('/', async (req, res) => {
    try {
        const categories = await Category.find().populate('products');
        res.json(categories);
    } catch (err) {
        // BUG: Error response format inconsistent with products route
        res.status(500).send(err.message);
    }
});

router.post('/', async (req, res) => {
    try {
        const { name, description } = req.body;
        const category = new Category({ name, description });
        await category.save();
        console.log('New category created:', name);
        res.status(201).json(category);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.get('/:id/products', async (req, res) => {
    try {
        const category = await Category.findById(req.params.id);
        if (!category) return res.status(404).json({ error: 'Category not found' });
        // TODO: Add pagination for large product lists
        const products = await Product.find({ category: req.params.id });
        res.json(products);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
''')

    # ── src/models/product.js ──
    create_text_file(os.path.join(PROJECT, "src", "models", "product.js"), '''\
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: { type: String, required: true, trim: true },
    sku: { type: String, required: true, unique: true },
    price: { type: Number, required: true, min: 0 },
    quantity: { type: Number, default: 0, min: 0 },
    category: { type: mongoose.Schema.Types.ObjectId, ref: 'Category' },
    description: { type: String, default: '' },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
});

// TODO: Add pre-save hook to update updatedAt timestamp
productSchema.index({ sku: 1 });
productSchema.index({ category: 1 });

module.exports = mongoose.model('Product', productSchema);
''')

    # ── src/models/category.js ──
    create_text_file(os.path.join(PROJECT, "src", "models", "category.js"), '''\
const mongoose = require('mongoose');

const categorySchema = new mongoose.Schema({
    name: { type: String, required: true, unique: true, trim: true },
    description: { type: String, default: '' },
    isActive: { type: Boolean, default: true },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Category', categorySchema);
''')

    # ── src/utils/helpers.js ── (has console.log, HACK)
    create_text_file(os.path.join(PROJECT, "src", "utils", "helpers.js"), '''\
/**
 * Utility helpers for the inventory tracker
 */

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function generateSKU(category, sequence) {
    const prefix = category.substring(0, 3).toUpperCase();
    const num = String(sequence).padStart(5, '0');
    console.log('Generated SKU:', `${prefix}-${num}`);
    return `${prefix}-${num}`;
}

// HACK: This validation is too basic, needs proper regex
function validateEmail(email) {
    return email.includes('@') && email.includes('.');
}

function calculateDiscount(price, discountPercent) {
    if (discountPercent < 0 || discountPercent > 100) {
        throw new Error('Invalid discount percentage');
    }
    return price * (1 - discountPercent / 100);
}

function paginateResults(items, page = 1, limit = 20) {
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    return {
        data: items.slice(startIndex, endIndex),
        total: items.length,
        page,
        totalPages: Math.ceil(items.length / limit)
    };
}

module.exports = {
    formatCurrency,
    generateSKU,
    validateEmail,
    calculateDiscount,
    paginateResults
};
''')

    # ── src/middleware/errorHandler.js ──
    create_text_file(os.path.join(PROJECT, "src", "middleware", "errorHandler.js"), '''\
/**
 * Global error handling middleware
 */

function errorHandler(err, req, res, next) {
    console.log('Error caught by handler:', err.message);

    const statusCode = err.statusCode || 500;
    const message = err.message || 'Internal Server Error';

    // FIXME: Should not expose stack traces in production
    res.status(statusCode).json({
        error: {
            message,
            stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
        }
    });
}

function notFoundHandler(req, res) {
    res.status(404).json({ error: { message: 'Route not found' } });
}

module.exports = { errorHandler, notFoundHandler };
''')

    # ── src/config/database.js ──
    create_text_file(os.path.join(PROJECT, "src", "config", "database.js"), '''\
const mongoose = require('mongoose');

async function connectDatabase() {
    const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/inventory';
    try {
        await mongoose.connect(uri);
        console.log('Connected to MongoDB');
    } catch (err) {
        console.log('Database connection failed:', err.message);
        // BUG: Process exits without cleanup on connection failure
        process.exit(1);
    }
}

module.exports = { connectDatabase };
''')

    # ── tests/products.test.js ── (only test file; categories has NO test)
    create_text_file(os.path.join(PROJECT, "tests", "products.test.js"), '''\
const request = require('supertest');

describe('Product API', () => {
    // TODO: Set up test database connection

    test('GET /api/products returns array', async () => {
        // Placeholder test
        expect(Array.isArray([])).toBe(true);
    });

    test('POST /api/products creates product', async () => {
        const product = {
            name: 'Test Widget',
            sku: 'TST-00001',
            price: 29.99,
            quantity: 100
        };
        // TODO: Implement actual API test
        expect(product.name).toBeDefined();
    });
});
''')

    # ── README.md ──
    create_text_file(os.path.join(PROJECT, "README.md"), '''\
# Inventory Tracker

A product inventory management system built with Express and MongoDB.

## Getting Started

```bash
npm install
npm start
```

## API Endpoints

- `GET /api/products` - List all products
- `POST /api/products` - Create a product
- `PUT /api/products/:id` - Update a product
- `DELETE /api/products/:id` - Delete a product
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create a category

## Development

```bash
npm run lint    # Run ESLint
npm test        # Run tests with coverage
```
''')

    # ── .env.example ──
    create_text_file(os.path.join(PROJECT, ".env.example"), '''\
PORT=3000
MONGODB_URI=mongodb://localhost:27017/inventory
NODE_ENV=development
''')

    # ── .gitignore ──
    create_text_file(os.path.join(PROJECT, ".gitignore"), '''\
node_modules/
.env
coverage/
dist/
''')

    print(f'Initial project created at: {PROJECT}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
