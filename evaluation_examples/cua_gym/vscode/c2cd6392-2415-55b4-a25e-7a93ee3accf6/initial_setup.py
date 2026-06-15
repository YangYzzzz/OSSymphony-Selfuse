"""
Initial Setup: Set up API testing workflow in ~/project
Task ID: vscode_wf_060
Domain: vs_code

Creates an Express.js API project structure in ~/project.
No REST Client extension, no api_tests/, no .vscode config.
Opens VSCode with the project folder.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_060'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'routes'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'models'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'middleware'), exist_ok=True)

    # package.json - Express.js project
    package_json = {
        "name": "user-management-api",
        "version": "1.0.0",
        "description": "REST API for user management",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "body-parser": "^1.20.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        },
        "author": "DevOps Team",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # server.js - Main Express server
    server_js = '''const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const userRoutes = require('./routes/users');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.use('/api/users', userRoutes);

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
'''
    with open(os.path.join(PROJECT_DIR, 'server.js'), 'w') as f:
        f.write(server_js)

    # routes/users.js - CRUD routes
    users_routes = '''const express = require('express');
const router = express.Router();

// In-memory store for demo
let users = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@techcorp.com', role: 'engineer' },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@techcorp.com', role: 'designer' },
    { id: 3, name: 'Priya Patel', email: 'priya.p@techcorp.com', role: 'manager' },
    { id: 4, name: 'James Wilson', email: 'james.w@techcorp.com', role: 'engineer' },
    { id: 5, name: 'Amelia Rodriguez', email: 'amelia.r@techcorp.com', role: 'analyst' },
];

let nextId = 6;

// GET all users
router.get('/', (req, res) => {
    res.json(users);
});

// GET single user
router.get('/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
});

// POST create user
router.post('/', (req, res) => {
    const { name, email, role } = req.body;
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' });
    }
    const newUser = { id: nextId++, name, email, role: role || 'user' };
    users.push(newUser);
    res.status(201).json(newUser);
});

// PUT update user
router.put('/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) return res.status(404).json({ error: 'User not found' });
    const { name, email, role } = req.body;
    if (name) user.name = name;
    if (email) user.email = email;
    if (role) user.role = role;
    res.json(user);
});

// DELETE user
router.delete('/:id', (req, res) => {
    const index = users.findIndex(u => u.id === parseInt(req.params.id));
    if (index === -1) return res.status(404).json({ error: 'User not found' });
    const deleted = users.splice(index, 1);
    res.json({ message: 'User deleted', user: deleted[0] });
});

module.exports = router;
'''
    with open(os.path.join(PROJECT_DIR, 'routes', 'users.js'), 'w') as f:
        f.write(users_routes)

    # models/user.js - User model placeholder
    user_model = '''/**
 * User model definition
 * Currently uses in-memory storage for development
 * Replace with database model (MongoDB/PostgreSQL) for production
 */

class User {
    constructor(id, name, email, role) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.role = role;
        this.createdAt = new Date().toISOString();
    }
}

module.exports = User;
'''
    with open(os.path.join(PROJECT_DIR, 'models', 'user.js'), 'w') as f:
        f.write(user_model)

    # middleware/auth.js - Auth middleware placeholder
    auth_middleware = '''/**
 * Authentication middleware
 * TODO: Implement JWT token verification
 */

function authenticate(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) {
        return res.status(401).json({ error: 'Authentication required' });
    }
    // Token verification logic goes here
    next();
}

module.exports = authenticate;
'''
    with open(os.path.join(PROJECT_DIR, 'middleware', 'auth.js'), 'w') as f:
        f.write(auth_middleware)

    # .env file
    env_content = '''PORT=3000
NODE_ENV=development
'''
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # .gitignore
    gitignore = '''node_modules/
.env
*.log
'''
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # README.md
    readme = '''# User Management API

A RESTful API for managing users, built with Express.js.

## Endpoints

- `GET /api/users` - List all users
- `GET /api/users/:id` - Get a single user
- `POST /api/users` - Create a new user
- `PUT /api/users/:id` - Update a user
- `DELETE /api/users/:id` - Delete a user
- `GET /api/health` - Health check

## Setup

```bash
npm install
npm start
```

Server runs on port 3000 by default.
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    print(f'Initial Express.js project created at: {PROJECT_DIR}')

    # Make sure REST Client extension is NOT installed (remove if present)
    subprocess.run(
        ['code', '--uninstall-extension', 'humao.rest-client'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project on DISPLAY=:0')


create_initial()
