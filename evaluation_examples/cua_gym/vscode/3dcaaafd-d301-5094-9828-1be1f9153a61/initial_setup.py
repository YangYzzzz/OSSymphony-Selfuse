"""
Initial Setup: Configure file nesting to group related configuration files under package.json
Task ID: vscode_lp_074
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_074'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project_files():
    """Create a realistic Node.js project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json - realistic Node.js project
    package_json = {
        "name": "inventory-dashboard",
        "version": "2.3.1",
        "description": "Real-time inventory tracking dashboard for warehouse operations",
        "main": "dist/index.js",
        "scripts": {
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "build": "tsc",
            "test": "jest --coverage",
            "lint": "eslint src/ --ext .ts",
            "format": "prettier --write src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "socket.io": "^4.7.2",
            "pg": "^8.11.3",
            "redis": "^4.6.10",
            "winston": "^3.11.0",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "typescript": "^5.3.2",
            "ts-node": "^10.9.2",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "eslint": "^8.54.0",
            "@typescript-eslint/eslint-plugin": "^6.12.0",
            "prettier": "^3.1.0"
        },
        "author": "Elena Vasquez <elena.vasquez@techcorp.io>",
        "license": "MIT",
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # package-lock.json - simplified but realistic structure
    lock_json = {
        "name": "inventory-dashboard",
        "version": "2.3.1",
        "lockfileVersion": 3,
        "requires": True,
        "packages": {
            "": {
                "name": "inventory-dashboard",
                "version": "2.3.1",
                "license": "MIT",
                "dependencies": {
                    "express": "^4.18.2",
                    "socket.io": "^4.7.2",
                    "pg": "^8.11.3"
                }
            },
            "node_modules/express": {
                "version": "4.18.2",
                "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
                "integrity": "sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMg=="
            },
            "node_modules/socket.io": {
                "version": "4.7.2",
                "resolved": "https://registry.npmjs.org/socket.io/-/socket.io-4.7.2.tgz",
                "integrity": "sha512-bvKVS29/I5fl2FGLNHuXlQaUH/BlzX1IN6S+NKLNZpBsPZQ3eJKK2CLwMFuYYEY4dHBg/s2DfFcJKAJJHMYPg=="
            }
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package-lock.json'), 'w') as f:
        json.dump(lock_json, f, indent=2)

    # .npmrc - npm configuration
    npmrc_content = """registry=https://registry.npmjs.org/
save-exact=true
engine-strict=true
auto-install-peers=true
fund=false
audit-level=moderate
"""
    with open(os.path.join(PROJECT_DIR, '.npmrc'), 'w') as f:
        f.write(npmrc_content.lstrip())

    # .nvmrc - Node version specification
    with open(os.path.join(PROJECT_DIR, '.nvmrc'), 'w') as f:
        f.write('18.19.0\n')

    # tsconfig.json - TypeScript configuration
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "commonjs",
            "lib": ["ES2022"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True,
            "baseUrl": ".",
            "paths": {
                "@/*": ["src/*"],
                "@models/*": ["src/models/*"],
                "@services/*": ["src/services/*"]
            }
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Create a basic src directory with a file for realism
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.ts'), 'w') as f:
        f.write('''import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { Pool } from 'pg';
import winston from 'winston';
import dotenv from 'dotenv';

dotenv.config();

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: process.env.CORS_ORIGIN || '*' }
});

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

const PORT = parseInt(process.env.PORT || '3000', 10);

httpServer.listen(PORT, () => {
  logger.info(`Inventory Dashboard server running on port ${PORT}`);
});
''')

    print(f'Project files created in: {PROJECT_DIR}')


def ensure_clean_settings():
    """Ensure VSCode settings exist but do NOT have file nesting configured."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any file nesting settings if they exist
    settings.pop('explorer.fileNesting.enabled', None)
    settings.pop('explorer.fileNesting.patterns', None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print('VSCode settings cleaned (no file nesting)')


def main():
    create_project_files()
    ensure_clean_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
