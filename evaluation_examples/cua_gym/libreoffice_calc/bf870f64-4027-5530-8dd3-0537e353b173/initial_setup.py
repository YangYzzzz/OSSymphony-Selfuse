"""
Initial Setup: Create VSCode workspace for Node.js env-app project
Task ID: vscode_td_068
Domain: libreoffice_calc (vscode)
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_068'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'env-app')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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

    # Create .env file with realistic environment variables
    env_content = """\
# Database Configuration
DATABASE_URL=postgresql://admin:s3cur3Pa$$@db.internal.acme.io:5432/envapp_prod

# API Keys
API_KEY=sk_live_7f3a9b2c4d5e6f1a8b0c3d4e5f6a7b8c9d0e1f2a
"""
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # Create src/app.js - a realistic Node.js entry point
    app_js_content = """\
require('dotenv').config();
const express = require('express');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

// Database connection using environment variable
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

app.get('/api/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ status: 'healthy', timestamp: result.rows[0].now });
  } catch (err) {
    res.status(500).json({ status: 'error', message: err.message });
  }
});

app.get('/api/data', async (req, res) => {
  // Verify API key from header
  const apiKey = req.headers['x-api-key'];
  if (apiKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  try {
    const result = await pool.query('SELECT * FROM records LIMIT 50');
    res.json({ data: result.rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Database: ${process.env.DATABASE_URL ? 'configured' : 'NOT configured'}`);
});
"""
    with open(os.path.join(SRC_DIR, 'app.js'), 'w') as f:
        f.write(app_js_content)

    # Create package.json
    package_json = {
        "name": "env-app",
        "version": "1.0.0",
        "description": "Environment variable demo application",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js"
        },
        "dependencies": {
            "dotenv": "^16.3.1",
            "express": "^4.18.2",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create a .gitignore
    gitignore_content = """\
node_modules/
.env
*.log
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # NO .vscode/launch.json - that's the task for the agent to create

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'  .env file: {os.path.join(PROJECT_DIR, ".env")}')
    print(f'  src/app.js: {os.path.join(SRC_DIR, "app.js")}')
    print(f'  package.json: {os.path.join(PROJECT_DIR, "package.json")}')
    print(f'  No .vscode/launch.json (task target)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
