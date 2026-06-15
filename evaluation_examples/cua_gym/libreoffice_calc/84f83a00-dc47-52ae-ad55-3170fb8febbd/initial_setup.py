"""
Initial Setup: Create a mature project workspace with VSCode configs but no backup/sync workflow
Task ID: vscode_wf_095
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')


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
        os.path.join(PROJECT, 'src'),
        os.path.join(PROJECT, 'src', 'components'),
        os.path.join(PROJECT, 'src', 'utils'),
        os.path.join(PROJECT, 'tests'),
        os.path.join(PROJECT, 'docs'),
        os.path.join(PROJECT, 'config'),
        os.path.join(PROJECT, 'scripts'),
        VSCODE_DIR,
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- .vscode/settings.json (existing project settings, NO backup-related configs) ---
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.formatOnSave": True,
        "editor.minimap.enabled": False,
        "workbench.colorTheme": "Default Dark Modern",
        "python.analysis.typeCheckingMode": "basic",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "terminal.integrated.defaultProfile.linux": "bash",
        "git.autofetch": True,
        "git.confirmSync": False,
        "explorer.confirmDelete": False,
        "debug.console.fontSize": 13
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(settings, f, indent=4)

    # --- .vscode/launch.json (existing debug config) ---
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            },
            {
                "name": "Node: Debug",
                "type": "node",
                "request": "launch",
                "program": "${workspaceFolder}/src/index.js",
                "console": "integratedTerminal"
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'launch.json'), 'w') as f:
        json.dump(launch, f, indent=4)

    # --- Initialize git repo ---
    subprocess.run(['git', 'init'], cwd=PROJECT, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'dev@company.com'], cwd=PROJECT, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Developer'], cwd=PROJECT, capture_output=True)

    # --- Source files ---
    # src/index.js
    with open(os.path.join(PROJECT, 'src', 'index.js'), 'w') as f:
        f.write('''const express = require('express');
const { setupRoutes } = require('./components/routes');
const { connectDatabase } = require('./utils/database');
const config = require('../config/app.config');

const app = express();
const PORT = config.port || 3000;

async function startServer() {
    try {
        await connectDatabase();
        setupRoutes(app);
        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error.message);
        process.exit(1);
    }
}

startServer();
''')

    # src/components/routes.js
    with open(os.path.join(PROJECT, 'src', 'components', 'routes.js'), 'w') as f:
        f.write('''const { authenticateUser, authorizeRole } = require('../utils/auth');
const { validateRequest } = require('../utils/validation');

function setupRoutes(app) {
    app.get('/api/health', (req, res) => {
        res.json({ status: 'healthy', timestamp: new Date().toISOString() });
    });

    app.get('/api/users', authenticateUser, async (req, res) => {
        const users = await req.db.collection('users').find().toArray();
        res.json(users);
    });

    app.post('/api/users', authenticateUser, authorizeRole('admin'), validateRequest, async (req, res) => {
        const result = await req.db.collection('users').insertOne(req.body);
        res.status(201).json(result);
    });
}

module.exports = { setupRoutes };
''')

    # src/utils/database.js
    with open(os.path.join(PROJECT, 'src', 'utils', 'database.js'), 'w') as f:
        f.write('''const { MongoClient } = require('mongodb');

let dbConnection = null;

async function connectDatabase() {
    const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/appdb';
    const client = new MongoClient(uri);
    await client.connect();
    dbConnection = client.db();
    console.log('Database connected successfully');
    return dbConnection;
}

function getDb() {
    if (!dbConnection) {
        throw new Error('Database not initialized. Call connectDatabase first.');
    }
    return dbConnection;
}

module.exports = { connectDatabase, getDb };
''')

    # src/utils/auth.js
    with open(os.path.join(PROJECT, 'src', 'utils', 'auth.js'), 'w') as f:
        f.write('''const jwt = require('jsonwebtoken');
const SECRET = process.env.JWT_SECRET || 'development-secret-key';

function authenticateUser(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token provided' });
    try {
        const decoded = jwt.verify(token, SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(403).json({ error: 'Invalid token' });
    }
}

function authorizeRole(role) {
    return (req, res, next) => {
        if (req.user.role !== role) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }
        next();
    };
}

module.exports = { authenticateUser, authorizeRole };
''')

    # src/utils/validation.js
    with open(os.path.join(PROJECT, 'src', 'utils', 'validation.js'), 'w') as f:
        f.write('''function validateRequest(req, res, next) {
    const { name, email } = req.body;
    const errors = [];
    if (!name || name.trim().length === 0) errors.push('Name is required');
    if (!email || !email.includes('@')) errors.push('Valid email is required');
    if (errors.length > 0) return res.status(400).json({ errors });
    next();
}

module.exports = { validateRequest };
''')

    # config/app.config.js
    with open(os.path.join(PROJECT, 'config', 'app.config.js'), 'w') as f:
        f.write('''module.exports = {
    port: process.env.PORT || 3000,
    environment: process.env.NODE_ENV || 'development',
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        format: 'json'
    },
    cors: {
        origin: process.env.CORS_ORIGIN || '*',
        methods: ['GET', 'POST', 'PUT', 'DELETE']
    },
    rateLimit: {
        windowMs: 15 * 60 * 1000,
        max: 100
    }
};
''')

    # tests/test_routes.py
    with open(os.path.join(PROJECT, 'tests', 'test_routes.py'), 'w') as f:
        f.write('''import unittest
import requests

BASE_URL = 'http://localhost:3000/api'

class TestHealthEndpoint(unittest.TestCase):
    def test_health_returns_200(self):
        resp = requests.get(f'{BASE_URL}/health')
        self.assertEqual(resp.status_code, 200)

    def test_health_has_timestamp(self):
        resp = requests.get(f'{BASE_URL}/health')
        data = resp.json()
        self.assertIn('timestamp', data)

class TestUsersEndpoint(unittest.TestCase):
    def test_users_requires_auth(self):
        resp = requests.get(f'{BASE_URL}/users')
        self.assertEqual(resp.status_code, 401)

if __name__ == '__main__':
    unittest.main()
''')

    # package.json
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump({
            "name": "project-workspace",
            "version": "2.4.1",
            "description": "Enterprise API server with authentication and data management",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest --coverage",
                "lint": "eslint src/ --fix"
            },
            "dependencies": {
                "express": "^4.18.2",
                "mongodb": "^6.3.0",
                "jsonwebtoken": "^9.0.2"
            },
            "devDependencies": {
                "jest": "^29.7.0",
                "eslint": "^8.56.0",
                "nodemon": "^3.0.3"
            }
        }, f, indent=2)

    # .gitignore
    with open(os.path.join(PROJECT, '.gitignore'), 'w') as f:
        f.write('''node_modules/
.env
*.log
dist/
coverage/
.DS_Store
''')

    # README.md
    with open(os.path.join(PROJECT, 'README.md'), 'w') as f:
        f.write('''# Project Workspace

Enterprise API server built with Express.js and MongoDB.

## Features
- JWT-based authentication and role authorization
- RESTful API endpoints for user management
- Request validation middleware
- Configurable CORS and rate limiting

## Getting Started

```bash
npm install
npm run dev
```

## Testing

```bash
npm test
python -m pytest tests/
```

## Configuration

Environment variables:
- `PORT` - Server port (default: 3000)
- `MONGODB_URI` - Database connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `NODE_ENV` - Environment (development/production)
''')

    # docs/architecture.md
    with open(os.path.join(PROJECT, 'docs', 'architecture.md'), 'w') as f:
        f.write('''# Architecture Overview

## Components

### API Layer (src/components/routes.js)
Defines REST endpoints with middleware chain.

### Authentication (src/utils/auth.js)
JWT-based auth with role-based access control.

### Database (src/utils/database.js)
MongoDB driver with connection pooling.

### Configuration (config/app.config.js)
Centralized config with environment variable overrides.

## Data Flow
1. Request -> Rate Limiter -> CORS -> Router
2. Router -> Auth Middleware -> Validation -> Handler
3. Handler -> Database -> Response
''')

    # Git initial commit
    subprocess.run(['git', 'add', '-A'], cwd=PROJECT, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial project setup'], cwd=PROJECT, capture_output=True)

    print(f'Initial project created at: {PROJECT}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project')


create_initial()
