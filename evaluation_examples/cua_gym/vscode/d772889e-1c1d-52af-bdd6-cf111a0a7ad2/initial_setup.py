"""
Initial Setup: Create project directory structure for REST Client API testing
Task ID: vscode_gf3_014
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_014'
PROJECT_DIR = f'{WORKDIR}/projects'
DOCS_DIR = f'{PROJECT_DIR}/docs'

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
    # 1. Create project directory structure
    os.makedirs(DOCS_DIR, exist_ok=True)
    print(f'Created directory: {DOCS_DIR}')

    # 2. Add some existing project files for realism
    # A simple README for the project
    readme_path = f'{PROJECT_DIR}/README.md'
    with open(readme_path, 'w') as f:
        f.write("""# Auth Service API

A JWT-secured REST API for user authentication and resource management.

## Endpoints

- `POST /auth/token` — Obtain a JWT token with valid credentials
- `GET /users/me` — Retrieve the authenticated user's profile
- `GET /resources` — List all available resources (requires auth)

## Running Locally

```bash
npm install
npm start
```

The server starts on `http://localhost:4000`.

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header.
Obtain a token by posting credentials to `/auth/token`.
""")
    print(f'Created: {readme_path}')

    # A package.json stub
    package_path = f'{PROJECT_DIR}/package.json'
    with open(package_path, 'w') as f:
        f.write("""{
  "name": "auth-service-api",
  "version": "1.2.0",
  "description": "JWT-secured REST API for authentication",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.1",
    "bcrypt": "^5.1.0"
  }
}
""")
    print(f'Created: {package_path}')

    # An existing .http file for a different endpoint (adds realism to docs/ folder)
    health_http_path = f'{DOCS_DIR}/health-check.http'
    with open(health_http_path, 'w') as f:
        f.write("""### Health Check
GET http://localhost:4000/health

### Version Info
GET http://localhost:4000/version
""")
    print(f'Created: {health_http_path}')

    # 3. Install REST Client extension
    print('Installing REST Client extension...')
    result = subprocess.run(
        ['code', '--install-extension', 'humao.rest-client'],
        capture_output=True, text=True
    )
    print(f'Extension install: {result.stdout.strip()}')
    if result.returncode != 0:
        print(f'Extension install stderr: {result.stderr.strip()}')

    # 4. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
