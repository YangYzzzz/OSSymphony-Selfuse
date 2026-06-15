"""
Initial Setup: Database migration workflow project
Task ID: vscode_gf3_066
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_066'
PROJECT_DIR = f'{WORKDIR}/projects/backend'

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
    # Create project directory structure (no migrations yet)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a basic package.json for the backend project
    package_json = {
        "name": "backend-service",
        "version": "1.0.0",
        "description": "Backend API service with PostgreSQL",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create a basic server.js
    server_js = """const express = require('express');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost:5432/backend_db'
});

app.use(express.json());

app.get('/api/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ status: 'healthy', timestamp: result.rows[0].now });
  } catch (err) {
    res.status(500).json({ status: 'unhealthy', error: err.message });
  }
});

app.get('/api/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, username, email, created_at FROM users ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
"""
    with open(os.path.join(PROJECT_DIR, 'server.js'), 'w') as f:
        f.write(server_js)

    # Create a .env.example
    env_example = """DATABASE_URL=postgresql://user:password@localhost:5432/backend_db
PORT=3000
NODE_ENV=development
"""
    with open(os.path.join(PROJECT_DIR, '.env.example'), 'w') as f:
        f.write(env_example)

    # Create a basic README
    readme = """# Backend Service

A Node.js backend API service with PostgreSQL database.

## Setup

1. Copy `.env.example` to `.env` and configure your database connection
2. Run `npm install` to install dependencies
3. Run `npm start` to start the server

## Database

TODO: Set up database migrations for schema management.
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Do NOT create migrations/ directory, migrate.js, or .vscode/tasks.json
    # Those are what the agent needs to create

    print(f'Initial project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
