"""
Initial Setup: Create fullstack project workspace for VSCode debug config task
Task ID: vscode_td_055
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_055'
PROJECT_DIR = f'{WORKDIR}/projects/fullstack'


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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # Ensure NO .vscode/launch.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(f'{vscode_dir}/launch.json'):
        os.remove(f'{vscode_dir}/launch.json')

    # Create src/server.js - a realistic Express backend
    with open(f'{PROJECT_DIR}/src/server.js', 'w') as f:
        f.write('''const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, '..', 'public')));
app.use(express.json());

// API routes
const tasks = [
    { id: 1, title: 'Set up CI/CD pipeline', status: 'in-progress', assignee: 'Sarah Chen' },
    { id: 2, title: 'Design landing page mockups', status: 'completed', assignee: 'Marcus Rivera' },
    { id: 3, title: 'Write integration tests', status: 'pending', assignee: 'Aisha Patel' },
    { id: 4, title: 'Optimize database queries', status: 'in-progress', assignee: 'David Kim' },
    { id: 5, title: 'Update API documentation', status: 'pending', assignee: 'Elena Volkov' },
];

app.get('/api/tasks', (req, res) => {
    res.json({ tasks, total: tasks.length });
});

app.get('/api/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    res.json(task);
});

app.post('/api/tasks', (req, res) => {
    const newTask = {
        id: tasks.length + 1,
        title: req.body.title,
        status: 'pending',
        assignee: req.body.assignee || 'Unassigned',
    };
    tasks.push(newTask);
    res.status(201).json(newTask);
});

app.listen(PORT, () => {
    console.log(`Task Manager API running on http://localhost:${PORT}`);
});
''')

    # Create public/index.html - a realistic frontend
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #2c3e50; margin-bottom: 24px; }
        .task-list { list-style: none; }
        .task-item {
            background: white;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-title { font-weight: 600; color: #333; }
        .task-assignee { color: #666; font-size: 0.9em; }
        .status { padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 500; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-in-progress { background: #cce5ff; color: #004085; }
        .status-completed { background: #d4edda; color: #155724; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Manager</h1>
        <ul id="task-list" class="task-list"></ul>
    </div>
    <script src="app.js"></script>
</body>
</html>
''')

    # Create public/app.js - frontend JavaScript
    with open(f'{PROJECT_DIR}/public/app.js', 'w') as f:
        f.write('''document.addEventListener('DOMContentLoaded', async () => {
    const taskList = document.getElementById('task-list');

    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();

        data.tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';

            const statusClass = `status-${task.status}`;
            const statusLabel = task.status.replace('-', ' ');

            li.innerHTML = `
                <div>
                    <div class="task-title">${task.title}</div>
                    <div class="task-assignee">Assigned to: ${task.assignee}</div>
                </div>
                <span class="status ${statusClass}">${statusLabel}</span>
            `;
            taskList.appendChild(li);
        });
    } catch (error) {
        taskList.innerHTML = '<li class="task-item">Failed to load tasks. Is the server running?</li>';
        console.error('Error fetching tasks:', error);
    }
});
''')

    # Create package.json for the project
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
    "name": "fullstack-task-manager",
    "version": "1.0.0",
    "description": "A simple fullstack task manager application",
    "main": "src/server.js",
    "scripts": {
        "start": "node src/server.js",
        "dev": "nodemon src/server.js"
    },
    "dependencies": {
        "express": "^4.18.2"
    },
    "devDependencies": {
        "nodemon": "^3.0.1"
    }
}
''')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Files: src/server.js, public/index.html, public/app.js, package.json')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
