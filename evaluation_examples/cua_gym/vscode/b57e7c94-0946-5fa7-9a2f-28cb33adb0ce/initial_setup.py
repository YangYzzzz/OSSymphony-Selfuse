"""
Initial Setup: Add CLI args to VSCode launch.json Node.js config
Task ID: vscode_dbg_009
Domain: vs_code

Creates ~/projects/node-cli with a realistic Node.js CLI project structure,
including a .vscode/launch.json that has a Node.js debug config WITHOUT 'args'.
Opens VSCode with the project folder so the agent can edit the launch.json.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_009'
PROJECT_DIR = f'{WORKDIR}/projects/node-cli'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'


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
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create cli.js — a realistic Node.js CLI entry point
    cli_js_content = """\
#!/usr/bin/env node
'use strict';

const http = require('http');

// Parse command-line arguments
const args = process.argv.slice(2);
let verbose = false;
let port = 8080;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--verbose') {
        verbose = true;
    } else if (args[i] === '--port' && args[i + 1]) {
        port = parseInt(args[i + 1], 10);
        i++;
    }
}

if (verbose) {
    console.log(`[INFO] Starting server on port ${port}`);
}

const server = http.createServer((req, res) => {
    if (verbose) {
        console.log(`[REQUEST] ${req.method} ${req.url}`);
    }
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('node-cli server running\\n');
});

server.listen(port, '127.0.0.1', () => {
    console.log(`Server listening at http://127.0.0.1:${port}`);
});
"""
    with open(f'{PROJECT_DIR}/cli.js', 'w') as f:
        f.write(cli_js_content)

    # Create package.json
    package_json = {
        "name": "node-cli",
        "version": "1.0.0",
        "description": "A simple Node.js CLI HTTP server",
        "main": "cli.js",
        "scripts": {
            "start": "node cli.js",
            "debug": "node --inspect cli.js"
        },
        "keywords": ["cli", "http", "server"],
        "author": "Dev Team",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create README.md
    readme_content = """\
# node-cli

A lightweight Node.js CLI HTTP server for development and testing.

## Usage

```bash
node cli.js [options]

Options:
  --verbose       Enable verbose logging
  --port <number> Port to listen on (default: 8080)
```

## Examples

```bash
node cli.js --verbose --port 3000
node cli.js --port 9090
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Create .vscode/launch.json WITHOUT 'args' property
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Launch CLI",
                "program": "${workspaceFolder}/cli.js",
                "console": "integratedTerminal",
                "skipFiles": [
                    "<node_internals>/**"
                ]
            }
        ]
    }
    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'launch.json created (no args): {LAUNCH_JSON}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder DISPLAY=:0')


create_initial()
