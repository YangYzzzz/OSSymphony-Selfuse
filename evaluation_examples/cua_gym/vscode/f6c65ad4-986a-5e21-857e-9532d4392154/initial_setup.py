"""
Initial Setup: Set up language-specific settings for JavaScript files
Task ID: vscode_lp_031
Domain: vs_code

Creates a workspace with JS files and sets global tabSize to 4.
VSCode is opened with the workspace folder.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
WORKSPACE = os.path.join(HOME, 'workspace')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # 1. Create workspace directory with sample JS files
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a sample JavaScript project
    with open(os.path.join(WORKSPACE, 'app.js'), 'w') as f:
        f.write('''\
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    const greeting = 'Hello, World!';
    res.json({
        message: greeting,
        timestamp: new Date().toISOString()
    });
});

app.get('/users', (req, res) => {
    const users = [
        { id: 1, name: 'Sarah Chen', role: 'developer' },
        { id: 2, name: 'Marcus Johnson', role: 'designer' },
        { id: 3, name: 'Emily Rodriguez', role: 'product manager' }
    ];
    res.json(users);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
''')

    with open(os.path.join(WORKSPACE, 'utils.js'), 'w') as f:
        f.write('''\
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function calculateDiscount(price, percentage) {
    if (percentage < 0 || percentage > 100) {
        throw new Error('Invalid discount percentage');
    }
    return price * (1 - percentage / 100);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

module.exports = { formatCurrency, calculateDiscount, debounce };
''')

    with open(os.path.join(WORKSPACE, 'config.py'), 'w') as f:
        f.write('''\
"""Application configuration module."""

DATABASE_URL = "postgresql://localhost:5432/myapp"
SECRET_KEY = "dev-secret-key-change-in-production"
DEBUG = True
LOG_LEVEL = "INFO"

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]
''')

    # 2. Set VSCode global settings — tabSize 4 only, NO language-specific overrides
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    settings["editor.tabSize"] = 4
    # Ensure NO javascript-specific settings exist
    if "[javascript]" in settings:
        del settings["[javascript]"]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Settings written to: {SETTINGS_PATH}')
    print(f'Workspace created at: {WORKSPACE}')

    # 3. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
