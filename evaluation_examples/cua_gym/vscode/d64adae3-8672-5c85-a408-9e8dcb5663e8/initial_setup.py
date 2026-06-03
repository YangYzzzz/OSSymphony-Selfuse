"""
Initial Setup: Create ~/projects/fullstack workspace without .vscode directory.
Task ID: vscode_ext_030
Domain: vs_code

Creates a realistic fullstack project folder at ~/projects/fullstack/ with:
  - README.md
  - package.json
  - src/ directory with frontend and backend code
  - NO .vscode/ directory (task requires creating it)
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/projects/fullstack'


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
    # Remove any existing .vscode to ensure clean initial state
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print(f'Removed existing .vscode directory: {vscode_dir}')

    # Create the project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'frontend'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'backend'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # README.md
    readme = """\
# Fullstack Project

A modern fullstack web application with React frontend and Node.js backend.

## Tech Stack

- **Frontend**: React, TypeScript, Prettier
- **Backend**: Node.js, Express
- **Database**: PostgreSQL
- **Container**: Docker

## Getting Started

### Prerequisites
- Node.js >= 18
- Docker Desktop
- Python 3.9+

### Installation

```bash
npm install
```

### Running the Application

```bash
# Start frontend
npm run start:frontend

# Start backend
npm run start:backend

# Or use Docker
docker-compose up
```

## Project Structure

```
fullstack/
├── src/
│   ├── frontend/        # React application
│   └── backend/         # Express API server
├── tests/               # Test suites
├── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # package.json
    package_json = {
        "name": "fullstack-project",
        "version": "1.0.0",
        "description": "A modern fullstack web application",
        "scripts": {
            "start:frontend": "cd src/frontend && npm start",
            "start:backend": "cd src/backend && node server.js",
            "test": "jest",
            "lint": "eslint src/",
            "format": "prettier --write src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "axios": "^1.4.0",
            "cors": "^2.8.5"
        },
        "devDependencies": {
            "@types/react": "^18.2.0",
            "@types/express": "^4.17.17",
            "eslint": "^8.45.0",
            "prettier": "^3.0.0",
            "jest": "^29.6.0",
            "typescript": "^5.1.0"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/frontend/App.tsx
    app_tsx = """\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: number;
  name: string;
  email: string;
}

const App: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get<User[]>('/api/users');
        setUsers(response.data);
      } catch (error) {
        console.error('Failed to fetch users:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app">
      <header>
        <h1>Fullstack Application</h1>
      </header>
      <main>
        <h2>Users ({users.length})</h2>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {user.name} - {user.email}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
};

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'frontend', 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # src/backend/server.js
    server_js = """\
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Mock data
const users = [
  { id: 1, name: 'Sarah Chen', email: 'sarah.chen@example.com' },
  { id: 2, name: 'Marcus Johnson', email: 'm.johnson@example.com' },
  { id: 3, name: 'Emily Rodriguez', email: 'emily.r@example.com' },
  { id: 4, name: 'David Kim', email: 'd.kim@example.com' },
  { id: 5, name: 'Jessica Patel', email: 'jessica.p@example.com' },
];

app.get('/api/users', (req, res) => {
  res.json(users);
});

app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  const newUser = { id: users.length + 1, name, email };
  users.push(newUser);
  res.status(201).json(newUser);
});

app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});

module.exports = app;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'backend', 'server.js'), 'w') as f:
        f.write(server_js)

    # Dockerfile
    dockerfile = """\
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY src/ ./src/

EXPOSE 3001

CMD ["node", "src/backend/server.js"]
"""
    with open(os.path.join(PROJECT_DIR, 'Dockerfile'), 'w') as f:
        f.write(dockerfile)

    # docker-compose.yml
    docker_compose = """\
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - PORT=3001
    depends_on:
      - db

  frontend:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./src/frontend:/app
    ports:
      - "3000:3000"
    command: npm start

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fullstack_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: securepassword123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""
    with open(os.path.join(PROJECT_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose)

    # .gitignore
    gitignore = """\
node_modules/
dist/
build/
.env
.env.local
*.log
.DS_Store
coverage/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # tests/api.test.js
    test_js = """\
const request = require('supertest');
const app = require('../src/backend/server');

describe('Users API', () => {
  test('GET /api/users returns all users', async () => {
    const response = await request(app).get('/api/users');
    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body.length).toBeGreaterThan(0);
  });

  test('GET /api/users/:id returns specific user', async () => {
    const response = await request(app).get('/api/users/1');
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('id', 1);
    expect(response.body).toHaveProperty('name');
    expect(response.body).toHaveProperty('email');
  });

  test('GET /api/users/:id returns 404 for unknown user', async () => {
    const response = await request(app).get('/api/users/999');
    expect(response.status).toBe(404);
  });
});
"""
    with open(os.path.join(PROJECT_DIR, 'tests', 'api.test.js'), 'w') as f:
        f.write(test_js)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'Files created:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = '  ' * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '  ' * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Verify .vscode does NOT exist in initial state
    if not os.path.exists(os.path.join(PROJECT_DIR, '.vscode')):
        print('VERIFIED: No .vscode directory in initial state (correct)')
    else:
        print('WARNING: .vscode directory exists in initial state (WRONG!)')

    # GUI-ready startup: Open VSCode with the fullstack project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 pointing to ~/projects/fullstack')


create_initial()
