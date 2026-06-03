"""
Initial Setup: Configure VSCode with e2e-tests project for Playwright testing
Task ID: vscode_gf5_030
Domain: vscode

Creates:
- ~/projects/e2e-tests/ with a basic Node.js project
- A simple Express web server running at localhost:3000 with title 'My App'
- No test framework configured (task is to set up Playwright)
- VSCode opened with the project folder
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_030'
PROJECT_DIR = f'{WORKDIR}/projects/e2e-tests'


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


def install_nodejs():
    """Install Node.js 18 locally if not already available."""
    import shutil as _shutil

    # Check if node is already on PATH
    if _shutil.which('node'):
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        print(f'Node.js already installed: {result.stdout.strip()}')
        return

    print('Installing Node.js 18 (user-local)...')
    node_dir = os.path.expanduser('~/nodejs')
    os.makedirs(node_dir, exist_ok=True)

    # Download Node.js 18 binary tarball
    tarball = f'{node_dir}/node-v18.20.2-linux-x64.tar.xz'
    result = subprocess.run(
        ['curl', '-fsSL', '-o', tarball,
         'https://nodejs.org/dist/v18.20.2/node-v18.20.2-linux-x64.tar.xz'],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f'Download failed: {result.stderr}')
        return

    # Extract
    result = subprocess.run(
        ['tar', '-xJf', tarball, '-C', node_dir, '--strip-components=1'],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f'Extract failed: {result.stderr}')
        return

    # Add to PATH for current process and future shells
    node_bin = f'{node_dir}/bin'
    os.environ['PATH'] = f'{node_bin}:{os.environ["PATH"]}'

    # Also update .bashrc for GUI processes
    bashrc = os.path.expanduser('~/.bashrc')
    path_line = f'\nexport PATH="{node_bin}:$PATH"\n'
    with open(bashrc, 'a') as f:
        f.write(path_line)

    # Verify
    result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
    print(f'Node.js installed: {result.stdout.strip()}')
    result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
    print(f'npm installed: {result.stdout.strip()}')


def create_initial():
    # Install Node.js 18 if needed
    install_nodejs()

    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- package.json (basic Node.js project, NO test framework) ---
    package_json = {
        "name": "e2e-tests",
        "version": "1.0.0",
        "description": "End-to-end testing project for the QA team",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "node server.js"
        },
        "keywords": ["testing", "qa"],
        "author": "QA Team",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- server.js (simple Express server serving 'My App' page) ---
    server_js = '''\
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>My App</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
          margin: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }
        .container {
          text-align: center;
          padding: 2rem;
        }
        h1 { font-size: 3rem; margin-bottom: 0.5rem; }
        p { font-size: 1.2rem; opacity: 0.9; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>My App</h1>
        <p>Welcome to the application dashboard</p>
        <p>Status: Running on port ${PORT}</p>
      </div>
    </body>
    </html>
  `);
});

app.get('/api/status', (req, res) => {
  res.json({ status: 'healthy', uptime: process.uptime() });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/server.js', 'w') as f:
        f.write(server_js)

    # --- .gitignore ---
    gitignore = '''\
node_modules/
dist/
.env
*.log
test-results/
playwright-report/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = '''\
# E2E Tests Project

This project hosts the web application and end-to-end tests for the QA team.

## Getting Started

```bash
npm install
npm start
```

The server will start at http://localhost:3000.

## Testing

No test framework has been configured yet. The QA team plans to implement
cross-browser automated testing using Playwright.
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # --- Install system dependencies for Playwright browsers (agent will need these) ---
    subprocess.run(
        ['bash', '-c', 'echo "password" | sudo -S apt-get install -y libavif13'],
        capture_output=True, text=True, timeout=60
    )

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

    # --- Start the web server in background ---
    print('Starting web server...')
    env = os.environ.copy()
    subprocess.Popen(
        ['node', 'server.js'],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(2)

    # Verify server is running
    try:
        import urllib.request
        resp = urllib.request.urlopen('http://localhost:3000', timeout=5)
        content = resp.read().decode()
        if 'My App' in content:
            print('Server verified: localhost:3000 serves "My App"')
        else:
            print('WARNING: Server responded but title not found')
    except Exception as e:
        print(f'WARNING: Could not verify server: {e}')

    # --- Install Playwright VSCode extension ---
    print('Installing Playwright VSCode extension...')
    result = subprocess.run(
        ['code', '--install-extension', 'ms-playwright.playwright', '--force'],
        capture_output=True, text=True, timeout=60
    )
    print(f'Extension install: {result.stdout.strip()}')

    print(f'Initial project created: {PROJECT_DIR}')

    # --- GUI-ready startup: open VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
