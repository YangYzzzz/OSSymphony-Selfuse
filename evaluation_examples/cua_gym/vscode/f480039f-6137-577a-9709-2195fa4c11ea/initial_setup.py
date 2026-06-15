"""
Initial Setup: Create monorepo structure with three packages for VSCode task configuration
Task ID: vscode_gf2_043
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_043'
MONOREPO = f'{WORKDIR}/projects/monorepo'


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


def create_package(pkg_path, name, description, dependencies=None):
    """Create a realistic package directory with package.json and source files."""
    os.makedirs(os.path.join(pkg_path, 'src'), exist_ok=True)
    os.makedirs(os.path.join(pkg_path, 'test'), exist_ok=True)

    pkg_json = {
        "name": f"@monorepo/{name}",
        "version": "1.2.0",
        "description": description,
        "main": "src/index.js",
        "scripts": {
            "build": "echo 'Building {name}...' && exit 0".format(name=name),
            "test": "echo 'Testing {name}...' && exit 0".format(name=name),
            "lint": "echo 'Linting {name}...' && exit 0"
        },
        "dependencies": dependencies or {},
        "devDependencies": {
            "jest": "^29.7.0",
            "typescript": "^5.3.3"
        }
    }
    with open(os.path.join(pkg_path, 'package.json'), 'w') as f:
        json.dump(pkg_json, f, indent=2)

    return pkg_json


def create_initial():
    # Create monorepo root
    os.makedirs(MONOREPO, exist_ok=True)

    # Root package.json
    root_pkg = {
        "name": "monorepo",
        "version": "1.0.0",
        "private": True,
        "description": "Enterprise monorepo with auth, api, and ui packages",
        "workspaces": [
            "packages/*"
        ],
        "scripts": {
            "clean": "rm -rf packages/*/dist"
        }
    }
    with open(os.path.join(MONOREPO, 'package.json'), 'w') as f:
        json.dump(root_pkg, f, indent=2)

    # --- packages/auth ---
    auth_path = os.path.join(MONOREPO, 'packages', 'auth')
    create_package(auth_path, 'auth', 'Authentication and authorization module', {
        "jsonwebtoken": "^9.0.2",
        "bcryptjs": "^2.4.3"
    })

    with open(os.path.join(auth_path, 'src', 'index.js'), 'w') as f:
        f.write("""const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';
const TOKEN_EXPIRY = '24h';

class AuthService {
    async hashPassword(password) {
        const salt = await bcrypt.genSalt(12);
        return bcrypt.hash(password, salt);
    }

    async verifyPassword(password, hash) {
        return bcrypt.compare(password, hash);
    }

    generateToken(userId, roles = []) {
        return jwt.sign(
            { sub: userId, roles, iat: Date.now() },
            JWT_SECRET,
            { expiresIn: TOKEN_EXPIRY }
        );
    }

    verifyToken(token) {
        try {
            return jwt.verify(token, JWT_SECRET);
        } catch (err) {
            throw new Error('Invalid or expired token');
        }
    }
}

module.exports = { AuthService };
""")

    with open(os.path.join(auth_path, 'test', 'auth.test.js'), 'w') as f:
        f.write("""const { AuthService } = require('../src/index');

describe('AuthService', () => {
    const auth = new AuthService();

    test('should hash and verify password', async () => {
        const hash = await auth.hashPassword('secure123');
        expect(await auth.verifyPassword('secure123', hash)).toBe(true);
        expect(await auth.verifyPassword('wrong', hash)).toBe(false);
    });

    test('should generate and verify JWT token', () => {
        const token = auth.generateToken('user-42', ['admin']);
        const decoded = auth.verifyToken(token);
        expect(decoded.sub).toBe('user-42');
        expect(decoded.roles).toContain('admin');
    });
});
""")

    # --- packages/api ---
    api_path = os.path.join(MONOREPO, 'packages', 'api')
    create_package(api_path, 'api', 'REST API server with Express', {
        "express": "^4.18.2",
        "cors": "^2.8.5",
        "helmet": "^7.1.0",
        "@monorepo/auth": "1.2.0"
    })

    with open(os.path.join(api_path, 'src', 'index.js'), 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { AuthService } = require('@monorepo/auth');

const app = express();
const auth = new AuthService();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(helmet());
app.use(express.json());

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;
    // Simplified login logic
    const token = auth.generateToken(email, ['user']);
    res.json({ token, expiresIn: '24h' });
});

app.get('/api/users', (req, res) => {
    res.json({
        users: [
            { id: 1, name: 'Sarah Chen', department: 'Engineering' },
            { id: 2, name: 'Marcus Johnson', department: 'Product' },
            { id: 3, name: 'Priya Patel', department: 'Design' },
        ]
    });
});

if (require.main === module) {
    app.listen(PORT, () => console.log(`API running on port ${PORT}`));
}

module.exports = { app };
""")

    with open(os.path.join(api_path, 'test', 'api.test.js'), 'w') as f:
        f.write("""const request = require('supertest');
const { app } = require('../src/index');

describe('API endpoints', () => {
    test('GET /api/health returns ok', async () => {
        const res = await request(app).get('/api/health');
        expect(res.status).toBe(200);
        expect(res.body.status).toBe('ok');
    });

    test('GET /api/users returns user list', async () => {
        const res = await request(app).get('/api/users');
        expect(res.status).toBe(200);
        expect(res.body.users.length).toBe(3);
    });
});
""")

    # --- packages/ui ---
    ui_path = os.path.join(MONOREPO, 'packages', 'ui')
    create_package(ui_path, 'ui', 'React UI component library', {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "@monorepo/api": "1.2.0"
    })

    with open(os.path.join(ui_path, 'src', 'index.js'), 'w') as f:
        f.write("""import React from 'react';

export function Button({ label, onClick, variant = 'primary' }) {
    const styles = {
        primary: { backgroundColor: '#2563eb', color: '#fff' },
        secondary: { backgroundColor: '#6b7280', color: '#fff' },
        danger: { backgroundColor: '#dc2626', color: '#fff' },
    };
    return (
        <button
            onClick={onClick}
            style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 600,
                ...styles[variant],
            }}
        >
            {label}
        </button>
    );
}

export function Card({ title, children }) {
    return (
        <div style={{
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            padding: '16px',
            marginBottom: '12px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
            {title && <h3 style={{ marginTop: 0 }}>{title}</h3>}
            {children}
        </div>
    );
}

export function UserList({ users }) {
    return (
        <div>
            {users.map(user => (
                <Card key={user.id} title={user.name}>
                    <p>Department: {user.department}</p>
                </Card>
            ))}
        </div>
    );
}
""")

    with open(os.path.join(ui_path, 'test', 'ui.test.js'), 'w') as f:
        f.write("""import React from 'react';
import { render, screen } from '@testing-library/react';
import { Button, Card } from '../src/index';

describe('UI Components', () => {
    test('Button renders with label', () => {
        render(<Button label="Click Me" />);
        expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    test('Card renders with title', () => {
        render(<Card title="Test Card"><p>Content</p></Card>);
        expect(screen.getByText('Test Card')).toBeInTheDocument();
    });
});
""")

    # Create .vscode directory but NO tasks.json (agent must create it)
    vscode_dir = os.path.join(MONOREPO, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # Add a basic settings.json so the .vscode folder isn't empty
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "files.exclude": {
            "**/node_modules": True,
            "**/dist": True
        }
    }
    with open(os.path.join(vscode_dir, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # Create a README
    with open(os.path.join(MONOREPO, 'README.md'), 'w') as f:
        f.write("""# Enterprise Monorepo

A multi-package monorepo containing authentication, API, and UI modules.

## Packages

- **packages/auth** - Authentication and authorization (JWT, bcrypt)
- **packages/api** - REST API server (Express)
- **packages/ui** - React UI component library

## Development

Each package can be built independently:

```bash
cd packages/auth && npm run build
cd packages/api && npm run build
cd packages/ui && npm run build
```

## Testing

Run tests for each package:

```bash
cd packages/auth && npm test
cd packages/api && npm test
cd packages/ui && npm test
```
""")

    print(f'Monorepo structure created at: {MONOREPO}')
    print(f'Packages: auth, api, ui')
    print(f'.vscode/settings.json created (NO tasks.json)')

    # GUI-ready: open VSCode with the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
