"""
Initial Setup: Create backend project structure for database seed workflow task
Task ID: vscode_gf3_073
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_073'
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
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)

    # package.json - realistic Node.js backend project
    package_json = {
        "name": "acme-backend",
        "version": "2.1.0",
        "description": "ACME Corp backend API service",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0",
            "joi": "^17.11.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0",
            "eslint": "^8.55.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js - main entry point
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(helmet());
app.use(morgan('combined'));
app.use(express.json());

// Database connection pool
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'acme_dev',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
});

// Routes
const userRoutes = require('./routes/users');
const postRoutes = require('./routes/posts');

app.use('/api/users', userRoutes(pool));
app.use('/api/posts', postRoutes(pool));

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(port, () => {
  console.log(`ACME Backend API running on port ${port}`);
});
""")

    # src/routes/users.js
    with open(f'{PROJECT_DIR}/src/routes/users.js', 'w') as f:
        f.write("""const { Router } = require('express');

module.exports = (pool) => {
  const router = Router();

  router.get('/', async (req, res) => {
    try {
      const { rows } = await pool.query(
        'SELECT id, name, email, created_at FROM users ORDER BY created_at DESC'
      );
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: 'Failed to fetch users' });
    }
  });

  router.get('/:id', async (req, res) => {
    try {
      const { rows } = await pool.query(
        'SELECT id, name, email, created_at FROM users WHERE id = $1',
        [req.params.id]
      );
      if (rows.length === 0) return res.status(404).json({ error: 'User not found' });
      res.json(rows[0]);
    } catch (err) {
      res.status(500).json({ error: 'Failed to fetch user' });
    }
  });

  return router;
};
""")

    # src/routes/posts.js
    with open(f'{PROJECT_DIR}/src/routes/posts.js', 'w') as f:
        f.write("""const { Router } = require('express');

module.exports = (pool) => {
  const router = Router();

  router.get('/', async (req, res) => {
    try {
      const { rows } = await pool.query(`
        SELECT p.id, p.title, p.content, p.created_at, u.name as author
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT 20
      `);
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: 'Failed to fetch posts' });
    }
  });

  return router;
};
""")

    # src/models/schema.sql - existing schema reference
    with open(f'{PROJECT_DIR}/src/models/schema.sql', 'w') as f:
        f.write("""-- ACME Backend Database Schema
-- PostgreSQL 15+

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
""")

    # config/database.js
    with open(f'{PROJECT_DIR}/config/database.js', 'w') as f:
        f.write("""require('dotenv').config();

module.exports = {
  development: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME || 'acme_dev',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    pool: { min: 2, max: 10 },
  },
  test: {
    host: 'localhost',
    port: 5432,
    database: 'acme_test',
    user: 'postgres',
    password: 'postgres',
    pool: { min: 1, max: 5 },
  },
  production: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    ssl: { rejectUnauthorized: false },
    pool: { min: 5, max: 20 },
  },
};
""")

    # .env file
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write("""DB_HOST=localhost
DB_PORT=5432
DB_NAME=acme_dev
DB_USER=postgres
DB_PASSWORD=postgres
PORT=3000
NODE_ENV=development
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
.env
*.log
coverage/
dist/
.DS_Store
""")

    # src/middleware/auth.js
    with open(f'{PROJECT_DIR}/src/middleware/auth.js', 'w') as f:
        f.write("""/**
 * Simple token-based authentication middleware.
 * In production, replace with JWT verification.
 */
module.exports = (req, res, next) => {
  const token = req.headers['authorization'];
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  // TODO: Implement proper JWT verification
  req.userId = 1; // Placeholder
  next();
};
""")

    # NOTE: No .vscode/ directory, no scripts/ directory
    # The task requires the agent to CREATE these

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
