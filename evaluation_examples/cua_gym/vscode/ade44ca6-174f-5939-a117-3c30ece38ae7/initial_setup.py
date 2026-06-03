"""
Initial Setup: Create a Node.js API project with server.js that reads env vars.
Task ID: vscode_td_053
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_053'
PROJECT_DIR = f'{WORKDIR}/projects/node-api'
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

    # Create package.json
    package_json = {
        "name": "node-api",
        "version": "1.0.0",
        "description": "REST API service for inventory management",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest"
        },
        "keywords": ["api", "rest", "inventory"],
        "author": "Sarah Chen",
        "license": "MIT",
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

    # Create src/server.js - reads environment variables for configuration
    server_js = '''\
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const app = express();

// Configuration from environment variables
const NODE_ENV = process.env.NODE_ENV || 'production';
const DB_HOST = process.env.DB_HOST || '127.0.0.1';
const DB_PORT = process.env.DB_PORT || 3306;
const APP_PORT = process.env.APP_PORT || 3000;

// Middleware
app.use(cors());
app.use(helmet());
app.use(express.json());

// Database connection config
const dbConfig = {
  host: DB_HOST,
  port: parseInt(DB_PORT, 10),
  database: 'inventory_db',
  max: 20,
  idleTimeoutMillis: 30000,
};

console.log(`Starting server in ${NODE_ENV} mode`);
console.log(`Database: ${DB_HOST}:${DB_PORT}`);

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', environment: NODE_ENV });
});

app.get('/api/products', async (req, res) => {
  try {
    // TODO: Implement database query
    res.json({ products: [], message: 'Database connection pending' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/products/:id', async (req, res) => {
  try {
    const { id } = req.params;
    res.json({ id, message: 'Product lookup pending' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/products', async (req, res) => {
  try {
    const { name, sku, quantity, price } = req.body;
    if (!name || !sku) {
      return res.status(400).json({ error: 'Name and SKU are required' });
    }
    res.status(201).json({ message: 'Product creation pending', data: req.body });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(APP_PORT, () => {
  console.log(`Inventory API running on port ${APP_PORT}`);
  console.log(`Health check: http://localhost:${APP_PORT}/api/health`);
});
'''
    with open(f'{SRC_DIR}/server.js', 'w') as f:
        f.write(server_js)

    # Create a README.md for the project
    readme = '''\
# Node API - Inventory Management

A REST API service for managing product inventory, built with Express.js and PostgreSQL.

## Getting Started

1. Install dependencies: `npm install`
2. Configure environment variables
3. Start the server: `npm start`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product by ID
- `POST /api/products` - Create new product

## Configuration

The server reads the following environment variables:
- `NODE_ENV` - Environment mode (development/production)
- `DB_HOST` - Database host address
- `DB_PORT` - Database port number
- `APP_PORT` - Application listening port (default: 3000)
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Create .gitignore
    gitignore = '''\
node_modules/
.env
*.log
dist/
coverage/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # Ensure NO .vscode directory exists (task is to create launch.json)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - package.json')
    print(f'  - src/server.js')
    print(f'  - README.md')
    print(f'  - .gitignore')
    print(f'  - NO .vscode/ directory')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
