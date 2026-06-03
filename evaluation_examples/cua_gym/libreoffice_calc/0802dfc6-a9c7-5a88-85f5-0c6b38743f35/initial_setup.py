"""
Initial Setup: Create a keybinding that splits the terminal and sends a command
Task ID: vscode_rrt_092
Domain: vscode (keybindings)

Initial state:
- A Node.js project workspace exists at /home/user/vscode_rrt_092/
- keybindings.json is empty (no custom keybindings)
- VSCode is open with the workspace folder
- A terminal is running a dev server
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
TASK_ID = 'vscode_rrt_092'
WORKSPACE_DIR = f'{HOME}/{TASK_ID}'
VSCODE_USER = f'{HOME}/.config/Code/User'
KEYBINDINGS_PATH = f'{VSCODE_USER}/keybindings.json'


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
    # 1. Create a realistic Node.js project workspace
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    os.makedirs(f'{WORKSPACE_DIR}/src', exist_ok=True)
    os.makedirs(f'{WORKSPACE_DIR}/public', exist_ok=True)

    # package.json with dev server and watch scripts
    package_json = {
        "name": "inventory-dashboard",
        "version": "2.1.0",
        "description": "Real-time inventory tracking dashboard",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "node src/server.js",
            "watch": "node src/watcher.js",
            "test": "node src/test.js",
            "build": "echo 'Building production bundle...' && node src/build.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "ws": "^8.14.2",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "chokidar": "^3.5.3"
        },
        "author": "Lena Park <lena.park@inventorytech.io>",
        "license": "MIT"
    }
    with open(f'{WORKSPACE_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Main server file
    server_js = '''const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3200;
const HOST = '127.0.0.1';

const server = http.createServer((req, res) => {
    if (req.url === '/api/inventory') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            items: [
                { sku: 'WH-4410', name: 'Wireless Headphones', qty: 142, warehouse: 'A3' },
                { sku: 'KB-7723', name: 'Mechanical Keyboard', qty: 89, warehouse: 'B1' },
                { sku: 'MN-1156', name: '27-inch Monitor', qty: 34, warehouse: 'A3' },
                { sku: 'MS-9981', name: 'Ergonomic Mouse', qty: 210, warehouse: 'C2' },
            ],
            lastUpdated: new Date().toISOString()
        }));
    } else {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>Inventory Dashboard</h1><p>Server running.</p>');
    }
});

server.listen(PORT, HOST, () => {
    console.log(`[inventory-dashboard] Dev server running at http://${HOST}:${PORT}`);
    console.log('Press Ctrl+C to stop.');
});
'''
    with open(f'{WORKSPACE_DIR}/src/server.js', 'w') as f:
        f.write(server_js)

    # Watcher script (what npm run watch would run)
    watcher_js = '''const fs = require('fs');
const path = require('path');

const WATCH_DIR = path.join(__dirname, '..', 'src');

console.log('[watcher] Watching for file changes in src/...');
console.log('[watcher] Press Ctrl+C to stop.');

fs.watch(WATCH_DIR, { recursive: true }, (eventType, filename) => {
    if (filename && filename.endsWith('.js')) {
        console.log(`[watcher] ${eventType}: ${filename} - rebuilding...`);
    }
});

// Keep alive
setInterval(() => {}, 60000);
'''
    with open(f'{WORKSPACE_DIR}/src/watcher.js', 'w') as f:
        f.write(watcher_js)

    # A simple config file
    env_content = '''# Inventory Dashboard Configuration
PORT=3200
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_prod
LOG_LEVEL=info
CACHE_TTL=300
'''
    with open(f'{WORKSPACE_DIR}/.env', 'w') as f:
        f.write(env_content)

    # README
    readme = '''# Inventory Dashboard

Real-time inventory tracking dashboard for warehouse management.

## Getting Started

```bash
npm install
npm run dev      # Start development server
npm run watch    # Watch for file changes
```

## API Endpoints

- `GET /api/inventory` - Returns current inventory data
'''
    with open(f'{WORKSPACE_DIR}/README.md', 'w') as f:
        f.write(readme)

    # 2. Ensure keybindings.json is empty (no custom keybindings)
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'keybindings.json created (empty): {KEYBINDINGS_PATH}')

    # 3. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('VSCode launched with workspace')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
