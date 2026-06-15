"""
Initial Setup: Create a TypeScript project with package.json containing a 'watch' script.
Task ID: vscode_wf_030
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_030'
PROJECT_DIR = f'{WORKDIR}/project'


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

    # Create package.json with a 'watch' script
    package_json = {
        "name": "inventory-tracker",
        "version": "1.2.0",
        "description": "Real-time inventory tracking service for warehouse management",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "watch": "tsc --watch",
            "start": "node dist/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/**/*.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "redis": "^4.6.10",
            "winston": "^3.11.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.6",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "eslint": "^8.56.0",
            "@typescript-eslint/parser": "^6.18.0"
        },
        "author": "Elena Rodriguez",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

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
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Create src/index.ts - main entry point
    index_ts = '''import express from 'express';
import { InventoryService } from './services/inventory';
import { logger } from './utils/logger';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const inventoryService = new InventoryService();

app.get('/api/items', async (req, res) => {
    try {
        const items = await inventoryService.getAllItems();
        res.json({ success: true, data: items });
    } catch (error) {
        logger.error('Failed to fetch items', { error });
        res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

app.get('/api/items/:sku', async (req, res) => {
    try {
        const item = await inventoryService.getItemBySku(req.params.sku);
        if (!item) {
            return res.status(404).json({ success: false, error: 'Item not found' });
        }
        res.json({ success: true, data: item });
    } catch (error) {
        logger.error('Failed to fetch item', { sku: req.params.sku, error });
        res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

app.post('/api/items/:sku/adjust', async (req, res) => {
    const { quantity, reason } = req.body;
    try {
        const updated = await inventoryService.adjustStock(req.params.sku, quantity, reason);
        res.json({ success: true, data: updated });
    } catch (error) {
        logger.error('Stock adjustment failed', { sku: req.params.sku, error });
        res.status(500).json({ success: false, error: 'Adjustment failed' });
    }
});

app.listen(PORT, () => {
    logger.info(`Inventory service running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # Create src/services/inventory.ts
    os.makedirs(f'{PROJECT_DIR}/src/services', exist_ok=True)
    inventory_ts = '''export interface InventoryItem {
    sku: string;
    name: string;
    quantity: number;
    location: string;
    lastUpdated: Date;
}

export class InventoryService {
    private items: Map<string, InventoryItem> = new Map();

    async getAllItems(): Promise<InventoryItem[]> {
        return Array.from(this.items.values());
    }

    async getItemBySku(sku: string): Promise<InventoryItem | undefined> {
        return this.items.get(sku);
    }

    async adjustStock(sku: string, quantity: number, reason: string): Promise<InventoryItem> {
        const item = this.items.get(sku);
        if (!item) {
            throw new Error(`Item ${sku} not found`);
        }
        item.quantity += quantity;
        item.lastUpdated = new Date();
        return item;
    }
}
'''
    with open(f'{PROJECT_DIR}/src/services/inventory.ts', 'w') as f:
        f.write(inventory_ts)

    # Create src/utils/logger.ts
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    logger_ts = '''export const logger = {
    info: (message: string, meta?: Record<string, unknown>) => {
        console.log(JSON.stringify({ level: 'info', message, ...meta, timestamp: new Date().toISOString() }));
    },
    error: (message: string, meta?: Record<string, unknown>) => {
        console.error(JSON.stringify({ level: 'error', message, ...meta, timestamp: new Date().toISOString() }));
    },
    warn: (message: string, meta?: Record<string, unknown>) => {
        console.warn(JSON.stringify({ level: 'warn', message, ...meta, timestamp: new Date().toISOString() }));
    }
};
'''
    with open(f'{PROJECT_DIR}/src/utils/logger.ts', 'w') as f:
        f.write(logger_ts)

    # NOTE: Do NOT create .vscode/tasks.json - that's the task for the agent
    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  package.json with watch script: OK')
    print(f'  tsconfig.json: OK')
    print(f'  src/index.ts: OK')
    print(f'  src/services/inventory.ts: OK')
    print(f'  src/utils/logger.ts: OK')
    print(f'  .vscode/tasks.json: NOT created (agent task)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
