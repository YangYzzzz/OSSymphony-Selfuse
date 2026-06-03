"""
Initial Setup: Branch-based code review workflow in VSCode
Task ID: vscode_wf_045
Domain: vscode

Creates a Node.js Express project with git initialized on main branch.
src/middleware/ directory exists but no auth.js.
Opens VSCode with the project.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_045'
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


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd,
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    return result


def create_initial():
    # Clean up any existing project
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.package-lock', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "taskflow-api",
        "version": "1.2.0",
        "description": "TaskFlow project management API service",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "mongoose": "^7.6.3",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.7.0"
        },
        "author": "Elena Rodriguez",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- .gitignore ---
    gitignore_content = """node_modules/
.env
coverage/
*.log
.DS_Store
dist/
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    # --- .env.example ---
    env_example = """PORT=3000
MONGODB_URI=mongodb://localhost:27017/taskflow
JWT_SECRET=your_jwt_secret_here
NODE_ENV=development
"""
    with open(f'{PROJECT_DIR}/.env.example', 'w') as f:
        f.write(env_example)

    # --- src/app.js ---
    app_js = '''const express = require('express');
const cors = require('cors');
require('dotenv').config();

const indexRouter = require('./routes/index');
const taskRouter = require('./routes/tasks');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/', indexRouter);
app.use('/api/tasks', taskRouter);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(`[${new Date().toISOString()}] Error: ${err.message}`);
    res.status(err.status || 500).json({
        error: {
            message: err.message || 'Internal Server Error',
            status: err.status || 500
        }
    });
});

app.listen(PORT, () => {
    console.log(`TaskFlow API running on port ${PORT}`);
});

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write(app_js)

    # --- src/routes/index.js ---
    index_routes = '''const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({
        service: 'TaskFlow API',
        version: '1.2.0',
        status: 'running',
        timestamp: new Date().toISOString()
    });
});

router.get('/health', (req, res) => {
    res.json({ status: 'healthy', uptime: process.uptime() });
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/index.js', 'w') as f:
        f.write(index_routes)

    # --- src/routes/tasks.js ---
    tasks_routes = '''const express = require('express');
const router = express.Router();

// In-memory store for demo purposes
let tasks = [
    { id: 1, title: 'Design database schema', assignee: 'Elena Rodriguez', status: 'completed', priority: 'high', createdAt: '2025-09-01T10:00:00Z' },
    { id: 2, title: 'Implement user registration', assignee: 'Marcus Chen', status: 'in-progress', priority: 'high', createdAt: '2025-09-03T14:30:00Z' },
    { id: 3, title: 'Set up CI/CD pipeline', assignee: 'Priya Sharma', status: 'pending', priority: 'medium', createdAt: '2025-09-05T09:15:00Z' },
    { id: 4, title: 'Write API documentation', assignee: 'James Wilson', status: 'pending', priority: 'low', createdAt: '2025-09-06T11:00:00Z' },
];
let nextId = 5;

router.get('/', (req, res) => {
    const { status, priority } = req.query;
    let filtered = [...tasks];
    if (status) filtered = filtered.filter(t => t.status === status);
    if (priority) filtered = filtered.filter(t => t.priority === priority);
    res.json({ tasks: filtered, total: filtered.length });
});

router.get('/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    res.json(task);
});

router.post('/', (req, res) => {
    const { title, assignee, priority } = req.body;
    if (!title) return res.status(400).json({ error: 'Title is required' });
    const task = {
        id: nextId++,
        title,
        assignee: assignee || 'Unassigned',
        status: 'pending',
        priority: priority || 'medium',
        createdAt: new Date().toISOString()
    };
    tasks.push(task);
    res.status(201).json(task);
});

router.put('/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    Object.assign(task, req.body, { id: task.id });
    res.json(task);
});

router.delete('/:id', (req, res) => {
    const idx = tasks.findIndex(t => t.id === parseInt(req.params.id));
    if (idx === -1) return res.status(404).json({ error: 'Task not found' });
    tasks.splice(idx, 1);
    res.status(204).send();
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/tasks.js', 'w') as f:
        f.write(tasks_routes)

    # --- src/models/task.js ---
    task_model = '''const mongoose = require('mongoose');

const taskSchema = new mongoose.Schema({
    title: { type: String, required: true, trim: true },
    description: { type: String, default: '' },
    assignee: { type: String, default: 'Unassigned' },
    status: {
        type: String,
        enum: ['pending', 'in-progress', 'completed', 'archived'],
        default: 'pending'
    },
    priority: {
        type: String,
        enum: ['low', 'medium', 'high', 'critical'],
        default: 'medium'
    },
    dueDate: { type: Date },
    tags: [{ type: String }],
}, {
    timestamps: true
});

taskSchema.index({ status: 1, priority: 1 });
taskSchema.index({ assignee: 1 });

module.exports = mongoose.model('Task', taskSchema);
'''
    with open(f'{PROJECT_DIR}/src/models/task.js', 'w') as f:
        f.write(task_model)

    # --- src/middleware/.gitkeep ---
    # Keep the middleware directory in git but empty (no auth.js!)
    with open(f'{PROJECT_DIR}/src/middleware/.gitkeep', 'w') as f:
        f.write('')

    # --- README.md ---
    readme = '''# TaskFlow API

A project management API built with Express.js and MongoDB.

## Getting Started

```bash
npm install
cp .env.example .env
npm run dev
```

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `GET /api/tasks` - List tasks (supports ?status= and ?priority= filters)
- `GET /api/tasks/:id` - Get task by ID
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

## Project Structure

```
src/
  app.js          - Express app entry point
  routes/
    index.js      - Root and health routes
    tasks.js      - Task CRUD routes
  models/
    task.js       - Mongoose task schema
  middleware/     - Middleware modules (auth, logging, etc.)
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # --- Initialize git repo on main branch ---
    run_cmd('git init -b main', cwd=PROJECT_DIR)
    run_cmd('git config user.email "elena@taskflow.dev"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Elena Rodriguez"', cwd=PROJECT_DIR)
    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: TaskFlow API with Express routes and task model"', cwd=PROJECT_DIR)

    print(f'Project created at: {PROJECT_DIR}')
    print('Git initialized on main branch with all files committed.')

    # --- GUI-ready startup: Open VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
