"""
Initial Setup: Configure Docker extension for Node.js user-service
Task ID: vscode_gf5_015
Domain: vscode

Creates ~/projects/microservices/user-service/ with app.js and package.json.
Opens VSCode with the microservices folder. No Dockerfile exists yet.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_015'
PROJECT_DIR = f'{WORKDIR}/projects/microservices'
SERVICE_DIR = f'{PROJECT_DIR}/user-service'


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
    os.makedirs(SERVICE_DIR, exist_ok=True)

    # Create package.json - realistic Node.js microservice
    package_json = {
        "name": "user-service",
        "version": "1.0.0",
        "description": "User management microservice for the platform",
        "main": "app.js",
        "scripts": {
            "start": "node app.js",
            "dev": "nodemon app.js",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "bcryptjs": "^2.4.3",
            "jsonwebtoken": "^9.0.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "express-validator": "^7.0.1",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.7.0"
        },
        "author": "DevOps Team",
        "license": "MIT"
    }

    with open(f'{SERVICE_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {SERVICE_DIR}/package.json')

    # Create app.js - realistic Express microservice
    app_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// In-memory user store (replace with MongoDB in production)
let users = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@company.com', role: 'admin' },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@company.com', role: 'user' },
    { id: 3, name: 'Priya Patel', email: 'priya.p@company.com', role: 'user' },
    { id: 4, name: 'James Wilson', email: 'james.w@company.com', role: 'moderator' },
];
let nextId = 5;

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'user-service', timestamp: new Date().toISOString() });
});

// GET all users
app.get('/api/users', (req, res) => {
    const { role } = req.query;
    let result = users;
    if (role) {
        result = users.filter(u => u.role === role);
    }
    res.json({ count: result.length, users: result });
});

// GET user by ID
app.get('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

// POST create user
app.post('/api/users', (req, res) => {
    const { name, email, role } = req.body;
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' });
    }
    const newUser = { id: nextId++, name, email, role: role || 'user' };
    users.push(newUser);
    res.status(201).json(newUser);
});

// PUT update user
app.put('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    const { name, email, role } = req.body;
    if (name) user.name = name;
    if (email) user.email = email;
    if (role) user.role = role;
    res.json(user);
});

// DELETE user
app.delete('/api/users/:id', (req, res) => {
    const index = users.findIndex(u => u.id === parseInt(req.params.id));
    if (index === -1) {
        return res.status(404).json({ error: 'User not found' });
    }
    const deleted = users.splice(index, 1);
    res.json({ message: 'User deleted', user: deleted[0] });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
    console.log(`User Service running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
});
'''

    with open(f'{SERVICE_DIR}/app.js', 'w') as f:
        f.write(app_js)
    print(f'Created: {SERVICE_DIR}/app.js')

    # Also create a .env.example for realism
    env_example = '''# User Service Environment Variables
PORT=3000
MONGODB_URI=mongodb://localhost:27017/userservice
JWT_SECRET=your-secret-key-here
NODE_ENV=development
'''
    with open(f'{SERVICE_DIR}/.env.example', 'w') as f:
        f.write(env_example)
    print(f'Created: {SERVICE_DIR}/.env.example')

    # Verify no Dockerfile exists (negative constraint)
    dockerfile_path = f'{SERVICE_DIR}/Dockerfile'
    if os.path.exists(dockerfile_path):
        os.remove(dockerfile_path)
        print(f'Removed pre-existing Dockerfile')

    # Install Docker (task says "Docker Desktop is running")
    def sudo_run(cmd, timeout=180):
        """Run command with sudo using SUDO_ASKPASS."""
        # Create askpass helper
        with open('/tmp/askpass.sh', 'wb') as f:
            f.write(b'\x23\x21/bin/bash\necho password\n')
        os.chmod('/tmp/askpass.sh', 0o755)
        env = os.environ.copy()
        env['SUDO_ASKPASS'] = '/tmp/askpass.sh'
        return subprocess.run(
            ['sudo', '-A', 'bash', '-c', cmd],
            capture_output=True, text=True, timeout=timeout, env=env
        )

    docker_check = subprocess.run(['which', 'docker'], capture_output=True, text=True)
    if docker_check.returncode != 0:
        print('Installing Docker for initial environment...')
        install_cmds = [
            'apt-get update -qq',
            'DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ca-certificates curl gnupg lsb-release',
            'install -m 0755 -d /etc/apt/keyrings',
            'curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc',
            'chmod a+r /etc/apt/keyrings/docker.asc',
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list',
            'apt-get update -qq',
            'DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin',
        ]
        for cmd in install_cmds:
            r = sudo_run(cmd)
            if r.returncode != 0:
                print(f'  WARN: {r.stderr[-200:] if r.stderr else ""}')

        sudo_run('systemctl start docker', timeout=30)
        sudo_run('usermod -aG docker user')
        time.sleep(3)
        print('Docker installed and started.')
    else:
        print('Docker already available.')

    # GUI-ready: Open VSCode with the microservices project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
