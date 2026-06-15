"""
Initial Setup: Configure Git hooks workflow with Husky for team-project
Task ID: vscode_gf5_032
Domain: vscode

Creates a Node.js project with ESLint configured but NO Husky, NO git hooks.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_032'
PROJECT_DIR = f'{WORKDIR}/projects/team-project'
SRC_DIR = f'{PROJECT_DIR}/src'

# NVM setup: source nvm so node/npm are available
NVM_DIR = os.path.expanduser('~/.nvm')
NVM_NODE_BIN = None
for d in sorted(os.listdir(os.path.join(NVM_DIR, 'versions', 'node')), reverse=True):
    candidate = os.path.join(NVM_DIR, 'versions', 'node', d, 'bin')
    if os.path.isdir(candidate):
        NVM_NODE_BIN = candidate
        break
if NVM_NODE_BIN:
    os.environ['PATH'] = NVM_NODE_BIN + ':' + os.environ.get('PATH', '')


def run_shell(cmd, cwd=None, timeout=120):
    """Run a shell command with nvm-aware PATH."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- package.json (NO husky) ---
    package_json = {
        "name": "team-project",
        "version": "1.0.0",
        "description": "Internal team collaboration platform backend",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "jsonwebtoken": "^9.0.2",
            "mongoose": "^7.6.3"
        },
        "devDependencies": {
            "eslint": "^8.52.0",
            "jest": "^29.7.0"
        },
        "author": "DevOps Team",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- .eslintrc.json ---
    eslintrc = {
        "env": {
            "node": True,
            "es2021": True,
            "jest": True
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "no-unused-vars": "error",
            "no-console": "warn",
            "semi": ["error", "always"],
            "quotes": ["error", "single"],
            "indent": ["error", 2],
            "no-undef": "error"
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # --- src/index.js ---
    with open(f'{SRC_DIR}/index.js', 'w') as f:
        f.write("""\
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// User routes
app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});

app.post('/api/users', (req, res) => {
  const { name, email, role } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  res.status(201).json({ id: Date.now(), name, email, role: role || 'member' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
""")

    # --- src/auth.js ---
    with open(f'{SRC_DIR}/auth.js', 'w') as f:
        f.write("""\
const jwt = require('jsonwebtoken');

const SECRET = process.env.JWT_SECRET || 'dev-secret-key';
const TOKEN_EXPIRY = '24h';

function generateToken(user) {
  return jwt.sign(
    { id: user.id, email: user.email, role: user.role },
    SECRET,
    { expiresIn: TOKEN_EXPIRY }
  );
}

function verifyToken(token) {
  try {
    return jwt.verify(token, SECRET);
  } catch (err) {
    return null;
  }
}

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  const token = authHeader.split(' ')[1];
  const decoded = verifyToken(token);
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
  req.user = decoded;
  next();
}

module.exports = { generateToken, verifyToken, authMiddleware };
""")

    # --- src/database.js ---
    with open(f'{SRC_DIR}/database.js', 'w') as f:
        f.write("""\
const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/team-project';

async function connectDB() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('MongoDB connection error:', error.message);
    process.exit(1);
  }
}

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  role: { type: String, enum: ['admin', 'member', 'viewer'], default: 'member' },
  department: { type: String },
  joinedAt: { type: Date, default: Date.now },
});

const User = mongoose.model('User', userSchema);

module.exports = { connectDB, User };
""")

    # --- src/utils.js ---
    with open(f'{SRC_DIR}/utils.js', 'w') as f:
        f.write("""\
function formatDate(date) {
  const d = new Date(date);
  return d.toISOString().split('T')[0];
}

function validateEmail(email) {
  const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  return re.test(email);
}

function paginate(items, page, pageSize) {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  return {
    data: items.slice(start, end),
    total: items.length,
    page: page,
    totalPages: Math.ceil(items.length / pageSize),
  };
}

module.exports = { formatDate, validateEmail, paginate };
""")

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""\
node_modules/
.env
coverage/
dist/
*.log
.DS_Store
""")

    # --- .env (template) ---
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write("""\
PORT=3000
JWT_SECRET=dev-secret-key-change-in-production
MONGO_URI=mongodb://localhost:27017/team-project
""")

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""\
# Team Project

Internal team collaboration platform backend.

## Setup

```bash
npm install
npm start
```

## Development

```bash
npm run lint    # Run ESLint
npm test        # Run tests
```
""")

    # --- Initialize git repo ---
    subprocess.run(['git', 'init'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'developer@company.com'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Developer'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'feat(init): initial project setup with Express and ESLint'], cwd=PROJECT_DIR, capture_output=True)

    # Install npm dependencies (eslint needed for the task)
    result = run_shell(['npm', 'install'], cwd=PROJECT_DIR, timeout=120)
    print(f'npm install: rc={result.returncode}')
    if result.stderr:
        print(f'  stderr: {result.stderr[:500]}')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Git repo initialized with initial commit')
    print(f'ESLint configured, Husky NOT installed')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
