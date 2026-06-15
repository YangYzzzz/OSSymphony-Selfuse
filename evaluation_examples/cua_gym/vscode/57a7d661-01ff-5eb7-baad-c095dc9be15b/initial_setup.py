"""
Initial Setup: Create backend project structure for SQL migration task
Task ID: vscode_gf3_040
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_040'
PROJECT_ROOT = f'{WORKDIR}/projects/backend'
MIGRATIONS_DIR = f'{PROJECT_ROOT}/src/database/migrations'


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
    os.makedirs(MIGRATIONS_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_ROOT}/src/database', exist_ok=True)
    os.makedirs(f'{PROJECT_ROOT}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_ROOT}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_ROOT}/tests', exist_ok=True)

    # Create a realistic package.json
    package_json = {
        "name": "inventory-api",
        "version": "1.2.0",
        "description": "Backend API for inventory management system",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "migrate": "node src/database/migrate.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.2"
        }
    }
    with open(f'{PROJECT_ROOT}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src/index.js
    with open(f'{PROJECT_ROOT}/src/index.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(helmet());
app.use(express.json());

// Routes
app.use('/api/users', require('./routes/users'));
app.use('/api/posts', require('./routes/posts'));

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
""")

    # Create database connection config
    with open(f'{PROJECT_ROOT}/src/database/connection.js', 'w') as f:
        f.write("""const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 5432,
  database: process.env.DB_NAME || 'inventory_db',
  user: process.env.DB_USER || 'app_user',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

module.exports = { pool };
""")

    # Create migration runner
    with open(f'{PROJECT_ROOT}/src/database/migrate.js', 'w') as f:
        f.write("""const fs = require('fs');
const path = require('path');
const { pool } = require('./connection');

async function runMigrations() {
  const migrationsDir = path.join(__dirname, 'migrations');
  const files = fs.readdirSync(migrationsDir)
    .filter(f => f.endsWith('.sql'))
    .sort();

  for (const file of files) {
    const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf8');
    console.log(`Running migration: ${file}`);
    await pool.query(sql);
    console.log(`Completed: ${file}`);
  }

  await pool.end();
  console.log('All migrations completed successfully.');
}

runMigrations().catch(err => {
  console.error('Migration failed:', err);
  process.exit(1);
});
""")

    # Create a placeholder route file
    with open(f'{PROJECT_ROOT}/src/routes/users.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const { pool } = require('../database/connection');

router.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, username, email, created_at FROM users ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, username, email, created_at FROM users WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
""")

    # Create .env.example
    with open(f'{PROJECT_ROOT}/.env.example', 'w') as f:
        f.write("""DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_db
DB_USER=app_user
DB_PASSWORD=your_password_here
PORT=3000
NODE_ENV=development
""")

    # Create a README placeholder
    with open(f'{PROJECT_ROOT}/README.md', 'w') as f:
        f.write("""# Inventory API

Backend API service for the inventory management system.

## Setup

1. Copy `.env.example` to `.env` and fill in your database credentials
2. Run `npm install`
3. Run migrations: `npm run migrate`
4. Start server: `npm start`

## Database Migrations

SQL migration files are stored in `src/database/migrations/`.
Files are executed in alphabetical order (001_, 002_, etc.).
""")

    # NOTE: Do NOT create any .sql files in migrations/ - that's the task!
    # The migrations directory exists but is empty.

    print(f'Project structure created at: {PROJECT_ROOT}')
    print(f'Migrations directory (empty): {MIGRATIONS_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
