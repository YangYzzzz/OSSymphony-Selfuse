"""
Initial Setup: Open ~/projects/cwd-debug in VSCode with a launch.json that has no 'cwd' property.
Task ID: vscode_dbg_040
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_040'
PROJECT_DIR = f'{WORKDIR}/projects/cwd-debug'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
BACKEND_DIR = f'{PROJECT_DIR}/backend'


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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(BACKEND_DIR, exist_ok=True)

    # Create .vscode/launch.json WITHOUT 'cwd' property
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Launch Backend Server",
                "program": "${workspaceFolder}/backend/server.js",
                "console": "integratedTerminal"
            }
        ]
    }
    launch_json_path = f'{VSCODE_DIR}/launch.json'
    with open(launch_json_path, 'w') as f:
        json.dump(launch_config, f, indent=4)
    print(f'Created: {launch_json_path}')

    # Create backend/server.js — realistic Node.js Express server
    server_js_content = '''\
'use strict';

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Load config relative to current working directory
const configPath = path.join(process.cwd(), 'config', 'app.json');
let appConfig = {};
if (fs.existsSync(configPath)) {
    appConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// Routes
app.get('/health', (req, res) => {
    res.json({ status: 'ok', version: appConfig.version || '1.0.0' });
});

app.get('/api/users', (req, res) => {
    res.json([
        { id: 1, name: 'Alice Nguyen', role: 'admin' },
        { id: 2, name: 'Bob Martinez', role: 'editor' },
        { id: 3, name: 'Carol Singh', role: 'viewer' }
    ]);
});

app.post('/api/data', (req, res) => {
    const { payload } = req.body;
    if (!payload) {
        return res.status(400).json({ error: 'Missing payload' });
    }
    res.json({ received: payload, timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
    console.log(`Working directory: ${process.cwd()}`);
});

module.exports = app;
'''
    server_js_path = f'{BACKEND_DIR}/server.js'
    with open(server_js_path, 'w') as f:
        f.write(server_js_content)
    print(f'Created: {server_js_path}')

    # Create backend/package.json
    package_config = {
        "name": "cwd-debug-backend",
        "version": "1.0.0",
        "description": "Backend server for cwd-debug project",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.5.0"
        },
        "author": "Dev Team",
        "license": "MIT"
    }
    package_json_path = f'{BACKEND_DIR}/package.json'
    with open(package_json_path, 'w') as f:
        json.dump(package_config, f, indent=4)
    print(f'Created: {package_json_path}')

    # Create a top-level README.md
    readme_content = '''\
# cwd-debug

A sample Node.js project demonstrating working directory configuration in VSCode.

## Structure

```
cwd-debug/
├── .vscode/
│   └── launch.json      # Debug configuration
└── backend/
    ├── server.js        # Main Express server
    └── package.json     # Package manifest
```

## Getting Started

1. Run `npm install` inside `backend/`
2. Use the VSCode debug panel to launch the server
'''
    readme_path = f'{PROJECT_DIR}/README.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f'Created: {readme_path}')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open the project folder in VSCode
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
