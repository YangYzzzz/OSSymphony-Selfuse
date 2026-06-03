"""
Initial Setup: Multi-environment VSCode configuration system for full-stack app
Task ID: vscode_gf3_095
Domain: vscode

Creates the project structure with env files and validate-env script,
but does NOT create .vscode/launch.json or .vscode/tasks.json (that's the agent's task).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_095'
PROJECT_DIR = f'{WORKDIR}/projects/fullstack'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'

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
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "fullstack-app",
        "version": "2.4.1",
        "description": "Multi-environment full-stack application",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/server.js ---
    server_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Database connection
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

// Routes
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');
const orderRoutes = require('./routes/orders');

app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/orders', orderRoutes);

// Health check
app.get('/health', async (req, res) => {
    try {
        await pool.query('SELECT 1');
        res.json({ status: 'healthy', environment: process.env.NODE_ENV });
    } catch (err) {
        res.status(503).json({ status: 'unhealthy', error: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port} in ${process.env.NODE_ENV} mode`);
});

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/src/server.js', 'w') as f:
        f.write(server_js)

    # --- src/routes/users.js ---
    users_js = '''const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const result = await req.app.locals.pool.query('SELECT id, name, email FROM users LIMIT 50');
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch users' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const result = await req.app.locals.pool.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
        if (result.rows.length === 0) return res.status(404).json({ error: 'User not found' });
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch user' });
    }
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/users.js', 'w') as f:
        f.write(users_js)

    # --- src/routes/products.js ---
    products_js = '''const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const result = await req.app.locals.pool.query(
            'SELECT id, name, price, category FROM products ORDER BY name'
        );
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch products' });
    }
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/products.js', 'w') as f:
        f.write(products_js)

    # --- src/routes/orders.js ---
    orders_js = '''const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const result = await req.app.locals.pool.query(
            'SELECT o.id, o.total, o.status, u.name as customer FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.created_at DESC LIMIT 100'
        );
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch orders' });
    }
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/orders.js', 'w') as f:
        f.write(orders_js)

    # --- src/middleware/auth.js ---
    auth_js = '''function authenticate(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'Authentication required' });
    }
    try {
        const decoded = verifyToken(token);
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Invalid or expired token' });
    }
}

function verifyToken(token) {
    // Token verification logic
    const jwt = require('jsonwebtoken');
    return jwt.verify(token, process.env.API_KEY);
}

module.exports = { authenticate };
'''
    with open(f'{PROJECT_DIR}/src/middleware/auth.js', 'w') as f:
        f.write(auth_js)

    # --- .env.local ---
    env_local = '''# Local Development Environment
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/fullstack_dev
API_KEY=local-dev-api-key-2024-xk9m3
LOG_LEVEL=debug
CORS_ORIGIN=http://localhost:3000
REDIS_URL=redis://localhost:6379
SESSION_SECRET=local-session-secret-abc123
'''
    with open(f'{PROJECT_DIR}/.env.local', 'w') as f:
        f.write(env_local)

    # --- .env.staging ---
    env_staging = '''# Staging Environment
NODE_ENV=staging
PORT=8080
DATABASE_URL=postgresql://staging_user:stg_P@ss2024@staging-db.internal.example.com:5432/fullstack_staging
API_KEY=staging-api-key-2024-rw7p4
LOG_LEVEL=verbose
CORS_ORIGIN=https://staging.example.com
REDIS_URL=redis://staging-redis.internal.example.com:6379
SESSION_SECRET=staging-session-secret-def456
ENABLE_DEBUG_LOGGING=true
'''
    with open(f'{PROJECT_DIR}/.env.staging', 'w') as f:
        f.write(env_staging)

    # --- .env.production.readonly ---
    env_prod = '''# Production Read-Only Environment
NODE_ENV=production
PORT=8080
DATABASE_URL=postgresql://readonly_user:ro_P@ss2024@prod-replica.internal.example.com:5432/fullstack_prod
API_KEY=prod-api-key-2024-qz5n8
LOG_LEVEL=warn
CORS_ORIGIN=https://app.example.com
REDIS_URL=redis://prod-redis.internal.example.com:6379
SESSION_SECRET=prod-session-secret-ghi789
READ_ONLY=true
'''
    with open(f'{PROJECT_DIR}/.env.production.readonly', 'w') as f:
        f.write(env_prod)

    # --- validate-env.js (the validation script referenced by tasks.json) ---
    validate_env_js = '''#!/usr/bin/env node
/**
 * Environment Variable Validator
 * Checks that all required environment variables are set for the selected environment.
 * Used as a pre-launch task to prevent debug sessions from starting with missing config.
 */

const fs = require('fs');
const path = require('path');

// Required variables for all environments
const REQUIRED_VARS = [
    'NODE_ENV',
    'PORT',
    'DATABASE_URL',
    'API_KEY',
    'LOG_LEVEL',
    'CORS_ORIGIN'
];

function loadEnvFile(envPath) {
    if (!fs.existsSync(envPath)) {
        console.error(`ERROR: Environment file not found: ${envPath}`);
        process.exit(1);
    }

    const content = fs.readFileSync(envPath, 'utf-8');
    const vars = {};

    content.split('\\n').forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#')) {
            const [key, ...valueParts] = line.split('=');
            if (key) {
                vars[key.trim()] = valueParts.join('=').trim();
            }
        }
    });

    return vars;
}

function validate() {
    // Detect which .env file to validate based on NODE_ENV or command-line arg
    let envFile = process.argv[2];

    if (!envFile) {
        // Try to detect from current environment
        const nodeEnv = process.env.NODE_ENV || 'development';
        const envMap = {
            'development': '.env.local',
            'staging': '.env.staging',
            'production': '.env.production.readonly'
        };
        envFile = envMap[nodeEnv] || '.env.local';
    }

    const envPath = path.resolve(__dirname, envFile);
    console.log(`Validating environment: ${envFile}`);
    console.log(`File path: ${envPath}`);
    console.log('---');

    const vars = loadEnvFile(envPath);
    let hasErrors = false;

    REQUIRED_VARS.forEach(varName => {
        if (!vars[varName] || vars[varName].length === 0) {
            console.error(`MISSING: ${varName} is not set`);
            hasErrors = true;
        } else {
            console.log(`  OK: ${varName} = ${vars[varName].substring(0, 20)}...`);
        }
    });

    console.log('---');

    if (hasErrors) {
        console.error('VALIDATION FAILED: Missing required environment variables.');
        console.error('Please check your environment file and try again.');
        process.exit(1);
    }

    console.log(`All ${REQUIRED_VARS.length} required variables validated successfully.`);
    console.log(`Environment: ${vars.NODE_ENV || 'unknown'}`);
    process.exit(0);
}

validate();
'''
    with open(f'{PROJECT_DIR}/validate-env.js', 'w') as f:
        f.write(validate_env_js)

    # --- tests/server.test.js ---
    test_js = '''const request = require('supertest');
const app = require('../src/server');

describe('Health Check', () => {
    test('GET /health returns healthy status', async () => {
        const response = await request(app).get('/health');
        expect(response.statusCode).toBe(200);
        expect(response.body.status).toBe('healthy');
    });
});

describe('Users API', () => {
    test('GET /api/users returns user list', async () => {
        const response = await request(app).get('/api/users');
        expect(response.statusCode).toBe(200);
        expect(Array.isArray(response.body)).toBe(true);
    });
});
'''
    with open(f'{PROJECT_DIR}/tests/server.test.js', 'w') as f:
        f.write(test_js)

    # --- .gitignore ---
    gitignore = '''node_modules/
.env
.env.local
.env.staging
.env.production.readonly
coverage/
dist/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = '''# Fullstack Application

Multi-environment full-stack application with Express.js backend.

## Environments

- **Local**: Development with local PostgreSQL (`npm run dev`)
- **Staging**: Staging environment with verbose logging
- **Production (Read-Only)**: Safe debugging against production read-replica

## Setup

1. Copy the appropriate `.env.*` file
2. Install dependencies: `npm install`
3. Start the server: `npm start`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| API_KEY | API authentication key | Yes |
| NODE_ENV | Environment name | Yes |
| PORT | Server port | Yes |
| LOG_LEVEL | Logging verbosity | Yes |
| CORS_ORIGIN | Allowed CORS origin | Yes |
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Project structure created at: {PROJECT_DIR}')

    # DO NOT create .vscode/launch.json or .vscode/tasks.json
    # That is the agent's task

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
