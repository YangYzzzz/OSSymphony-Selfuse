"""
Initial Setup: Set up a complete load testing pipeline with k6
Task ID: vscode_gf3_087
Domain: vscode

Creates a realistic API service project structure WITHOUT k6 scripts,
VSCode tasks, or GitHub Actions workflows. The agent must create those.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_087'
PROJECT_DIR = f'{WORKDIR}/projects/api-service'


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
    # --- Create project directory structure ---
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "api-service",
        "version": "2.4.1",
        "description": "RESTful API service for inventory management platform",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0",
            "joi": "^17.11.0",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.1",
            "eslint": "^8.53.0",
            "supertest": "^6.3.3"
        },
        "engines": {
            "node": ">=18.0.0"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/index.js ---
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write('''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const mongoose = require('mongoose');
require('dotenv').config();

const productRoutes = require('./routes/products');
const orderRoutes = require('./routes/orders');
const authRoutes = require('./routes/auth');
const { errorHandler } = require('./middleware/errorHandler');
const { rateLimiter } = require('./middleware/rateLimiter');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(rateLimiter);

// Routes
app.use('/api/v1/products', productRoutes);
app.use('/api/v1/orders', orderRoutes);
app.use('/api/v1/auth', authRoutes);

// Health check
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

// Error handling
app.use(errorHandler);

// Database connection and server start
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/inventory')
    .then(() => {
        console.log('Connected to MongoDB');
        app.listen(PORT, () => {
            console.log(`API service running on port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('Database connection failed:', err.message);
        process.exit(1);
    });

module.exports = app;
''')

    # --- src/routes/products.js ---
    with open(f'{PROJECT_DIR}/src/routes/products.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();
const Product = require('../models/Product');
const { authenticate } = require('../middleware/auth');
const Joi = require('joi');

const productSchema = Joi.object({
    name: Joi.string().required().min(2).max(200),
    sku: Joi.string().required().pattern(/^[A-Z]{2,4}-\\d{4,6}$/),
    price: Joi.number().required().min(0),
    quantity: Joi.number().integer().min(0).default(0),
    category: Joi.string().required(),
    warehouse: Joi.string().required()
});

router.get('/', async (req, res, next) => {
    try {
        const { page = 1, limit = 20, category, warehouse } = req.query;
        const filter = {};
        if (category) filter.category = category;
        if (warehouse) filter.warehouse = warehouse;

        const products = await Product.find(filter)
            .skip((page - 1) * limit)
            .limit(parseInt(limit))
            .sort({ updatedAt: -1 });

        const total = await Product.countDocuments(filter);
        res.json({ products, total, page: parseInt(page), pages: Math.ceil(total / limit) });
    } catch (err) {
        next(err);
    }
});

router.post('/', authenticate, async (req, res, next) => {
    try {
        const { error, value } = productSchema.validate(req.body);
        if (error) return res.status(400).json({ error: error.details[0].message });

        const product = new Product(value);
        await product.save();
        res.status(201).json(product);
    } catch (err) {
        next(err);
    }
});

router.get('/:id', async (req, res, next) => {
    try {
        const product = await Product.findById(req.params.id);
        if (!product) return res.status(404).json({ error: 'Product not found' });
        res.json(product);
    } catch (err) {
        next(err);
    }
});

router.put('/:id', authenticate, async (req, res, next) => {
    try {
        const { error, value } = productSchema.validate(req.body);
        if (error) return res.status(400).json({ error: error.details[0].message });

        const product = await Product.findByIdAndUpdate(req.params.id, value, { new: true });
        if (!product) return res.status(404).json({ error: 'Product not found' });
        res.json(product);
    } catch (err) {
        next(err);
    }
});

router.delete('/:id', authenticate, async (req, res, next) => {
    try {
        const product = await Product.findByIdAndDelete(req.params.id);
        if (!product) return res.status(404).json({ error: 'Product not found' });
        res.status(204).send();
    } catch (err) {
        next(err);
    }
});

module.exports = router;
''')

    # --- src/routes/orders.js ---
    with open(f'{PROJECT_DIR}/src/routes/orders.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, async (req, res) => {
    res.json({ orders: [], total: 0 });
});

router.post('/', authenticate, async (req, res) => {
    res.status(201).json({ message: 'Order created' });
});

module.exports = router;
''')

    # --- src/routes/auth.js ---
    with open(f'{PROJECT_DIR}/src/routes/auth.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    // Authentication logic placeholder
    const token = jwt.sign({ email }, process.env.JWT_SECRET || 'dev-secret', { expiresIn: '24h' });
    res.json({ token, expiresIn: 86400 });
});

router.post('/register', async (req, res) => {
    const { email, password, name } = req.body;
    const hashedPassword = await bcrypt.hash(password, 12);
    res.status(201).json({ message: 'User registered successfully' });
});

module.exports = router;
''')

    # --- src/models/Product.js ---
    with open(f'{PROJECT_DIR}/src/models/Product.js', 'w') as f:
        f.write('''const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: { type: String, required: true, index: true },
    sku: { type: String, required: true, unique: true },
    price: { type: Number, required: true, min: 0 },
    quantity: { type: Number, default: 0, min: 0 },
    category: { type: String, required: true, index: true },
    warehouse: { type: String, required: true },
    description: { type: String, maxlength: 1000 },
    tags: [String],
    isActive: { type: Boolean, default: true }
}, {
    timestamps: true
});

productSchema.index({ category: 1, warehouse: 1 });

module.exports = mongoose.model('Product', productSchema);
''')

    # --- src/middleware/errorHandler.js ---
    with open(f'{PROJECT_DIR}/src/middleware/errorHandler.js', 'w') as f:
        f.write('''function errorHandler(err, req, res, next) {
    console.error(`[${new Date().toISOString()}] Error:`, err.message);

    if (err.name === 'ValidationError') {
        return res.status(400).json({ error: 'Validation failed', details: err.message });
    }

    if (err.name === 'CastError') {
        return res.status(400).json({ error: 'Invalid ID format' });
    }

    if (err.code === 11000) {
        return res.status(409).json({ error: 'Duplicate entry' });
    }

    res.status(500).json({ error: 'Internal server error' });
}

module.exports = { errorHandler };
''')

    # --- src/middleware/rateLimiter.js ---
    with open(f'{PROJECT_DIR}/src/middleware/rateLimiter.js', 'w') as f:
        f.write('''const requestCounts = new Map();

function rateLimiter(req, res, next) {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    const windowMs = 15 * 60 * 1000; // 15 minutes
    const maxRequests = 100;

    if (!requestCounts.has(ip)) {
        requestCounts.set(ip, []);
    }

    const timestamps = requestCounts.get(ip).filter(t => now - t < windowMs);
    timestamps.push(now);
    requestCounts.set(ip, timestamps);

    if (timestamps.length > maxRequests) {
        return res.status(429).json({ error: 'Too many requests, please try again later' });
    }

    next();
}

module.exports = { rateLimiter };
''')

    # --- src/middleware/auth.js ---
    with open(f'{PROJECT_DIR}/src/middleware/auth.js', 'w') as f:
        f.write('''const jwt = require('jsonwebtoken');

function authenticate(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Authentication required' });
    }

    try {
        const token = authHeader.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'dev-secret');
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(401).json({ error: 'Invalid or expired token' });
    }
}

module.exports = { authenticate };
''')

    # --- config/default.json ---
    config = {
        "server": {
            "port": 3000,
            "host": "0.0.0.0"
        },
        "database": {
            "uri": "mongodb://localhost:27017/inventory",
            "options": {
                "maxPoolSize": 10,
                "serverSelectionTimeoutMS": 5000
            }
        },
        "auth": {
            "jwtExpiry": "24h",
            "saltRounds": 12
        },
        "logging": {
            "level": "info",
            "format": "combined"
        }
    }
    with open(f'{PROJECT_DIR}/config/default.json', 'w') as f:
        json.dump(config, f, indent=2)

    # --- .env.example ---
    with open(f'{PROJECT_DIR}/.env.example', 'w') as f:
        f.write('''PORT=3000
MONGODB_URI=mongodb://localhost:27017/inventory
JWT_SECRET=your-secret-key-here
NODE_ENV=development
LOG_LEVEL=info
''')

    # --- tests/products.test.js ---
    with open(f'{PROJECT_DIR}/tests/products.test.js', 'w') as f:
        f.write('''const request = require('supertest');
const app = require('../src/index');

describe('Products API', () => {
    describe('GET /api/v1/products', () => {
        it('should return paginated product list', async () => {
            const res = await request(app).get('/api/v1/products');
            expect(res.status).toBe(200);
            expect(res.body).toHaveProperty('products');
            expect(res.body).toHaveProperty('total');
        });

        it('should filter by category', async () => {
            const res = await request(app).get('/api/v1/products?category=electronics');
            expect(res.status).toBe(200);
        });
    });

    describe('GET /health', () => {
        it('should return health status', async () => {
            const res = await request(app).get('/health');
            expect(res.status).toBe(200);
            expect(res.body.status).toBe('healthy');
        });
    });
});
''')

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# API Service - Inventory Management

RESTful API service for the inventory management platform. Built with Express.js and MongoDB.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/products | List products (paginated) |
| POST | /api/v1/products | Create product |
| GET | /api/v1/products/:id | Get product by ID |
| PUT | /api/v1/products/:id | Update product |
| DELETE | /api/v1/products/:id | Delete product |
| GET | /health | Health check |

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

## Testing

```bash
npm test
```

## Deployment

The service is deployed via GitHub Actions to staging and production environments.
Staging deploys happen automatically on push to the `develop` branch.
Production deploys require manual approval after staging verification.
''')

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''node_modules/
.env
coverage/
dist/
*.log
.DS_Store
''')

    # --- Existing GitHub Actions workflow (CI only, no k6) ---
    os.makedirs(f'{PROJECT_DIR}/.github/workflows', exist_ok=True)
    with open(f'{PROJECT_DIR}/.github/workflows/ci.yml', 'w') as f:
        f.write('''name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:7
        ports:
          - 27017:27017

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci --production

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment..."
          # Deploy script placeholder
''')

    print(f'Initial project created: {PROJECT_DIR}')

    # --- GUI-ready startup: Open VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
