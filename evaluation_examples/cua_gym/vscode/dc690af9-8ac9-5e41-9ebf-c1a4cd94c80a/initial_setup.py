"""
Initial Setup: Node.js project open in VSCode without .env files
Task ID: vscode_file_034
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_034'
PROJECT_DIR = f'{WORKDIR}/api-server'


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
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # Create src/index.js
    index_js = os.path.join(src_dir, 'index.js')
    with open(index_js, 'w') as f:
        f.write("""\
const express = require('express');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'API Server running', status: 'ok' });
});

app.get('/health', async (req, res) => {
    const isConnected = await db.ping();
    res.json({ status: isConnected ? 'healthy' : 'degraded' });
});

app.get('/users', async (req, res) => {
    try {
        const users = await db.query('SELECT id, name, email FROM users LIMIT 50');
        res.json(users.rows);
    } catch (err) {
        res.status(500).json({ error: 'Database error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});

module.exports = app;
""")

    # Create src/db.js
    db_js = os.path.join(src_dir, 'db.js')
    with open(db_js, 'w') as f:
        f.write("""\
const { Pool } = require('pg');

const pool = new Pool({
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT, 10) || 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
    console.error('Unexpected error on idle client', err);
});

async function ping() {
    try {
        const client = await pool.connect();
        client.release();
        return true;
    } catch (err) {
        return false;
    }
}

async function query(text, params) {
    const start = Date.now();
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
}

module.exports = { query, ping };
""")

    # Create package.json
    package_json = os.path.join(PROJECT_DIR, 'package.json')
    with open(package_json, 'w') as f:
        f.write("""\
{
  "name": "api-server",
  "version": "1.0.0",
  "description": "A RESTful API server for managing application data",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^3.0.1",
    "supertest": "^6.3.3"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "license": "MIT"
}
""")

    # Ensure .env and .env.example do NOT exist in project root
    for fname in ['.env', '.env.example']:
        fpath = os.path.join(PROJECT_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f'Removed pre-existing {fname}')

    print(f'Project structure created: {PROJECT_DIR}')
    print('  api-server/')
    print('    src/')
    print('      index.js')
    print('      db.js')
    print('    package.json')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder using DISPLAY=:0')


create_initial()
