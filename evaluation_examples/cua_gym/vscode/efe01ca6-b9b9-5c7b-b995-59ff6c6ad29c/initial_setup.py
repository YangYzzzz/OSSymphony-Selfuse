"""
Initial Setup: Install REST Client extension and configure environment variables
Task ID: vscode_we_067
Domain: vscode

Creates an API project workspace with realistic files. VSCode is opened with the
project. The REST Client extension is NOT installed and settings.json is empty.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_067'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
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
    # --- Create API project structure ---
    os.makedirs(WORKSPACE, exist_ok=True)

    # Main server file
    with open(os.path.join(WORKSPACE, 'server.js'), 'w') as f:
        f.write("""\
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Health check endpoint
app.get('/api/v1/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get all users
app.get('/api/v1/users', (req, res) => {
    res.json({
        users: [
            { id: 1, name: 'Sarah Chen', email: 'sarah.chen@example.com', role: 'admin' },
            { id: 2, name: 'Marcus Johnson', email: 'marcus.j@example.com', role: 'editor' },
            { id: 3, name: 'Priya Patel', email: 'priya.p@example.com', role: 'viewer' },
        ]
    });
});

// Get user by ID
app.get('/api/v1/users/:id', (req, res) => {
    const userId = parseInt(req.params.id);
    // Simplified lookup
    res.json({ id: userId, name: 'Sarah Chen', email: 'sarah.chen@example.com' });
});

// Create a new user
app.post('/api/v1/users', (req, res) => {
    const { name, email, role } = req.body;
    res.status(201).json({ id: 4, name, email, role, createdAt: new Date().toISOString() });
});

// Update user
app.put('/api/v1/users/:id', (req, res) => {
    const userId = parseInt(req.params.id);
    res.json({ id: userId, ...req.body, updatedAt: new Date().toISOString() });
});

// Delete user
app.delete('/api/v1/users/:id', (req, res) => {
    res.status(204).send();
});

app.listen(port, () => {
    console.log(`API server running on port ${port}`);
});
""")

    # Package.json
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump({
            "name": "user-management-api",
            "version": "1.0.0",
            "description": "User Management REST API",
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
                "jest": "^29.7.0",
                "nodemon": "^3.0.2"
            }
        }, f, indent=2)

    # REST API test file (plain text, not using REST Client yet)
    with open(os.path.join(WORKSPACE, 'api-tests.http'), 'w') as f:
        f.write("""\
### Health Check
GET http://localhost:3000/api/v1/health

### Get All Users
GET http://localhost:3000/api/v1/users

### Get User by ID
GET http://localhost:3000/api/v1/users/1

### Create New User
POST http://localhost:3000/api/v1/users
Content-Type: application/json

{
    "name": "Alex Rivera",
    "email": "alex.r@example.com",
    "role": "editor"
}

### Update User
PUT http://localhost:3000/api/v1/users/1
Content-Type: application/json

{
    "name": "Sarah Chen",
    "email": "sarah.chen@example.com",
    "role": "superadmin"
}

### Delete User
DELETE http://localhost:3000/api/v1/users/3
""")

    # README
    with open(os.path.join(WORKSPACE, 'README.md'), 'w') as f:
        f.write("""\
# User Management API

A RESTful API for managing users built with Express.js.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |
| GET | /api/v1/users | List all users |
| GET | /api/v1/users/:id | Get user by ID |
| POST | /api/v1/users | Create user |
| PUT | /api/v1/users/:id | Update user |
| DELETE | /api/v1/users/:id | Delete user |

## Setup

```bash
npm install
npm start
```

## Testing

Use the `api-tests.http` file with the REST Client extension for VSCode.
""")

    # .env.example
    with open(os.path.join(WORKSPACE, '.env.example'), 'w') as f:
        f.write("""\
PORT=3000
DATABASE_URL=mongodb://localhost:27017/users
JWT_SECRET=your-secret-key
""")

    # --- Ensure VSCode settings.json is empty ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Settings written: {SETTINGS_PATH}')

    # --- Ensure REST Client extension is NOT installed ---
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'humao.rest-client' in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', 'humao.rest-client'],
                capture_output=True, text=True, timeout=60
            )
            print('Uninstalled humao.rest-client extension')
        else:
            print('REST Client extension not installed (as expected)')
    except Exception as e:
        print(f'Extension check note: {e}')

    print(f'API project created at: {WORKSPACE}')

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
