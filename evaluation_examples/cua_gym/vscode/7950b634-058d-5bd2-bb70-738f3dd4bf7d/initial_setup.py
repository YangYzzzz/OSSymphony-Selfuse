"""
Initial Setup: Node.js Express project with buggy email validator
Task ID: vscode_gf6_013
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_013'
PROJECT_DIR = f'{WORKDIR}/projects/node-debug'

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
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/test', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "node-debug",
        "version": "1.0.0",
        "description": "Express API for user management",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest --verbose"
        },
        "dependencies": {
            "express": "^4.18.2",
            "body-parser": "^1.20.2"
        },
        "devDependencies": {
            "jest": "^29.7.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/index.js (Express server on port 3000) ---
    index_js = '''\
const express = require('express');
const bodyParser = require('body-parser');
const { validateEmail, validateUsername } = require('./middleware/validator');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

// Routes
app.post('/api/users/register', (req, res) => {
  const { email, username, password } = req.body;

  if (!email || !username || !password) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  if (!validateEmail(email)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }

  if (!validateUsername(username)) {
    return res.status(400).json({ error: 'Invalid username format' });
  }

  // Simulate user creation
  res.status(201).json({
    message: 'User registered successfully',
    user: { email, username, createdAt: new Date().toISOString() }
  });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.get('/api/users/:id', (req, res) => {
  // Simulated user lookup
  const users = {
    '1': { id: '1', email: 'sarah.chen@techcorp.com', username: 'sarah_chen' },
    '2': { id: '2', email: 'marcus.johnson+work@gmail.com', username: 'mjohnson' },
    '3': { id: '3', email: 'dev+staging@company.io', username: 'devops_lead' }
  };
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'production'}`);
  });
}

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # --- src/middleware/validator.js (BUGGY email regex) ---
    # The bug: regex /^[a-zA-Z0-9._%+-]+/ is incomplete - missing @ and domain parts
    # This means it only validates the local part and accepts anything after
    # Actually, to make plus signs rejected specifically, the bug is that the regex
    # does NOT include + in the character class before @
    validator_js = '''\
/**
 * Validation middleware for user input
 * Provides email and username validation utilities
 */

/**
 * Validates an email address format.
 * Known issue: some valid email formats may be incorrectly rejected.
 */
function validateEmail(email) {
  if (!email || typeof email !== 'string') {
    return false;
  }

  // BUG: The regex character class before @ does not include the + character,
  // so emails like user+tag@example.com are incorrectly rejected
  const emailRegex = /^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email.trim());
}

/**
 * Validates a username format.
 * Must be 3-30 characters, alphanumeric with underscores and hyphens.
 */
function validateUsername(username) {
  if (!username || typeof username !== 'string') {
    return false;
  }
  const usernameRegex = /^[a-zA-Z0-9_-]{3,30}$/;
  return usernameRegex.test(username.trim());
}

/**
 * Validates a password meets minimum requirements.
 * At least 8 characters, one uppercase, one lowercase, one digit.
 */
function validatePassword(password) {
  if (!password || typeof password !== 'string') {
    return false;
  }
  if (password.length < 8) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/[0-9]/.test(password)) return false;
  return true;
}

module.exports = {
  validateEmail,
  validateUsername,
  validatePassword
};
'''
    with open(f'{PROJECT_DIR}/src/middleware/validator.js', 'w') as f:
        f.write(validator_js)

    # --- src/routes/users.js ---
    users_routes = '''\
const express = require('express');
const router = express.Router();
const { validateEmail, validateUsername, validatePassword } = require('../middleware/validator');

router.post('/register', (req, res) => {
  const { email, username, password } = req.body;

  const errors = [];
  if (!validateEmail(email)) errors.push('Invalid email');
  if (!validateUsername(username)) errors.push('Invalid username');
  if (!validatePassword(password)) errors.push('Password too weak');

  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }

  res.status(201).json({ message: 'User created', user: { email, username } });
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/users.js', 'w') as f:
        f.write(users_routes)

    # --- test/validator.test.js ---
    test_js = '''\
const { validateEmail, validateUsername, validatePassword } = require('../src/middleware/validator');

describe('Email Validation', () => {
  test('accepts standard email addresses', () => {
    expect(validateEmail('user@example.com')).toBe(true);
    expect(validateEmail('john.doe@company.org')).toBe(true);
    expect(validateEmail('admin@mail.co.uk')).toBe(true);
  });

  test('accepts emails with plus signs (tagged addressing)', () => {
    expect(validateEmail('user+tag@example.com')).toBe(true);
    expect(validateEmail('sarah+newsletter@gmail.com')).toBe(true);
    expect(validateEmail('dev+staging@company.io')).toBe(true);
  });

  test('accepts emails with dots and hyphens in local part', () => {
    expect(validateEmail('first.last@domain.com')).toBe(true);
    expect(validateEmail('user-name@example.org')).toBe(true);
  });

  test('rejects invalid email formats', () => {
    expect(validateEmail('')).toBe(false);
    expect(validateEmail('notanemail')).toBe(false);
    expect(validateEmail('@missing-local.com')).toBe(false);
    expect(validateEmail('missing-domain@')).toBe(false);
    expect(validateEmail(null)).toBe(false);
    expect(validateEmail(undefined)).toBe(false);
  });
});

describe('Username Validation', () => {
  test('accepts valid usernames', () => {
    expect(validateUsername('sarah_chen')).toBe(true);
    expect(validateUsername('mjohnson')).toBe(true);
    expect(validateUsername('dev-ops-lead')).toBe(true);
    expect(validateUsername('user123')).toBe(true);
  });

  test('rejects invalid usernames', () => {
    expect(validateUsername('ab')).toBe(false);  // too short
    expect(validateUsername('')).toBe(false);
    expect(validateUsername('user@name')).toBe(false);
    expect(validateUsername(null)).toBe(false);
  });
});

describe('Password Validation', () => {
  test('accepts strong passwords', () => {
    expect(validatePassword('MyPass123')).toBe(true);
    expect(validatePassword('Str0ngP@ss')).toBe(true);
  });

  test('rejects weak passwords', () => {
    expect(validatePassword('short')).toBe(false);
    expect(validatePassword('nouppercase1')).toBe(false);
    expect(validatePassword('NOLOWERCASE1')).toBe(false);
    expect(validatePassword('NoDigitsHere')).toBe(false);
    expect(validatePassword('')).toBe(false);
    expect(validatePassword(null)).toBe(false);
  });
});
'''
    with open(f'{PROJECT_DIR}/test/validator.test.js', 'w') as f:
        f.write(test_js)

    # --- .gitignore ---
    gitignore = '''\
node_modules/
.env
coverage/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- Install Node.js 18 if not present (user-local, no sudo) ---
    node_bin = f'{WORKDIR}/.local/node/bin/node'
    npm_bin = f'{WORKDIR}/.local/node/bin/npm'
    npx_bin = f'{WORKDIR}/.local/node/bin/npx'

    node_check = subprocess.run(['which', 'node'], capture_output=True, text=True)
    if node_check.returncode != 0 and not os.path.exists(node_bin):
        print('Node.js not found, installing Node.js 18 locally...')
        os.makedirs(f'{WORKDIR}/.local', exist_ok=True)
        # Download Node.js 18 binary
        subprocess.run(
            f'curl -fsSL https://nodejs.org/dist/v18.20.4/node-v18.20.4-linux-x64.tar.xz '
            f'-o {WORKDIR}/.local/node18.tar.xz',
            shell=True, capture_output=True, text=True, timeout=120
        )
        subprocess.run(
            f'tar -xf {WORKDIR}/.local/node18.tar.xz -C {WORKDIR}/.local/',
            shell=True, capture_output=True, text=True, timeout=60
        )
        subprocess.run(
            f'mv {WORKDIR}/.local/node-v18.20.4-linux-x64 {WORKDIR}/.local/node',
            shell=True, capture_output=True, text=True
        )
        os.remove(f'{WORKDIR}/.local/node18.tar.xz')
        # Add to PATH for this process and child processes
        os.environ['PATH'] = f'{WORKDIR}/.local/node/bin:' + os.environ.get('PATH', '')
        ver = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f'Node version: {ver.stdout.strip()}')
        ver2 = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f'npm version: {ver2.stdout.strip()}')
    elif os.path.exists(node_bin):
        os.environ['PATH'] = f'{WORKDIR}/.local/node/bin:' + os.environ.get('PATH', '')
        print(f'Node.js already installed locally')
    else:
        print(f'Node.js already installed: {node_check.stdout.strip()}')

    # --- Install npm dependencies ---
    print('Installing npm dependencies...')
    result = subprocess.run(
        ['npm', 'install'],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=120
    )
    print(f'npm install stdout: {result.stdout[-500:] if result.stdout else ""}')
    if result.returncode != 0:
        print(f'npm install stderr: {result.stderr[-500:] if result.stderr else ""}')

    # Verify node_modules exists
    if os.path.isdir(f'{PROJECT_DIR}/node_modules'):
        print('node_modules installed successfully')
    else:
        print('WARNING: node_modules directory not found')

    # Verify tests FAIL with buggy regex (expected behavior)
    print('Running tests to confirm bug exists...')
    test_result = subprocess.run(
        ['npx', 'jest', '--verbose'],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=60
    )
    print(f'Test output (last 500 chars): {test_result.stdout[-500:] if test_result.stdout else ""}')
    print(f'Test stderr (last 500 chars): {test_result.stderr[-500:] if test_result.stderr else ""}')
    print(f'Tests exited with code: {test_result.returncode} (non-zero expected due to bug)')

    # Ensure NO .vscode directory exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print('Removed existing .vscode directory')

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
