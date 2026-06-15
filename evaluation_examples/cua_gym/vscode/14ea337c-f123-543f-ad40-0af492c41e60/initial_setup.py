"""
Initial Setup: VSCode multi-cursor console.log cleanup
Task ID: vscode_prod_040
Domain: vscode

Creates ~/projects/debug-cleanup/app.js with ~200 lines of realistic
JavaScript code containing 12 console.log statements scattered throughout.
Opens VSCode with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_040'
PROJECT_DIR = f'{WORKDIR}/projects/debug-cleanup'
OUTPUT = f'{PROJECT_DIR}/app.js'


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


APP_JS_CONTENT = r'''const express = require('express');
const helmet = require('helmet');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(express.json());

// Database connection
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 5432,
  database: 'taskmanager',
  user: 'admin',
  password: process.env.DB_PASSWORD,
  max: 20,
});

console.log('Database pool initialized, max connections:', pool.options.max);

// Auth middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  console.log('Received auth token:', token.substring(0, 8) + '...');
  try {
    const jwt = require('jsonwebtoken');
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}

// Validate email format
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// GET /api/tasks
app.get('/api/tasks', authenticateToken, async (req, res) => {
  try {
    const { status, priority, page = 1, limit = 20 } = req.query;
    const offset = (page - 1) * limit;
    let query = 'SELECT * FROM tasks WHERE user_id = $1';
    const params = [req.user.id];
    let idx = 2;
    if (status) {
      query += ` AND status = $${idx++}`;
      params.push(status);
    }
    if (priority) {
      query += ` AND priority = $${idx++}`;
      params.push(priority);
    }
    query += ` ORDER BY created_at DESC LIMIT $${idx++} OFFSET $${idx}`;
    params.push(parseInt(limit), parseInt(offset));
    console.log('Task query:', query, params);
    const result = await pool.query(query, params);
    const countRes = await pool.query(
      'SELECT COUNT(*) FROM tasks WHERE user_id = $1',
      [req.user.id]
    );
    res.json({
      tasks: result.rows,
      total: parseInt(countRes.rows[0].count),
      page: parseInt(page),
    });
  } catch (err) {
    console.log('GET /api/tasks error:', err.message);
    res.status(500).json({ error: 'Failed to fetch tasks' });
  }
});

// POST /api/tasks
app.post('/api/tasks', authenticateToken, async (req, res) => {
  try {
    const { title, description, priority, due_date } = req.body;
    if (!title || title.trim().length === 0) {
      return res.status(400).json({ error: 'Title is required' });
    }
    const validPriorities = ['low', 'medium', 'high', 'critical'];
    const taskPriority = validPriorities.includes(priority) ? priority : 'medium';
    console.log('Creating task:', title, 'priority:', taskPriority);
    const result = await pool.query(
      `INSERT INTO tasks (user_id, title, description, priority, due_date, status, created_at)
       VALUES ($1, $2, $3, $4, $5, 'pending', NOW()) RETURNING *`,
      [req.user.id, title.trim(), description || '', taskPriority, due_date || null]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.log('POST /api/tasks error:', err.message);
    res.status(500).json({ error: 'Failed to create task' });
  }
});

// PUT /api/tasks/:id
app.put('/api/tasks/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, priority, status, due_date } = req.body;
    const existing = await pool.query(
      'SELECT * FROM tasks WHERE id = $1 AND user_id = $2',
      [id, req.user.id]
    );
    if (existing.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    const current = existing.rows[0];
    const updates = {
      title: title || current.title,
      description: description !== undefined ? description : current.description,
      priority: priority || current.priority,
      status: status || current.status,
      due_date: due_date !== undefined ? due_date : current.due_date,
    };
    console.log('Updating task', id, 'fields:', JSON.stringify(updates));
    const result = await pool.query(
      `UPDATE tasks SET title=$1, description=$2, priority=$3,
       status=$4, due_date=$5, updated_at=NOW()
       WHERE id=$6 AND user_id=$7 RETURNING *`,
      [updates.title, updates.description, updates.priority,
       updates.status, updates.due_date, id, req.user.id]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to update task' });
  }
});

// DELETE /api/tasks/:id
app.delete('/api/tasks/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    console.log('Deleting task:', id, 'user:', req.user.id);
    const result = await pool.query(
      'DELETE FROM tasks WHERE id = $1 AND user_id = $2 RETURNING id',
      [id, req.user.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.json({ message: 'Task deleted', id: result.rows[0].id });
  } catch (err) {
    res.status(500).json({ error: 'Failed to delete task' });
  }
});

// GET /api/tasks/stats
app.get('/api/tasks/stats', authenticateToken, async (req, res) => {
  try {
    console.log('Fetching stats for user:', req.user.id);
    const result = await pool.query(
      `SELECT
        COUNT(*) FILTER (WHERE status = 'pending') AS pending,
        COUNT(*) FILTER (WHERE status = 'in_progress') AS in_progress,
        COUNT(*) FILTER (WHERE status = 'completed') AS completed,
        COUNT(*) FILTER (WHERE due_date < NOW() AND status != 'completed') AS overdue
       FROM tasks WHERE user_id = $1`,
      [req.user.id]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

// POST /api/tasks/:id/complete
app.post('/api/tasks/:id/complete', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    console.log('Completing task:', id);
    const result = await pool.query(
      `UPDATE tasks SET status='completed', completed_at=NOW(), updated_at=NOW()
       WHERE id=$1 AND user_id=$2 RETURNING *`,
      [id, req.user.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to complete task' });
  }
});

// Error handler
app.use((err, req, res, _next) => {
  console.log('Unhandled error:', err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end();
  process.exit(0);
});

app.listen(PORT, () => {
  console.log(`Task Manager API running on port ${PORT}`);
});
'''


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Also create a minimal package.json to make the project look real
    pkg_json = '''{
  "name": "debug-cleanup",
  "version": "1.2.0",
  "description": "Task Manager REST API",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "helmet": "^7.1.0",
    "jsonwebtoken": "^9.0.2",
    "pg": "^8.12.0"
  }
}
'''
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(pkg_json)

    with open(OUTPUT, 'w') as f:
        f.write(APP_JS_CONTENT)

    # Verify counts
    lines = APP_JS_CONTENT.strip().split('\n')
    console_count = sum(1 for line in lines if 'console.log' in line)
    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}')
    print(f'console.log statements: {console_count}')

    # Open VSCode with the project folder, then open the file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code -r "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
