"""
Initial Setup: Configure VSCode integrated terminal settings
Task ID: vscode_web_028
Domain: vscode

Creates a realistic web project directory and opens VSCode.
VSCode settings are left at defaults (no terminal configuration).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_028'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project_files():
    """Create a realistic web application project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "Customer portal web application",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest",
            "build": "webpack --mode production",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "eslint": "^8.56.0",
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # src/index.js
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/customers', async (req, res) => {
    try {
        const customers = await getCustomers();
        res.json(customers);
    } catch (error) {
        console.error('Failed to fetch customers:', error.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
""")

    # src/database.js
    with open(os.path.join(src_dir, 'database.js'), 'w') as f:
        f.write("""const { Pool } = require('pg');

const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'webapp_db',
    user: process.env.DB_USER || 'admin',
    password: process.env.DB_PASSWORD,
});

async function getCustomers() {
    const result = await pool.query(
        'SELECT id, name, email, created_at FROM customers ORDER BY created_at DESC'
    );
    return result.rows;
}

module.exports = { pool, getCustomers };
""")

    # .env.example
    with open(os.path.join(PROJECT_DIR, '.env.example'), 'w') as f:
        f.write("""PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=webapp_db
DB_USER=admin
DB_PASSWORD=changeme
""")

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Customer Portal Web Application

A Node.js/Express web application for managing customer data.

## Setup

1. Install dependencies: `npm install`
2. Copy `.env.example` to `.env` and configure database credentials
3. Start the server: `npm start`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/customers` - List all customers
""")

    # tests directory
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, 'health.test.js'), 'w') as f:
        f.write("""const request = require('supertest');
const app = require('../src/index');

describe('Health Check', () => {
    test('GET /api/health returns 200', async () => {
        const response = await request(app).get('/api/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('ok');
    });
});
""")

    print(f'Project files created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Ensure VSCode settings exist but without any terminal configuration."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any terminal-related settings if they exist
    keys_to_remove = [
        'terminal.integrated.defaultProfile.linux',
        'terminal.integrated.fontSize',
        'terminal.integrated.env.linux',
    ]
    for key in keys_to_remove:
        settings.pop(key, None)

    # Keep some basic non-terminal settings for realism
    settings.setdefault('editor.fontSize', 12)
    settings.setdefault('workbench.colorTheme', 'Default Dark Modern')

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written: {SETTINGS_PATH}')


def main():
    create_project_files()
    setup_vscode_settings()

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
