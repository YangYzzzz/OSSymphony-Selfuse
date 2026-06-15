"""
Initial Setup: Open ~/projects/build-app and prepare launch.json without preLaunchTask
Task ID: vscode_dbg_016
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_016'
PROJECT_DIR = f'{WORKDIR}/projects/build-app'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'
TASKS_JSON = f'{VSCODE_DIR}/tasks.json'
PACKAGE_JSON = f'{PROJECT_DIR}/package.json'
SRC_DIR = f'{PROJECT_DIR}/src'
DIST_DIR = f'{PROJECT_DIR}/dist'


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
    # Create directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

    # Create launch.json WITHOUT preLaunchTask (initial state)
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Launch Program",
                "skipFiles": [
                    "<node_internals>/**"
                ],
                "program": "${workspaceFolder}/dist/app.js",
                "outFiles": [
                    "${workspaceFolder}/dist/**/*.js"
                ]
            }
        ]
    }
    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)
    print(f'Created: {LAUNCH_JSON}')

    # Create tasks.json with 'npm: build' task
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "type": "npm",
                "script": "build",
                "label": "npm: build",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": [
                    "$tsc"
                ],
                "detail": "tsc -p tsconfig.json"
            }
        ]
    }
    with open(TASKS_JSON, 'w') as f:
        json.dump(tasks_config, f, indent=4)
    print(f'Created: {TASKS_JSON}')

    # Create package.json with build script
    package_config = {
        "name": "build-app",
        "version": "1.0.0",
        "description": "A Node.js application with TypeScript build pipeline",
        "main": "dist/app.js",
        "scripts": {
            "build": "tsc -p tsconfig.json",
            "start": "node dist/app.js",
            "dev": "ts-node src/app.ts",
            "test": "jest"
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/node": "^18.0.0",
            "ts-node": "^10.9.0"
        },
        "keywords": [],
        "author": "Dev Team",
        "license": "MIT"
    }
    with open(PACKAGE_JSON, 'w') as f:
        json.dump(package_config, f, indent=4)
    print(f'Created: {PACKAGE_JSON}')

    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=4)
    print(f'Created: {PROJECT_DIR}/tsconfig.json')

    # Create src/app.ts - realistic TypeScript source
    app_ts_content = '''import * as http from 'http';
import * as path from 'path';

interface ServerConfig {
    port: number;
    host: string;
    environment: string;
}

const config: ServerConfig = {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || 'localhost',
    environment: process.env.NODE_ENV || 'development',
};

function createRequestHandler() {
    return (req: http.IncomingMessage, res: http.ServerResponse): void => {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] ${req.method} ${req.url}`);

        if (req.url === '/health') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'ok', uptime: process.uptime() }));
            return;
        }

        if (req.url === '/api/info') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                name: 'build-app',
                version: '1.0.0',
                environment: config.environment,
            }));
            return;
        }

        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found', path: req.url }));
    };
}

const server = http.createServer(createRequestHandler());

server.listen(config.port, config.host, () => {
    console.log(`Server running at http://${config.host}:${config.port}`);
    console.log(`Environment: ${config.environment}`);
});

server.on('error', (err: NodeJS.ErrnoException) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`Port ${config.port} is already in use`);
        process.exit(1);
    }
    throw err;
});

export { server, config };
'''
    with open(f'{SRC_DIR}/app.ts', 'w') as f:
        f.write(app_ts_content)
    print(f'Created: {SRC_DIR}/app.ts')

    # Create dist/app.js - compiled output
    app_js_content = '''"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.config = exports.server = void 0;
const http = require("http");
const config = {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || 'localhost',
    environment: process.env.NODE_ENV || 'development',
};
exports.config = config;
function createRequestHandler() {
    return (req, res) => {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] ${req.method} ${req.url}`);
        if (req.url === '/health') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'ok', uptime: process.uptime() }));
            return;
        }
        if (req.url === '/api/info') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                name: 'build-app',
                version: '1.0.0',
                environment: config.environment,
            }));
            return;
        }
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found', path: req.url }));
    };
}
const server = http.createServer(createRequestHandler());
exports.server = server;
server.listen(config.port, config.host, () => {
    console.log(`Server running at http://${config.host}:${config.port}`);
    console.log(`Environment: ${config.environment}`);
});
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`Port ${config.port} is already in use`);
        process.exit(1);
    }
    throw err;
});
'''
    with open(f'{DIST_DIR}/app.js', 'w') as f:
        f.write(app_js_content)
    print(f'Created: {DIST_DIR}/app.js')

    # Create .gitignore
    gitignore_content = '''node_modules/
dist/
*.js.map
*.d.ts
.env
.env.local
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'launch.json has NO preLaunchTask (initial state)')

    # GUI-ready startup: open VSCode with the build-app project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Open launch.json in the editor so the agent can see it
    launch_gui(f'code "{LAUNCH_JSON}"', delay_sec=1.5)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
