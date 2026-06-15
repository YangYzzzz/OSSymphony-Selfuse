"""
Initial Setup: Fix YAML indentation in GitHub Actions deploy.yml
Task ID: vscode_gf3_023
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_023'
PROJECT_DIR = f'{WORKDIR}/projects/ci-demo'
WORKFLOW_DIR = f'{PROJECT_DIR}/.github/workflows'
DEPLOY_YML = f'{WORKFLOW_DIR}/deploy.yml'


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
    os.makedirs(WORKFLOW_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Initialize git repo
    subprocess.run(['git', 'init', PROJECT_DIR], capture_output=True)
    subprocess.run(
        ['git', 'config', 'user.email', 'devops@acmecorp.com'],
        cwd=PROJECT_DIR, capture_output=True,
    )
    subprocess.run(
        ['git', 'config', 'user.name', 'DevOps Team'],
        cwd=PROJECT_DIR, capture_output=True,
    )

    # Create a realistic README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# CI Demo Application

A sample Node.js application used for demonstrating CI/CD pipeline configuration
with GitHub Actions.

## Getting Started

```bash
npm install
npm run build
npm test
```

## Deployment

Deployments are handled automatically via GitHub Actions when changes are pushed
to the `main` branch. See `.github/workflows/deploy.yml` for the pipeline config.

## Architecture

- `src/` - Application source code
- `tests/` - Unit and integration tests
- `Dockerfile` - Container build specification
""")

    # Create a simple package.json
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "ci-demo",
  "version": "2.1.0",
  "description": "CI/CD demo application for Acme Corp",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "build": "npm run lint && tsc",
    "test": "jest --coverage",
    "lint": "eslint src/ tests/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "eslint": "^8.56.0",
    "typescript": "^5.3.3"
  }
}
""")

    # Create a simple source file
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""const express = require('express');
const dotenv = require('dotenv');
const logger = require('./logger');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/health', (req, res) => {
  res.json({ status: 'ok', version: '2.1.0' });
});

app.get('/api/data', (req, res) => {
  logger.info('Data endpoint called');
  res.json({ message: 'Hello from CI Demo' });
});

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

module.exports = app;
""")

    # Create a logger module
    with open(f'{PROJECT_DIR}/src/logger.js', 'w') as f:
        f.write("""const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
  ],
});

module.exports = logger;
""")

    # Create a test file
    with open(f'{PROJECT_DIR}/tests/index.test.js', 'w') as f:
        f.write("""const request = require('supertest');
const app = require('../src/index');

describe('Health endpoint', () => {
  it('should return 200 with status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});

describe('Data endpoint', () => {
  it('should return message', async () => {
    const res = await request(app).get('/api/data');
    expect(res.statusCode).toBe(200);
    expect(res.body.message).toBeDefined();
  });
});
""")

    # Create Dockerfile
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write("""FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["node", "src/index.js"]
""")

    # Create the BROKEN deploy.yml - this is the key file with indentation errors
    # The 'steps' is indented 2 spaces under the job instead of 4,
    # and 'uses'/'name'/'with' are improperly indented under steps
    broken_yaml = """name: Deploy to Production

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: acmecorp/ci-demo

jobs:
  build-and-test:
    runs-on: ubuntu-latest
  steps:
    - name: Checkout repository
    uses: actions/checkout@v4

    - name: Setup Node.js
    uses: actions/setup-node@v4
    with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
    run: npm ci

    - name: Run linter
    run: npm run lint

    - name: Run tests
    run: npm test

  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
  steps:
    - name: Checkout repository
    uses: actions/checkout@v4

    - name: Login to Container Registry
    uses: docker/login-action@v3
    with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push Docker image
    uses: docker/build-push-action@v5
    with:
        context: .
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

    - name: Deploy to staging
    run: |
        echo "Deploying ${{ github.sha }} to staging..."
        curl -X POST https://deploy.acmecorp.internal/api/deploy \\
          -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}" \\
          -d '{"image": "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}", "env": "staging"}'
"""

    with open(DEPLOY_YML, 'w') as f:
        f.write(broken_yaml)

    # Create another valid workflow file to make the project more realistic
    with open(f'{WORKFLOW_DIR}/ci.yml', 'w') as f:
        f.write("""name: CI Checks

on:
  pull_request:
    branches:
      - main
      - develop

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install
        run: npm ci

      - name: Lint
        run: npm run lint
""")

    # Create .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
dist/
coverage/
.env
*.log
""")

    # Initial git commit
    subprocess.run(['git', 'add', '.'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(
        ['git', 'commit', '-m', 'Initial project setup with CI/CD pipeline'],
        cwd=PROJECT_DIR, capture_output=True,
    )

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Broken deploy.yml created: {DEPLOY_YML}')

    # Launch VSCode with the broken file open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{DEPLOY_YML}"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
