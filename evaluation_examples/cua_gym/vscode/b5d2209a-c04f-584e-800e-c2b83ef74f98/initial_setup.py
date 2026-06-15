"""
Initial Setup: Create REST Client HTTP test file for user management API
Task ID: vscode_gf3_008
Domain: vscode

Initial state: The project directory exists with some supporting files,
but the users.http file does NOT exist yet. VSCode is opened to the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_008'
PROJECT_DIR = f'{WORKDIR}/projects/api-tests'

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
    # 1. Create the project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create some supporting project files to make it realistic
    # A simple package.json for the API project
    package_json = """{
  "name": "user-management-api",
  "version": "1.0.0",
  "description": "REST API for user management",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.6.3",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}
"""
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write(package_json)

    # A basic server.js stub
    server_js = """const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// In-memory user store
let users = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@company.com', role: 'admin' },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@company.com', role: 'editor' },
    { id: 3, name: 'Priya Patel', email: 'priya.p@company.com', role: 'viewer' },
];

app.get('/api/users', (req, res) => {
    res.json(users);
});

app.post('/api/users', (req, res) => {
    const newUser = { id: users.length + 1, ...req.body };
    users.push(newUser);
    res.status(201).json(newUser);
});

app.delete('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    users = users.filter(u => u.id !== id);
    res.status(204).send();
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
"""
    with open(os.path.join(PROJECT_DIR, 'server.js'), 'w') as f:
        f.write(server_js)

    # A .env file
    env_content = """PORT=3000
DB_URI=mongodb://localhost:27017/user-management
JWT_SECRET=dev-secret-key-change-in-production
"""
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # NOTE: users.http does NOT exist in initial state - the agent must create it
    print(f'Initial project structure created at: {PROJECT_DIR}')
    print(f'Files: package.json, server.js, .env')
    print(f'users.http does NOT exist (agent must create it)')

    # 3. Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
