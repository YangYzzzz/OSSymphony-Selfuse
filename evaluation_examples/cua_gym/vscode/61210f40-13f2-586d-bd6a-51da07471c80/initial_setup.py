"""
Initial Setup: Rebase feature/api-v2 onto main with conflict in src/routes.js
Task ID: vscode_gs_048
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_048'
PROJECT_DIR = f'{WORKDIR}/projects/api'
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


def run(cmd, cwd=None):
    """Run shell command, print output on failure."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout.strip()


def create_initial():
    # Clean up if exists
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(SRC_DIR, exist_ok=True)

    # Initialize git repo with 'main' as default branch
    run('git init -b main', cwd=PROJECT_DIR)
    run('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Developer"', cwd=PROJECT_DIR)

    # === Base commit (shared ancestor) ===
    # Create project structure
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
  "name": "api-service",
  "version": "1.0.0",
  "description": "REST API service for customer management",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }
}
''')

    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Customer API Service

A RESTful API for managing customer data.

## Endpoints
- GET /api/customers - List all customers
- GET /api/customers/:id - Get customer by ID
- POST /api/customers - Create customer
''')

    with open(f'{SRC_DIR}/index.js', 'w') as f:
        f.write('''const express = require('express');
const cors = require('cors');
const routes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use('/api', routes);

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
''')

    # Initial version of routes.js (shared base)
    with open(f'{SRC_DIR}/routes.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();

// Customer data store
let customers = [
    { id: 1, name: 'Acme Corp', contact: 'alice@acme.com' },
    { id: 2, name: 'Globex Inc', contact: 'bob@globex.com' },
];

// GET all customers
router.get('/customers', (req, res) => {
    res.json(customers);
});

// GET customer by ID
router.get('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    res.json(customer);
});

// POST new customer
router.post('/customers', (req, res) => {
    const { name, contact } = req.body;
    const newCustomer = { id: customers.length + 1, name, contact };
    customers.push(newCustomer);
    res.status(201).json(newCustomer);
});

module.exports = router;
''')

    with open(f'{SRC_DIR}/utils.js', 'w') as f:
        f.write('''// Utility functions

function validateEmail(email) {
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}

function generateId(items) {
    return items.length > 0 ? Math.max(...items.map(i => i.id)) + 1 : 1;
}

module.exports = { validateEmail, generateId };
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Initial project setup with customer API"', cwd=PROJECT_DIR)

    # === Second base commit ===
    with open(f'{SRC_DIR}/middleware.js', 'w') as f:
        f.write('''// Request logging middleware
function requestLogger(req, res, next) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.url}`);
    next();
}

module.exports = { requestLogger };
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add request logging middleware"', cwd=PROJECT_DIR)

    # Now create the feature branch from this point
    run('git checkout -b feature/api-v2', cwd=PROJECT_DIR)

    # === Feature commit 1: Add PUT endpoint (modifies routes.js - will conflict) ===
    with open(f'{SRC_DIR}/routes.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();

// Customer data store
let customers = [
    { id: 1, name: 'Acme Corp', contact: 'alice@acme.com' },
    { id: 2, name: 'Globex Inc', contact: 'bob@globex.com' },
];

// GET all customers
router.get('/customers', (req, res) => {
    res.json(customers);
});

// GET customer by ID
router.get('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    res.json(customer);
});

// POST new customer
router.post('/customers', (req, res) => {
    const { name, contact } = req.body;
    const newCustomer = { id: customers.length + 1, name, contact };
    customers.push(newCustomer);
    res.status(201).json(newCustomer);
});

// PUT update customer
router.put('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    const { name, contact } = req.body;
    if (name) customer.name = name;
    if (contact) customer.contact = contact;
    res.json(customer);
});

module.exports = router;
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add PUT endpoint for updating customers"', cwd=PROJECT_DIR)

    # === Feature commit 2: Add DELETE endpoint ===
    with open(f'{SRC_DIR}/routes.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();

// Customer data store
let customers = [
    { id: 1, name: 'Acme Corp', contact: 'alice@acme.com' },
    { id: 2, name: 'Globex Inc', contact: 'bob@globex.com' },
];

// GET all customers
router.get('/customers', (req, res) => {
    res.json(customers);
});

// GET customer by ID
router.get('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    res.json(customer);
});

// POST new customer
router.post('/customers', (req, res) => {
    const { name, contact } = req.body;
    const newCustomer = { id: customers.length + 1, name, contact };
    customers.push(newCustomer);
    res.status(201).json(newCustomer);
});

// PUT update customer
router.put('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    const { name, contact } = req.body;
    if (name) customer.name = name;
    if (contact) customer.contact = contact;
    res.json(customer);
});

// DELETE customer
router.delete('/customers/:id', (req, res) => {
    const index = customers.findIndex(c => c.id === parseInt(req.params.id));
    if (index === -1) return res.status(404).json({ error: 'Not found' });
    customers.splice(index, 1);
    res.status(204).send();
});

module.exports = router;
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add DELETE endpoint for removing customers"', cwd=PROJECT_DIR)

    # === Feature commit 3: Add validation helper ===
    with open(f'{SRC_DIR}/validators.js', 'w') as f:
        f.write('''// Input validation for API v2

function validateCustomerInput(data) {
    const errors = [];
    if (!data.name || typeof data.name !== 'string') {
        errors.push('Name is required and must be a string');
    }
    if (!data.contact || typeof data.contact !== 'string') {
        errors.push('Contact is required and must be a string');
    }
    if (data.contact && !data.contact.includes('@')) {
        errors.push('Contact must be a valid email address');
    }
    return { valid: errors.length === 0, errors };
}

module.exports = { validateCustomerInput };
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add input validation for customer endpoints"', cwd=PROJECT_DIR)

    # === Feature commit 4: Add error handler ===
    with open(f'{SRC_DIR}/errorHandler.js', 'w') as f:
        f.write('''// Centralized error handling for API v2

class ApiError extends Error {
    constructor(statusCode, message) {
        super(message);
        this.statusCode = statusCode;
    }
}

function errorHandler(err, req, res, next) {
    if (err instanceof ApiError) {
        return res.status(err.statusCode).json({ error: err.message });
    }
    console.error('Unexpected error:', err);
    res.status(500).json({ error: 'Internal server error' });
}

module.exports = { ApiError, errorHandler };
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add centralized error handling"', cwd=PROJECT_DIR)

    # === Go back to main and add 2 commits that create the conflict ===
    run('git checkout main', cwd=PROJECT_DIR)

    # Main commit 1: Add pagination to GET /customers (modifies routes.js - creates conflict)
    with open(f'{SRC_DIR}/routes.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();

// Customer data store
let customers = [
    { id: 1, name: 'Acme Corp', contact: 'alice@acme.com' },
    { id: 2, name: 'Globex Inc', contact: 'bob@globex.com' },
];

// GET all customers with pagination
router.get('/customers', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const start = (page - 1) * limit;
    const end = start + limit;
    const paginated = customers.slice(start, end);
    res.json({
        data: paginated,
        total: customers.length,
        page,
        limit
    });
});

// GET customer by ID
router.get('/customers/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Not found' });
    res.json(customer);
});

// POST new customer
router.post('/customers', (req, res) => {
    const { name, contact } = req.body;
    const newCustomer = { id: customers.length + 1, name, contact };
    customers.push(newCustomer);
    res.status(201).json(newCustomer);
});

module.exports = router;
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add pagination support to customer listing"', cwd=PROJECT_DIR)

    # Main commit 2: Add health check endpoint
    with open(f'{SRC_DIR}/health.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

module.exports = router;
''')

    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add health check endpoint"', cwd=PROJECT_DIR)

    # Switch back to the feature branch for the agent to work on
    run('git checkout feature/api-v2', cwd=PROJECT_DIR)

    # Verify the setup
    log = run('git log --oneline --all --graph', cwd=PROJECT_DIR)
    print("Git history:")
    print(log)

    branch = run('git branch', cwd=PROJECT_DIR)
    print(f"\nBranches:\n{branch}")

    print(f'\nInitial repo created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
