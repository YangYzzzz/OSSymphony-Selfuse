"""
Initial Setup: Create a Node.js project structure for Dockerfile creation task
Task ID: vscode_gf3_002
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_002'
PROJECT_DIR = f'{WORKDIR}/projects/myapp'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "myapp",
        "version": "1.2.0",
        "description": "Express API for inventory management",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0",
            "pg": "^8.11.3",
            "joi": "^17.11.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0",
            "eslint": "^8.56.0"
        },
        "engines": {
            "node": ">=18.0.0"
        },
        "license": "MIT",
        "author": "Sarah Chen <sarah.chen@inventoryworks.io>"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- server.js ---
    server_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const inventoryRoutes = require('./src/routes/inventory');
const healthRoutes = require('./src/routes/health');
const errorHandler = require('./src/middleware/errorHandler');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/inventory', inventoryRoutes);
app.use('/api/health', healthRoutes);

// Error handling
app.use(errorHandler);

app.listen(PORT, () => {
    console.log(`Inventory API running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/server.js', 'w') as f:
        f.write(server_js)

    # --- src/routes/inventory.js ---
    inventory_routes = '''const express = require('express');
const router = express.Router();
const Joi = require('joi');

const itemSchema = Joi.object({
    name: Joi.string().min(1).max(200).required(),
    sku: Joi.string().pattern(/^[A-Z]{3}-\\d{4}$/).required(),
    quantity: Joi.number().integer().min(0).required(),
    price: Joi.number().precision(2).positive().required(),
    category: Joi.string().valid('electronics', 'clothing', 'food', 'tools').required()
});

let inventory = [
    { id: 1, name: 'Wireless Keyboard', sku: 'ELC-1042', quantity: 150, price: 49.99, category: 'electronics' },
    { id: 2, name: 'Cotton T-Shirt', sku: 'CLT-2087', quantity: 340, price: 24.95, category: 'clothing' },
    { id: 3, name: 'Organic Granola', sku: 'FOD-3521', quantity: 85, price: 8.50, category: 'food' },
];

router.get('/', (req, res) => {
    const { category, minQuantity } = req.query;
    let results = [...inventory];
    if (category) results = results.filter(item => item.category === category);
    if (minQuantity) results = results.filter(item => item.quantity >= parseInt(minQuantity));
    res.json({ count: results.length, items: results });
});

router.get('/:id', (req, res) => {
    const item = inventory.find(i => i.id === parseInt(req.params.id));
    if (!item) return res.status(404).json({ error: 'Item not found' });
    res.json(item);
});

router.post('/', (req, res) => {
    const { error, value } = itemSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.details[0].message });
    const newItem = { id: inventory.length + 1, ...value };
    inventory.push(newItem);
    res.status(201).json(newItem);
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/inventory.js', 'w') as f:
        f.write(inventory_routes)

    # --- src/routes/health.js ---
    health_routes = '''const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({
        status: 'healthy',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        version: require('../../package.json').version
    });
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/health.js', 'w') as f:
        f.write(health_routes)

    # --- src/middleware/errorHandler.js ---
    error_handler = '''function errorHandler(err, req, res, next) {
    console.error(`[${new Date().toISOString()}] Error:`, err.message);
    console.error(err.stack);

    const statusCode = err.statusCode || 500;
    res.status(statusCode).json({
        error: {
            message: statusCode === 500 ? 'Internal server error' : err.message,
            code: err.code || 'UNKNOWN_ERROR'
        }
    });
}

module.exports = errorHandler;
'''
    with open(f'{PROJECT_DIR}/src/middleware/errorHandler.js', 'w') as f:
        f.write(error_handler)

    # --- .env ---
    env_content = '''PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://appuser:secret@localhost:5432/inventory_db
LOG_LEVEL=info
'''
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # --- .gitignore ---
    gitignore = '''node_modules/
.env
coverage/
dist/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- .vscode/settings.json ---
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "files.exclude": {
            "node_modules": True
        }
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # --- NO Dockerfile --- (task is to create it)

    print(f'Project structure created at: {PROJECT_DIR}')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
