"""
Initial Setup: Create a web-server project with tasks.json but no launch.json
Task ID: vscode_td_093
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_093'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'web-server')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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

    # Create a realistic Node.js server file
    server_js = os.path.join(PROJECT_DIR, 'server.js')
    with open(server_js, 'w') as f:
        f.write("""\
const http = require('http');

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
    if (req.url === '/api/status') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'running', uptime: process.uptime() }));
        return;
    }

    if (req.url === '/api/data') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ items: ['alpha', 'beta', 'gamma'], count: 3 }));
        return;
    }

    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
        <!DOCTYPE html>
        <html>
        <head><title>Web Server Dashboard</title></head>
        <body>
            <h1>Welcome to the Dashboard</h1>
            <p>Server is running on port ${port}</p>
            <ul>
                <li><a href="/api/status">Status API</a></li>
                <li><a href="/api/data">Data API</a></li>
            </ul>
        </body>
        </html>
    `);
});

server.listen(port, hostname, () => {
    console.log(`Listening on port ${port}`);
});
""")

    # Create package.json
    package_json = os.path.join(PROJECT_DIR, 'package.json')
    with open(package_json, 'w') as f:
        json.dump({
            "name": "web-server",
            "version": "1.0.0",
            "description": "A simple web server for dashboard data",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "node --watch server.js"
            },
            "author": "Sarah Chen",
            "license": "MIT"
        }, f, indent=2)

    # Create .vscode/tasks.json with "Start Server" task
    tasks_json = os.path.join(VSCODE_DIR, 'tasks.json')
    with open(tasks_json, 'w') as f:
        json.dump({
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Start Server",
                    "type": "shell",
                    "command": "node server.js",
                    "isBackground": True,
                    "problemMatcher": {
                        "pattern": {
                            "regexp": "^$"
                        },
                        "background": {
                            "activeOnStart": True,
                            "beginsPattern": "^.*$",
                            "endsPattern": "^Listening on port \\d+$"
                        }
                    },
                    "group": "build"
                }
            ]
        }, f, indent=4)

    # Create a README.md for the project
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write("""\
# Web Server Dashboard

A simple Node.js HTTP server that provides a dashboard and REST API endpoints.

## Endpoints

- `GET /` - Dashboard homepage
- `GET /api/status` - Server status and uptime
- `GET /api/data` - Sample data endpoint

## Running

```bash
npm start
```

The server will output "Listening on port 3000" when ready.

## Development

The project uses a VSCode task ("Start Server") defined in `.vscode/tasks.json`
to launch the server. You can configure a debug launch configuration to
automatically start the server and open a browser when it's ready.
""")

    # Ensure NO launch.json exists (task requires agent to create it)
    launch_json_path = os.path.join(VSCODE_DIR, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'tasks.json created at: {tasks_json}')
    print(f'No launch.json exists (as required)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
