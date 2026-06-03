"""
Initial Setup: Create project structure for multi-target Node.js debugging task
Task ID: vscode_dbg_042
Domain: vs_code

Creates ~/projects/multi-target/ with api/index.js and worker/index.js.
NO .vscode/ directory or launch.json — the agent must create that.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/projects/multi-target'

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
    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/worker', exist_ok=True)

    # Create api/index.js with realistic Express API content
    api_js = """\
'use strict';

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// In-memory data store
const tasks = [
    { id: 1, title: 'Review pull requests', status: 'pending', assignee: 'alice' },
    { id: 2, title: 'Deploy to staging', status: 'in-progress', assignee: 'bob' },
    { id: 3, title: 'Update documentation', status: 'completed', assignee: 'charlie' },
];

let nextId = tasks.length + 1;

app.get('/api/tasks', (req, res) => {
    const { status } = req.query;
    if (status) {
        return res.json(tasks.filter(t => t.status === status));
    }
    res.json(tasks);
});

app.get('/api/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    res.json(task);
});

app.post('/api/tasks', (req, res) => {
    const { title, assignee } = req.body;
    if (!title) return res.status(400).json({ error: 'Title is required' });
    const task = { id: nextId++, title, status: 'pending', assignee: assignee || 'unassigned' };
    tasks.push(task);
    res.status(201).json(task);
});

app.patch('/api/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    Object.assign(task, req.body);
    res.json(task);
});

app.listen(PORT, () => {
    console.log(`API server listening on port ${PORT}`);
});

module.exports = app;
"""

    # Create worker/index.js with realistic background worker content
    worker_js = """\
'use strict';

const EventEmitter = require('events');

const POLL_INTERVAL_MS = parseInt(process.env.POLL_INTERVAL_MS || '5000', 10);
const API_BASE = process.env.API_BASE || 'http://localhost:3000';

class TaskWorker extends EventEmitter {
    constructor() {
        super();
        this.running = false;
        this.processedCount = 0;
        this.errorCount = 0;
    }

    start() {
        if (this.running) {
            console.warn('[Worker] Already running');
            return;
        }
        this.running = true;
        console.log(`[Worker] Starting. Poll interval: ${POLL_INTERVAL_MS}ms`);
        this._scheduleNextPoll();
    }

    stop() {
        this.running = false;
        if (this._timer) clearTimeout(this._timer);
        console.log(`[Worker] Stopped. Processed: ${this.processedCount}, Errors: ${this.errorCount}`);
    }

    _scheduleNextPoll() {
        if (!this.running) return;
        this._timer = setTimeout(() => this._poll(), POLL_INTERVAL_MS);
    }

    async _poll() {
        try {
            const response = await fetch(`${API_BASE}/api/tasks?status=pending`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const pendingTasks = await response.json();

            for (const task of pendingTasks) {
                await this._processTask(task);
            }

            if (pendingTasks.length > 0) {
                console.log(`[Worker] Processed ${pendingTasks.length} pending task(s)`);
            }
        } catch (err) {
            this.errorCount++;
            console.error(`[Worker] Poll error: ${err.message}`);
        } finally {
            this._scheduleNextPoll();
        }
    }

    async _processTask(task) {
        try {
            // Simulate processing delay
            await new Promise(resolve => setTimeout(resolve, 100));

            await fetch(`${API_BASE}/api/tasks/${task.id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: 'completed' }),
            });

            this.processedCount++;
            this.emit('task:completed', task);
        } catch (err) {
            this.errorCount++;
            this.emit('task:error', { task, error: err });
        }
    }
}

const worker = new TaskWorker();

worker.on('task:completed', (task) => {
    console.log(`[Worker] Completed task #${task.id}: ${task.title}`);
});

worker.on('task:error', ({ task, error }) => {
    console.error(`[Worker] Failed task #${task.id}: ${error.message}`);
});

worker.start();

process.on('SIGINT', () => {
    worker.stop();
    process.exit(0);
});

process.on('SIGTERM', () => {
    worker.stop();
    process.exit(0);
});
"""

    # Create package.json at project root
    package_json = """\
{
  "name": "multi-target",
  "version": "1.0.0",
  "description": "Multi-target Node.js application with API server and background worker",
  "main": "api/index.js",
  "scripts": {
    "start:api": "node api/index.js",
    "start:worker": "node worker/index.js",
    "start": "node api/index.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
"""

    # Create README.md at project root
    readme = """\
# multi-target

A Node.js project with two runnable targets:

- **api**: HTTP REST API server (`api/index.js`)
- **worker**: Background task processor (`worker/index.js`)

## Running

```bash
# Start the API server
node api/index.js

# Start the background worker
node worker/index.js
```

## Debugging

To debug with VSCode, create a `.vscode/launch.json` with configurations
for each target.
"""

    with open(f'{PROJECT_DIR}/api/index.js', 'w') as f:
        f.write(api_js)
    with open(f'{PROJECT_DIR}/worker/index.js', 'w') as f:
        f.write(worker_js)
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(package_json)
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Verify .vscode does NOT exist (it must not be pre-created)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print(f'Removed pre-existing .vscode directory')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  api/index.js      : OK')
    print(f'  worker/index.js   : OK')
    print(f'  package.json      : OK')
    print(f'  .vscode/          : NOT present (agent must create)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')

create_initial()
