"""
Initial Setup: Set up environment-specific configurations in ~/project
Task ID: vscode_wf_052
Domain: vscode

Creates a basic Node.js project with git initialized. No .env files,
no launch.json, no .env patterns in .gitignore. VSCode opens ~/project.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_052'
PROJECT_DIR = f'{WORKDIR}/project'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create package.json
    package_json = {
        "name": "inventory-api",
        "version": "1.0.0",
        "description": "Warehouse inventory management REST API",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "dotenv": "^16.3.1",
            "pg": "^8.11.3",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0"
        },
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src directory and main file
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    index_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(helmet());
app.use(express.json());

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', environment: process.env.NODE_ENV });
});

app.get('/api/inventory', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM inventory ORDER BY updated_at DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('Database query failed:', err.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/inventory', async (req, res) => {
  const { sku, name, quantity, warehouse_id } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO inventory (sku, name, quantity, warehouse_id) VALUES ($1, $2, $3, $4) RETURNING *',
      [sku, name, quantity, warehouse_id]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Insert failed:', err.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Inventory API running on port ${port}`);
});
'''
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # Create a basic .gitignore (without .env patterns)
    gitignore_content = '''node_modules/
dist/
coverage/
*.log
'''
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # Create a README
    readme = '''# Inventory API

Warehouse inventory management REST API built with Express and PostgreSQL.

## Setup

1. Install dependencies: `npm install`
2. Configure environment variables
3. Start the server: `npm start`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/inventory` - List all inventory items
- `POST /api/inventory` - Add new inventory item
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Initialize git repository
    subprocess.run(['git', 'init'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(
        ['git', 'commit', '-m', 'Initial commit: project scaffold'],
        cwd=PROJECT_DIR, capture_output=True,
        env={**os.environ, 'GIT_AUTHOR_NAME': 'Dev', 'GIT_AUTHOR_EMAIL': 'dev@example.com',
             'GIT_COMMITTER_NAME': 'Dev', 'GIT_COMMITTER_EMAIL': 'dev@example.com'}
    )

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
