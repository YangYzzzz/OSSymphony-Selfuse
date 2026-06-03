"""
Initial Setup: Stage selected diff hunks in VSCode diff editor
Task ID: vscode_rf_033
Domain: vscode

Creates a Git repository at ~/projects/backend/ with api.js that has
3 unstaged hunks. VSCode is opened on the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_033'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'backend')
API_FILE = os.path.join(PROJECT_DIR, 'api.js')


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


def run_cmd(cmd, cwd=None):
    """Run a shell command, raise on failure."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout


# --- The committed (base) version of api.js ---
BASE_CONTENT = '''\
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Authentication middleware
function authenticateToken(req, res, next) {
  const token = req.headers['authorization'];
  if (!token) return res.sendStatus(401);
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// Database connection pool
const pool = require('./db').getPool();

// Rate limiter configuration
const rateLimit = require('express-rate-limit');
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

// User profile endpoint
router.get('/api/users/:id', authenticateToken, async (req, res) => {
  try {
    const userId = req.params.id;
    const result = await pool.query(
      'SELECT id, username, email, created_at FROM users WHERE id = $1',
      [userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Database query failed:', err.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Order processing endpoint
router.post('/api/orders', authenticateToken, async (req, res) => {
  const { items, shippingAddress } = req.body;
  if (!items || items.length === 0) {
    return res.status(400).json({ error: 'Order must contain at least one item' });
  }
  try {
    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const order = await pool.query(
      'INSERT INTO orders (user_id, items, total, shipping_address, status) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [req.user.id, JSON.stringify(items), total, shippingAddress, 'pending']
    );
    res.status(201).json(order.rows[0]);
  } catch (err) {
    console.error('Order creation failed:', err.message);
    res.status(500).json({ error: 'Failed to process order' });
  }
});

// Health check endpoint
router.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

module.exports = router;
'''

# --- The modified (working directory) version with 3 hunks ---
MODIFIED_CONTENT = '''\
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Authentication middleware - fixed token extraction
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// Database connection pool
const pool = require('./db').getPool();

// Rate limiter configuration
const rateLimit = require('express-rate-limit');
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

// User profile endpoint with caching support
router.get('/api/users/:id', authenticateToken, async (req, res) => {
  try {
    const userId = req.params.id;
    const cacheKey = `user_${userId}`;
    const cached = await redis.get(cacheKey);
    if (cached) {
      return res.json(JSON.parse(cached));
    }
    const result = await pool.query(
      'SELECT id, username, email, created_at, avatar_url, bio FROM users WHERE id = $1',
      [userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    await redis.setex(cacheKey, 300, JSON.stringify(result.rows[0]));
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Database query failed:', err.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Order processing endpoint
router.post('/api/orders', authenticateToken, async (req, res) => {
  const { items, shippingAddress } = req.body;
  if (!items || items.length === 0) {
    return res.status(400).json({ error: 'Order must contain at least one item' });
  }
  try {
    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const order = await pool.query(
      'INSERT INTO orders (user_id, items, total, shipping_address, status) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [req.user.id, JSON.stringify(items), total, shippingAddress, 'pending']
    );
    res.status(201).json(order.rows[0]);
  } catch (err) {
    console.error('Order creation failed:', err.message);
    res.status(500).json({ error: 'Unable to complete order processing. Please try again later.' });
  }
});

// Health check endpoint
router.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

module.exports = router;
'''


def create_initial():
    # 1. Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create a package.json for realism
    package_json = '''{
  "name": "backend-api",
  "version": "2.1.0",
  "description": "Backend API service for e-commerce platform",
  "main": "api.js",
  "scripts": {
    "start": "node api.js",
    "dev": "nodemon api.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.0",
    "bcrypt": "^5.1.0",
    "pg": "^8.11.0",
    "express-rate-limit": "^6.7.0"
  }
}
'''
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write(package_json)

    # 3. Create a db.js helper for realism
    db_content = '''\
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'ecommerce',
  user: process.env.DB_USER || 'admin',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
});

module.exports = { getPool: () => pool };
'''
    with open(os.path.join(PROJECT_DIR, 'db.js'), 'w') as f:
        f.write(db_content)

    # 4. Create a .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('node_modules/\n.env\n*.log\n')

    # 5. Write the BASE version of api.js and commit it
    with open(API_FILE, 'w') as f:
        f.write(BASE_CONTENT)

    # 6. Initialize Git repo and commit the base state
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "dev@company.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Backend Dev"', cwd=PROJECT_DIR)
    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: API endpoints with auth, users, orders"', cwd=PROJECT_DIR)

    # 7. Now overwrite api.js with the MODIFIED version (3 hunks of changes)
    with open(API_FILE, 'w') as f:
        f.write(MODIFIED_CONTENT)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'api.js has 3 unstaged hunks ready for partial staging')

    # 8. Verify the diff shows 3 hunks
    diff_output = run_cmd('git diff api.js', cwd=PROJECT_DIR)
    hunk_count = diff_output.count('@@')
    print(f'Number of diff hunks: {hunk_count}')

    # 9. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
