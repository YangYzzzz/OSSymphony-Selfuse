"""
Initial Setup: Configure files.exclude in workspace settings (pre-task state)
Task ID: vscode_file_025
Domain: vs_code

Creates a Node.js webapp project with node_modules and .log files visible,
with .vscode/settings.json containing only {}.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_025'
PROJECT_DIR = f'{WORKDIR}/webapp'


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
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create node_modules with realistic packages
    packages = [
        'express',
        'lodash',
        'axios',
        'dotenv',
        'body-parser',
        'cors',
        'morgan',
        'helmet',
    ]
    for pkg in packages:
        pkg_dir = f'{PROJECT_DIR}/node_modules/{pkg}'
        os.makedirs(pkg_dir, exist_ok=True)
        # Create a minimal package.json for each package
        pkg_meta = {
            "name": pkg,
            "version": "1.0.0",
            "description": f"The {pkg} package",
            "main": "index.js",
            "license": "MIT"
        }
        with open(f'{pkg_dir}/package.json', 'w') as f:
            json.dump(pkg_meta, f, indent=2)
        # Create a minimal index.js
        with open(f'{pkg_dir}/index.js', 'w') as f:
            f.write(f"'use strict';\n// {pkg} module\nmodule.exports = {{}};\n")

    # Create src/app.js with realistic Node.js content
    app_js_content = """\
'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the WebApp API', version: '1.0.0' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'OK', uptime: process.uptime() });
});

app.get('/api/users', (req, res) => {
    const users = [
        { id: 1, name: 'Alice Thompson', email: 'alice@example.com', role: 'admin' },
        { id: 2, name: 'Bob Martinez', email: 'bob@example.com', role: 'editor' },
        { id: 3, name: 'Carol Zhang', email: 'carol@example.com', role: 'viewer' },
    ];
    res.json(users);
});

app.post('/api/users', (req, res) => {
    const { name, email, role } = req.body;
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' });
    }
    const newUser = { id: Date.now(), name, email, role: role || 'viewer' };
    res.status(201).json(newUser);
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
"""
    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write(app_js_content)

    # Create debug.log with realistic log content
    debug_log_content = """\
[2025-03-01 08:12:34] DEBUG  Server starting up on port 3000
[2025-03-01 08:12:34] DEBUG  Loading environment variables from .env
[2025-03-01 08:12:35] DEBUG  Database connection initialized
[2025-03-01 08:12:35] DEBUG  Middleware stack configured: helmet, cors, morgan, body-parser
[2025-03-01 08:12:35] DEBUG  Route handlers registered: /, /health, /api/users
[2025-03-01 08:12:36] DEBUG  GET / 200 12ms - 54 bytes
[2025-03-01 08:12:41] DEBUG  GET /api/users 200 8ms - 247 bytes
[2025-03-01 08:12:55] DEBUG  POST /api/users 201 15ms - 98 bytes
[2025-03-01 08:13:02] DEBUG  GET /health 200 3ms - 41 bytes
[2025-03-01 08:13:10] DEBUG  Session cache cleared for user id=42
[2025-03-01 08:13:22] DEBUG  Background job 'cleanup-expired-tokens' started
[2025-03-01 08:13:22] DEBUG  Background job found 17 expired tokens, removing...
[2025-03-01 08:13:23] DEBUG  Background job 'cleanup-expired-tokens' completed in 1.2s
[2025-03-01 08:14:05] DEBUG  GET /api/users/1 200 5ms - 89 bytes
[2025-03-01 08:14:30] DEBUG  Config reload triggered by SIGHUP
"""
    with open(f'{PROJECT_DIR}/debug.log', 'w') as f:
        f.write(debug_log_content)

    # Create error.log with realistic log content
    error_log_content = """\
[2025-03-01 08:15:12] ERROR  Unhandled promise rejection in route /api/orders: TypeError: Cannot read properties of undefined (reading 'id')
    at /home/user/webapp/src/routes/orders.js:45:18
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
[2025-03-01 08:22:47] ERROR  Database query timeout after 5000ms: SELECT * FROM sessions WHERE expires_at < NOW()
[2025-03-01 08:35:09] ERROR  Failed to send email notification: ECONNREFUSED 127.0.0.1:25
[2025-03-01 09:04:31] ERROR  Rate limit exceeded for IP 192.168.1.105 on endpoint /api/login
[2025-03-01 09:17:55] ERROR  Uncaught exception: RangeError: Maximum call stack size exceeded
    at flatten (/home/user/webapp/node_modules/lodash/lodash.js:2332:14)
    at flatten (/home/user/webapp/node_modules/lodash/lodash.js:2332:14)
[2025-03-01 10:02:18] ERROR  File upload failed: ENOSPC no space left on device /tmp
[2025-03-01 10:45:33] ERROR  JWT verification failed: invalid signature for token issued to user id=88
"""
    with open(f'{PROJECT_DIR}/error.log', 'w') as f:
        f.write(error_log_content)

    # Create package.json with realistic Node.js project config
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "A RESTful web application API built with Express.js",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js",
            "test": "jest --coverage",
            "lint": "eslint src/**/*.js"
        },
        "keywords": ["express", "api", "nodejs", "rest"],
        "author": "Dev Team <dev@example.com>",
        "license": "MIT",
        "dependencies": {
            "axios": "^1.6.0",
            "body-parser": "^1.20.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "express": "^4.18.2",
            "helmet": "^7.1.0",
            "lodash": "^4.17.21",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "jest": "^29.7.0",
            "nodemon": "^3.0.2",
            "supertest": "^6.3.3"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create .vscode/settings.json with empty object (pre-task state)
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Project created: {PROJECT_DIR}')
    print(f'  - node_modules/ with {len(packages)} packages')
    print(f'  - src/app.js')
    print(f'  - debug.log')
    print(f'  - error.log')
    print(f'  - package.json')
    print(f'  - .vscode/settings.json (contains: {{}})')

    # GUI-ready startup: open VSCode with the webapp folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with webapp folder (DISPLAY=:0)')


create_initial()
