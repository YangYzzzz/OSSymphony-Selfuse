"""
Initial Setup: Configure a terminal send text keybinding
Task ID: vscode_rrt_078
Domain: vscode

Creates a Node.js project workspace and an empty keybindings.json.
Opens VSCode with the workspace.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_078'
WORKSPACE_DIR = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')


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
    # --- Create Node.js project workspace ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "dashboard-app",
        "version": "1.2.0",
        "description": "Internal analytics dashboard for the sales team",
        "main": "src/index.js",
        "scripts": {
            "dev": "node src/index.js --watch",
            "build": "node build.js",
            "test": "node tests/run.js",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "eslint": "^8.50.0",
            "nodemon": "^3.0.1"
        },
        "author": "Sarah Chen <sarah.chen@acmecorp.io>",
        "license": "MIT"
    }
    with open(os.path.join(WORKSPACE_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    src_dir = os.path.join(WORKSPACE_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""\
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Sales dashboard API routes
app.get('/api/metrics', (req, res) => {
    res.json({
        totalRevenue: 1245000,
        activeUsers: 847,
        conversionRate: 0.032,
        avgOrderValue: 128.50,
        updatedAt: new Date().toISOString()
    });
});

app.get('/api/team', (req, res) => {
    res.json([
        { name: 'Marcus Johnson', region: 'West', quota: 350000, achieved: 287000 },
        { name: 'Emily Park', region: 'East', quota: 420000, achieved: 395000 },
        { name: 'David Okafor', region: 'Central', quota: 280000, achieved: 301000 },
        { name: 'Priya Sharma', region: 'South', quota: 310000, achieved: 245000 }
    ]);
});

app.listen(PORT, () => {
    console.log(`Dashboard API running on port ${PORT}`);
});
""")

    # .env file
    with open(os.path.join(WORKSPACE_DIR, '.env'), 'w') as f:
        f.write("PORT=3000\nNODE_ENV=development\nDB_HOST=localhost\n")

    # README.md
    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write("""\
# Dashboard App

Internal analytics dashboard for the sales team at AcmeCorp.

## Quick Start

```bash
npm install
npm run dev
```

The server starts on port 3000 by default.
""")

    # --- Set up empty keybindings.json ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Keybindings file created (empty): {KEYBINDINGS_PATH}')

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
