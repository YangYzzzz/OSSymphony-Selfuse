"""
Initial Setup: Set up environment variable autocompletion in VSCode for a Node.js project
Task ID: vscode_web_074
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_074'
PROJECT_DIR = f'{WORKDIR}/projects/api-server'
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
    os.makedirs(f'{PROJECT_DIR}/node_modules', exist_ok=True)

    # --- .env file ---
    env_content = """DATABASE_URL=postgresql://admin:secretpass@db.internal.company.com:5432/api_production
API_KEY=sk-proj-a8f29c3d4e5b6710f2a9d4c8e1b7f3a2d9c6e4b1
NODE_ENV=development
PORT=3000
"""
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # --- package.json ---
    package_json = {
        "name": "api-server",
        "version": "1.2.0",
        "description": "Production API server for customer management platform",
        "main": "dist/index.js",
        "scripts": {
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "build": "tsc",
            "test": "jest",
            "lint": "eslint src/**/*.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "@types/express": "^4.17.21",
            "ts-node": "^10.9.2",
            "jest": "^29.7.0",
            "@types/jest": "^29.5.11",
            "eslint": "^8.55.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json (NO types directory included) ---
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

    # --- src/index.ts (main entry point using process.env) ---
    index_ts = '''import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import helmet from 'helmet';

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(helmet());
app.use(express.json());

// Database connection string - note: no autocomplete for process.env variables
const dbUrl = process.env.DATABASE_URL;
const apiKey = process.env.API_KEY;
const port = process.env.PORT || 3000;

app.get('/health', (req, res) => {
  res.json({ status: 'ok', environment: process.env.NODE_ENV });
});

app.get('/api/customers', async (req, res) => {
  try {
    // TODO: Implement database query using dbUrl
    res.json({ message: 'Customer list endpoint', db_connected: !!dbUrl });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/customers', async (req, res) => {
  const { name, email, company } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  // TODO: Insert into database
  res.status(201).json({ message: 'Customer created', data: { name, email, company } });
});

app.listen(port, () => {
  console.log(`API Server running on port ${port}`);
  console.log(`Environment: ${process.env.NODE_ENV}`);
});
'''
    with open(f'{SRC_DIR}/index.ts', 'w') as f:
        f.write(index_ts)

    # --- src/config.ts (config helper) ---
    config_ts = '''import dotenv from 'dotenv';

dotenv.config();

export const config = {
  database: {
    url: process.env.DATABASE_URL || '',
    ssl: process.env.NODE_ENV === 'production',
  },
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    env: process.env.NODE_ENV || 'development',
  },
  api: {
    key: process.env.API_KEY || '',
  },
};
'''
    with open(f'{SRC_DIR}/config.ts', 'w') as f:
        f.write(config_ts)

    # --- .gitignore ---
    gitignore = """node_modules/
dist/
.env
*.js.map
coverage/
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: .env, package.json, tsconfig.json, src/index.ts, src/config.ts, .gitignore')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
