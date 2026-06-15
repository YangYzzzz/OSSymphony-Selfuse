"""
Initial Setup: Configure JSON schema mapping in VSCode settings
Task ID: vscode_lp_030
Domain: vscode

Creates a workspace with a sample package.json file and opens VSCode.
No json.schemas setting is configured -- that is the agent's task.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_030'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'my-node-project')
PACKAGE_JSON_PATH = os.path.join(PROJECT_DIR, 'package.json')


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
    # 1. Create project directory with a realistic package.json
    os.makedirs(PROJECT_DIR, exist_ok=True)

    package_json = {
        "name": "inventory-dashboard",
        "version": "2.4.1",
        "description": "Real-time inventory tracking dashboard for warehouse management",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "build": "webpack --mode production",
            "lint": "eslint src/"
        },
        "keywords": ["inventory", "dashboard", "warehouse", "tracking"],
        "author": "Sarah Chen <sarah.chen@techcorp.io>",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "socket.io": "^4.7.2"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.1",
            "eslint": "^8.52.0",
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4"
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/techcorp/inventory-dashboard.git"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }

    with open(PACKAGE_JSON_PATH, 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created package.json at {PACKAGE_JSON_PATH}')

    # 2. Create a simple index.js so the project looks real
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.get('/api/inventory', (req, res) => {
    res.json({ status: 'ok', items: [] });
});

app.listen(PORT, () => {
    console.log(`Inventory Dashboard running on port ${PORT}`);
});
""")

    # 3. Ensure VSCode settings directory exists with basic settings (NO json.schemas)
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove json.schemas if it somehow exists
    settings.pop('json.schemas', None)

    # Set some basic settings so it looks like a used editor
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay"
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured at {SETTINGS_PATH} (no json.schemas)')

    # 4. Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
