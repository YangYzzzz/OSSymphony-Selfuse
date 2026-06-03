"""
Initial Setup: Create a Node.js logging-app project with console.log usage, no launch.json
Task ID: vscode_td_091
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_091'
PROJECT_DIR = f'{WORKDIR}/projects/logging-app'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create package.json
    package_json = {
        "name": "logging-app",
        "version": "1.0.0",
        "description": "A Node.js application with extensive logging",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "node --inspect src/app.js"
        },
        "keywords": ["logging", "nodejs"],
        "author": "Sarah Chen",
        "license": "MIT",
        "dependencies": {}
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src/app.js with extensive console.log usage
    app_js_content = '''const http = require('http');

const PORT = 3000;
const HOST = '0.0.0.0';

// Application configuration
const config = {
    appName: 'LoggingApp',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development'
};

console.log(`[${config.appName}] Starting application v${config.version}`);
console.log(`[${config.appName}] Environment: ${config.environment}`);

// Simple in-memory data store
const dataStore = new Map();

function handleRequest(req, res) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.url}`);

    if (req.url === '/health') {
        console.log('[HealthCheck] Service is healthy');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', uptime: process.uptime() }));
        return;
    }

    if (req.url === '/api/data' && req.method === 'GET') {
        const entries = Array.from(dataStore.entries());
        console.log(`[DataStore] Returning ${entries.length} entries`);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(entries));
        return;
    }

    if (req.url === '/api/data' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
            console.log(`[DataStore] Receiving data chunk: ${chunk.length} bytes`);
        });
        req.on('end', () => {
            try {
                const parsed = JSON.parse(body);
                const id = Date.now().toString();
                dataStore.set(id, parsed);
                console.log(`[DataStore] Stored new entry with id: ${id}`);
                console.log(`[DataStore] Total entries: ${dataStore.size}`);
                res.writeHead(201, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ id, data: parsed }));
            } catch (err) {
                console.log(`[Error] Failed to parse request body: ${err.message}`);
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });
        return;
    }

    console.log(`[Router] No handler found for ${req.method} ${req.url}`);
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
}

const server = http.createServer(handleRequest);

server.listen(PORT, HOST, () => {
    console.log(`[${config.appName}] Server listening on http://${HOST}:${PORT}`);
    console.log(`[${config.appName}] Ready to accept connections`);
});

process.on('SIGTERM', () => {
    console.log(`[${config.appName}] Received SIGTERM, shutting down gracefully`);
    server.close(() => {
        console.log(`[${config.appName}] Server closed`);
        process.exit(0);
    });
});

process.on('uncaughtException', (err) => {
    console.log(`[${config.appName}] Uncaught exception: ${err.message}`);
    console.log(err.stack);
    process.exit(1);
});
'''
    with open(f'{SRC_DIR}/app.js', 'w') as f:
        f.write(app_js_content)

    # Ensure NO .vscode/launch.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - package.json')
    print(f'  - src/app.js (with console.log statements)')
    print(f'  - No .vscode/launch.json')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
