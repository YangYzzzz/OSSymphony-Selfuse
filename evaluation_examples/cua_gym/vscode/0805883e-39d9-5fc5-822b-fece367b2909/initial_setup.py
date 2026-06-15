"""
Initial Setup: Create a git repo workspace with package.json for VSCode
Task ID: vscode_ops_069
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_069'
PROJECT_DIR = f'{WORKDIR}/my-service'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=PROJECT_DIR, check=True,
                   capture_output=True)
    subprocess.run(["git", "config", "user.email", "dev@my-service.com"],
                   cwd=PROJECT_DIR, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Developer"],
                   cwd=PROJECT_DIR, check=True, capture_output=True)

    # Create package.json
    package_json = {
        "name": "my-service",
        "version": "1.0.0",
        "description": "A backend microservice for order processing",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "eslint": "^8.56.0",
            "supertest": "^6.3.3"
        },
        "keywords": ["microservice", "orders", "api"],
        "author": "Engineering Team",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # Create src directory with a basic index.js
    src_dir = os.path.join(PROJECT_DIR, "src")
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, "index.js"), "w") as f:
        f.write("""const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/orders', (req, res) => {
  res.json({ orders: [], total: 0 });
});

app.post('/api/orders', (req, res) => {
  const { customerId, items } = req.body;
  if (!customerId || !items) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  res.status(201).json({ orderId: Date.now(), customerId, items, status: 'created' });
});

app.listen(port, () => {
  console.log(`Order service running on port ${port}`);
});

module.exports = app;
""")

    # Create a test file
    test_dir = os.path.join(PROJECT_DIR, "__tests__")
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "index.test.js"), "w") as f:
        f.write("""const request = require('supertest');
const app = require('../src/index');

describe('Order Service', () => {
  test('GET /health returns ok status', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('GET /api/orders returns empty list', async () => {
    const res = await request(app).get('/api/orders');
    expect(res.statusCode).toBe(200);
    expect(res.body.orders).toEqual([]);
  });

  test('POST /api/orders creates order', async () => {
    const res = await request(app)
      .post('/api/orders')
      .send({ customerId: 'C001', items: ['Widget A'] });
    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('orderId');
  });

  test('POST /api/orders returns 400 without required fields', async () => {
    const res = await request(app).post('/api/orders').send({});
    expect(res.statusCode).toBe(400);
  });
});
""")

    # Create .gitignore
    with open(os.path.join(PROJECT_DIR, ".gitignore"), "w") as f:
        f.write("node_modules/\n.env\ncoverage/\ndist/\n")

    # Create README
    with open(os.path.join(PROJECT_DIR, "README.md"), "w") as f:
        f.write("""# my-service

A backend microservice for order processing.

## Getting Started

```bash
npm install
npm start
```

## Testing

```bash
npm test
```
""")

    # Make initial git commit
    subprocess.run(["git", "add", "."], cwd=PROJECT_DIR, check=True,
                   capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit: order service"],
                   cwd=PROJECT_DIR, check=True, capture_output=True)

    # Ensure NO .github directory exists
    import shutil
    github_dir = os.path.join(PROJECT_DIR, ".github")
    if os.path.exists(github_dir):
        shutil.rmtree(github_dir)

    # Install YAML extension
    subprocess.run(["code", "--install-extension", "redhat.vscode-yaml"],
                   capture_output=True, timeout=30)

    print(f"Initial workspace created: {PROJECT_DIR}")
    print(f"Files: package.json, src/index.js, __tests__/index.test.js, .gitignore, README.md")

    # Launch VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
