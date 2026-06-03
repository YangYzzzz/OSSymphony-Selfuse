"""
Initial Setup: Set up a Node.js project with empty tests/ directory for testing pyramid workflow
Task ID: vscode_wf_089
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_089'
PROJECT = f'{WORKDIR}/project'


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
    os.makedirs(f'{PROJECT}/src', exist_ok=True)
    os.makedirs(f'{PROJECT}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT}/.vscode', exist_ok=True)

    # --- package.json with Jest and Playwright in devDependencies ---
    package_json = {
        "name": "taskflow-api",
        "version": "1.0.0",
        "description": "TaskFlow project management API",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js"
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
            "@playwright/test": "^1.42.0",
            "nodemon": "^3.0.2",
            "supertest": "^6.3.3"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/app.js ---
    with open(f'{PROJECT}/src/app.js', 'w') as f:
        f.write('''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const routes = require('./routes');

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

app.use('/api', routes);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`TaskFlow API running on port ${PORT}`);
  });
}

module.exports = app;
''')

    # --- src/db.js ---
    with open(f'{PROJECT}/src/db.js', 'w') as f:
        f.write('''const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost:5432/taskflow',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected database error:', err);
  process.exit(-1);
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  getClient: () => pool.connect(),
  pool,
};
''')

    # --- src/routes.js ---
    with open(f'{PROJECT}/src/routes.js', 'w') as f:
        f.write('''const express = require('express');
const router = express.Router();
const db = require('./db');

// Get all tasks
router.get('/tasks', async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT * FROM tasks ORDER BY created_at DESC'
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch tasks' });
  }
});

// Create a task
router.post('/tasks', async (req, res) => {
  const { title, description, assignee, priority } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  try {
    const { rows } = await db.query(
      'INSERT INTO tasks (title, description, assignee, priority) VALUES ($1, $2, $3, $4) RETURNING *',
      [title, description || null, assignee || null, priority || 'medium']
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to create task' });
  }
});

// Update a task
router.put('/tasks/:id', async (req, res) => {
  const { id } = req.params;
  const { title, description, assignee, priority, status } = req.body;
  try {
    const { rows } = await db.query(
      'UPDATE tasks SET title=$1, description=$2, assignee=$3, priority=$4, status=$5, updated_at=NOW() WHERE id=$6 RETURNING *',
      [title, description, assignee, priority, status, id]
    );
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to update task' });
  }
});

// Delete a task
router.delete('/tasks/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.query('DELETE FROM tasks WHERE id=$1', [id]);
    if (result.rowCount === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: 'Failed to delete task' });
  }
});

module.exports = router;
''')

    # --- src/utils.js ---
    with open(f'{PROJECT}/src/utils.js', 'w') as f:
        f.write('''/**
 * Utility functions for TaskFlow API
 */

function formatDate(date) {
  return new Date(date).toISOString().split('T')[0];
}

function validatePriority(priority) {
  const valid = ['low', 'medium', 'high', 'critical'];
  return valid.includes(priority);
}

function sanitizeInput(str) {
  if (typeof str !== 'string') return str;
  return str.replace(/[<>&"']/g, (c) => {
    const entities = { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' };
    return entities[c];
  });
}

function paginate(array, page = 1, limit = 20) {
  const offset = (page - 1) * limit;
  return {
    data: array.slice(offset, offset + limit),
    total: array.length,
    page,
    totalPages: Math.ceil(array.length / limit),
  };
}

module.exports = { formatDate, validatePriority, sanitizeInput, paginate };
''')

    # --- .env.example ---
    with open(f'{PROJECT}/.env.example', 'w') as f:
        f.write('''PORT=3000
DATABASE_URL=postgresql://localhost:5432/taskflow
NODE_ENV=development
''')

    # --- .gitignore ---
    with open(f'{PROJECT}/.gitignore', 'w') as f:
        f.write('''node_modules/
.env
coverage/
dist/
*.log
''')

    # --- Empty .vscode/settings.json ---
    with open(f'{PROJECT}/.vscode/settings.json', 'w') as f:
        json.dump({
            "editor.tabSize": 2,
            "editor.formatOnSave": True
        }, f, indent=4)

    print(f'Initial project created at: {PROJECT}')
    print(f'tests/ directory exists: {os.path.isdir(f"{PROJECT}/tests")}')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
