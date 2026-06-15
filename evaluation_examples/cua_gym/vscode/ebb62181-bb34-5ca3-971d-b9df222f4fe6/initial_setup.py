"""
Initial Setup: VSCode workspace with project structure, .vscode/settings.json empty,
and build/dist/coverage directories present but not excluded from search.
Task ID: vscode_file_074
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_074'
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


def create_initial():
    # Create project directory structure
    dirs = [
        f'{PROJECT_DIR}/.vscode',
        f'{PROJECT_DIR}/src',
        f'{PROJECT_DIR}/build',
        f'{PROJECT_DIR}/dist',
        f'{PROJECT_DIR}/coverage',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # .vscode/settings.json — empty object (NO search.exclude)
    settings_path = f'{PROJECT_DIR}/.vscode/settings.json'
    with open(settings_path, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Created: {settings_path}')

    # src/app.js — realistic JavaScript source file
    app_js_content = """\
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// API routes
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/users', async (req, res) => {
    try {
        const users = await User.findAll({ where: { active: true } });
        res.json(users);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/users', async (req, res) => {
    const { name, email, role } = req.body;
    if (!name || !email) {
        return res.status(400).json({ error: 'name and email are required' });
    }
    try {
        const user = await User.create({ name, email, role: role || 'viewer' });
        res.status(201).json(user);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

module.exports = app;
"""
    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write(app_js_content)
    print(f'Created: {PROJECT_DIR}/src/app.js')

    # build/ — compiled output files
    with open(f'{PROJECT_DIR}/build/app.bundle.js', 'w') as f:
        f.write('// Compiled bundle — DO NOT EDIT\n(function(e){var t={};\n/* minified output */\n})(window);\n')
    with open(f'{PROJECT_DIR}/build/app.bundle.js.map', 'w') as f:
        f.write('{"version":3,"sources":["src/app.js"],"mappings":"AAAA"}\n')

    # dist/ — distribution files
    with open(f'{PROJECT_DIR}/dist/index.html', 'w') as f:
        f.write('<!DOCTYPE html>\n<html><head><title>App</title></head><body><div id="root"></div><script src="app.bundle.js"></script></body></html>\n')
    with open(f'{PROJECT_DIR}/dist/app.bundle.min.js', 'w') as f:
        f.write('// minified\n')

    # coverage/ — test coverage report files
    with open(f'{PROJECT_DIR}/coverage/lcov.info', 'w') as f:
        f.write('SF:src/app.js\nDA:1,1\nDA:5,1\nDA:8,1\nDA:12,1\nend_of_record\n')
    with open(f'{PROJECT_DIR}/coverage/index.html', 'w') as f:
        f.write('<!DOCTYPE html>\n<html><head><title>Coverage Report</title></head><body><h1>Coverage: 87.4%</h1></body></html>\n')

    # package.json — realistic Node.js project manifest
    package_json = {
        "name": "my-web-app",
        "version": "2.3.1",
        "description": "A RESTful web application built with Express",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js",
            "build": "webpack --config webpack.config.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "sequelize": "^6.32.1",
            "pg": "^8.11.0",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "jest": "^29.5.0",
            "nodemon": "^3.0.1",
            "webpack": "^5.88.1",
            "eslint": "^8.45.0"
        },
        "author": "Alex Rivera <alex.rivera@example.com>",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/package.json')

    print(f'Project structure created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open the settings.json file so it's visible
    time.sleep(1.0)
    launch_gui(f'code "{settings_path}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder and settings.json open')


create_initial()
