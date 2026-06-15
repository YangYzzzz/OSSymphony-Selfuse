"""
Initial Setup: Create a Node.js project for devcontainer configuration task
Task ID: vscode_gf6_025
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_025'
PROJECT_DIR = f'{WORKDIR}/projects/devcontainer-node'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Ensure NO .devcontainer directory exists
    devcontainer_dir = f'{PROJECT_DIR}/.devcontainer'
    if os.path.exists(devcontainer_dir):
        import shutil
        shutil.rmtree(devcontainer_dir)

    # --- src/index.ts (Express app with TypeScript) ---
    index_ts = '''\
import express, { Request, Response } from 'express';
import { Pool } from 'pg';

const app = express();
const port = process.env.PORT || 3000;

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

app.get('/', (_req: Request, res: Response) => {
    res.json({ message: 'Welcome to the DevContainer Node API' });
});

app.get('/health', async (_req: Request, res: Response) => {
    try {
        const result = await pool.query('SELECT NOW()');
        res.json({
            status: 'healthy',
            timestamp: result.rows[0].now,
        });
    } catch (error) {
        res.status(503).json({ status: 'unhealthy', error: String(error) });
    }
});

app.get('/users', async (_req: Request, res: Response) => {
    try {
        const result = await pool.query('SELECT id, name, email FROM users ORDER BY id');
        res.json(result.rows);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch users' });
    }
});

app.post('/users', async (req: Request, res: Response) => {
    const { name, email } = req.body;
    try {
        const result = await pool.query(
            'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
            [name, email]
        );
        res.status(201).json(result.rows[0]);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create user' });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # --- package.json ---
    package_json = {
        "name": "devcontainer-node",
        "version": "1.0.0",
        "description": "Node.js Express API with PostgreSQL",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "lint": "eslint src/**/*.ts",
            "format": "prettier --write src/**/*.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/pg": "^8.10.9",
            "@types/node": "^20.10.0",
            "ts-node": "^10.9.2",
            "eslint": "^8.56.0",
            "@typescript-eslint/eslint-plugin": "^6.19.0",
            "@typescript-eslint/parser": "^6.19.0",
            "prettier": "^3.2.4"
        },
        "author": "Sarah Chen",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
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
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: src/index.ts, package.json, tsconfig.json')
    print(f'No .devcontainer directory exists (as expected)')

    # Install Dev Containers extension
    subprocess.run(['code', '--install-extension', 'ms-vscode-remote.remote-containers'],
                   capture_output=True, text=True)
    print('Dev Containers extension installed')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
