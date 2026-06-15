"""
Initial Setup: Git rebase workflow with VSCode
Task ID: vscode_gf2_045
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_045'
PROJECT_DIR = f'{WORKDIR}/projects/node-api'


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


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result.stdout.strip()


def create_project():
    """Create a realistic Node.js API project with 3 WIP commits."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Initialize git repo
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Developer"', cwd=PROJECT_DIR)

    # --- Base commit: project skeleton ---
    package_json = {
        "name": "node-api",
        "version": "1.0.0",
        "description": "REST API for inventory management",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "test": "jest --verbose",
            "dev": "nodemon index.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "mongoose": "^7.6.3"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "supertest": "^6.3.3",
            "nodemon": "^3.0.1"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("node_modules/\n.env\ncoverage/\n*.log\n")

    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("# Node API\n\nREST API for inventory management system.\n\n## Setup\n\n```bash\nnpm install\nnpm start\n```\n")

    with open(f'{PROJECT_DIR}/index.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
""")

    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial project setup with Express server"', cwd=PROJECT_DIR)

    # --- WIP Commit 1: start feature ---
    with open(f'{PROJECT_DIR}/src/routes.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();

// GET /api/products - List all products
router.get('/products', async (req, res) => {
    try {
        const products = [
            { id: 1, name: 'Wireless Keyboard', price: 49.99, stock: 150 },
            { id: 2, name: 'USB-C Hub', price: 34.99, stock: 89 },
            { id: 3, name: 'Monitor Stand', price: 79.99, stock: 42 },
            { id: 4, name: 'Webcam HD', price: 64.99, stock: 203 },
            { id: 5, name: 'Desk Lamp LED', price: 29.99, stock: 67 },
        ];
        res.json({ success: true, data: products, count: products.length });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// POST /api/products - Create a new product
router.post('/products', async (req, res) => {
    const { name, price, stock } = req.body;
    if (!name || price === undefined) {
        return res.status(400).json({ success: false, error: 'Name and price are required' });
    }
    const newProduct = { id: Date.now(), name, price, stock: stock || 0 };
    res.status(201).json({ success: true, data: newProduct });
});

module.exports = router;
""")

    with open(f'{PROJECT_DIR}/src/middleware.js', 'w') as f:
        f.write("""/**
 * Request logging middleware
 */
function requestLogger(req, res, next) {
    const start = Date.now();
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`${req.method} ${req.originalUrl} ${res.statusCode} - ${duration}ms`);
    });
    next();
}

/**
 * Error handling middleware
 */
function errorHandler(err, req, res, next) {
    console.error('Unhandled error:', err.stack);
    res.status(500).json({
        success: false,
        error: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message
    });
}

module.exports = { requestLogger, errorHandler };
""")

    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "WIP: start feature"', cwd=PROJECT_DIR)

    # --- WIP Commit 2: add tests ---
    with open(f'{PROJECT_DIR}/tests/api.test.js', 'w') as f:
        f.write("""const request = require('supertest');
const app = require('../index');

describe('Health Check', () => {
    test('GET /health returns status ok', async () => {
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('ok');
        expect(response.body.timestamp).toBeDefined();
    });
});

describe('Products API', () => {
    test('GET /api/products returns product list', async () => {
        const response = await request(app).get('/api/products');
        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(Array.isArray(response.body.data)).toBe(true);
        expect(response.body.count).toBeGreaterThan(0);
    });

    test('POST /api/products creates a new product', async () => {
        const newProduct = { name: 'Test Widget', price: 19.99, stock: 100 };
        const response = await request(app)
            .post('/api/products')
            .send(newProduct);
        expect(response.status).toBe(201);
        expect(response.body.data.name).toBe('Test Widget');
    });

    test('POST /api/products returns 400 without name', async () => {
        const response = await request(app)
            .post('/api/products')
            .send({ price: 9.99 });
        expect(response.status).toBe(400);
        expect(response.body.success).toBe(false);
    });
});
""")

    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "WIP: add tests"', cwd=PROJECT_DIR)

    # --- WIP Commit 3: fix tests ---
    # Update index.js to wire up routes and middleware
    with open(f'{PROJECT_DIR}/index.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
require('dotenv').config();

const routes = require('./src/routes');
const { requestLogger, errorHandler } = require('./src/middleware');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(requestLogger);

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Mount API routes
app.use('/api', routes);

// Error handling
app.use(errorHandler);

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;
""")

    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "WIP: fix tests"', cwd=PROJECT_DIR)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Git log:')
    log = run_cmd('git log --oneline', cwd=PROJECT_DIR)
    print(log)


def setup_initial():
    create_project()

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


setup_initial()
