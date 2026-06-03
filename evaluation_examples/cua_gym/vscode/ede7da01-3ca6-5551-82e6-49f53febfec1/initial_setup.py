"""
Initial Setup: Create workspace folder for VSCode tasks.json task
Task ID: vscode_td_001
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_001'
WORKSPACE = f'{WORKDIR}/projects/demo-app'

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
    # Create workspace directory structure (no .vscode folder)
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create some realistic project files so the workspace isn't empty
    # Package.json
    import json
    package_json = {
        "name": "demo-app",
        "version": "1.0.0",
        "description": "A simple demo application",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "author": "Sarah Chen",
        "license": "MIT"
    }
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src directory with a simple JS file
    src_dir = os.path.join(WORKSPACE, 'src')
    os.makedirs(src_dir, exist_ok=True)

    index_js = '''const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello World from Demo App!');
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
'''
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # Create a README
    readme = '''# Demo App

A simple Node.js demo application for testing purposes.

## Getting Started

```bash
npm start
```

This will start the server on port 3000.
'''
    with open(os.path.join(WORKSPACE, 'README.md'), 'w') as f:
        f.write(readme)

    # Ensure NO .vscode directory exists (task requires creating it)
    vscode_dir = os.path.join(WORKSPACE, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Workspace created: {WORKSPACE}')
    print(f'.vscode directory does NOT exist (as required by task)')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
