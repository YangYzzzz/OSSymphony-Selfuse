"""
Initial Setup: Multi-stage Docker build debug workflow for Node TypeScript API
Task ID: vscode_gf3_032
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_032'
PROJECT_DIR = f'{WORKDIR}/projects/node-api'


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
    os.makedirs(f'{PROJECT_DIR}/dist', exist_ok=True)

    # package.json - realistic Node.js TypeScript API project
    package_json = {
        "name": "node-api",
        "version": "1.0.0",
        "description": "TypeScript REST API for inventory management",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node-dev --respawn src/index.ts",
            "lint": "eslint src/**/*.ts",
            "test": "jest --passWithNoTests"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0",
            "uuid": "^9.0.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/cors": "^2.8.17",
            "@types/morgan": "^1.9.9",
            "@types/uuid": "^9.0.7",
            "ts-node-dev": "^2.0.0",
            "eslint": "^8.56.0",
            "@typescript-eslint/parser": "^6.19.0",
            "@typescript-eslint/eslint-plugin": "^6.19.0",
            "jest": "^29.7.0",
            "@types/jest": "^29.5.11"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
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

    # src/index.ts - main entry point
    index_ts = '''import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { router as inventoryRouter } from './routes';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Routes
app.use('/api/inventory', inventoryRouter);

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handler
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(`[ERROR] ${err.message}`);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Inventory API running on port ${PORT}`);
});

export default app;
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # src/routes.ts - API routes
    routes_ts = '''import { Router, Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';

export const router = Router();

interface InventoryItem {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unitPrice: number;
  warehouse: string;
  lastUpdated: string;
}

const inventory: InventoryItem[] = [
  {
    id: uuidv4(),
    name: 'Industrial Bearings SKF-6205',
    category: 'Components',
    quantity: 2500,
    unitPrice: 12.75,
    warehouse: 'Seattle-W1',
    lastUpdated: '2025-03-15T08:30:00Z',
  },
  {
    id: uuidv4(),
    name: 'Hydraulic Cylinder HC-200',
    category: 'Actuators',
    quantity: 180,
    unitPrice: 345.00,
    warehouse: 'Portland-W3',
    lastUpdated: '2025-03-14T14:20:00Z',
  },
];

// GET all items
router.get('/', (_req: Request, res: Response) => {
  res.json(inventory);
});

// GET item by ID
router.get('/:id', (req: Request, res: Response) => {
  const item = inventory.find((i) => i.id === req.params.id);
  if (!item) {
    return res.status(404).json({ error: 'Item not found' });
  }
  res.json(item);
});

// POST new item
router.post('/', (req: Request, res: Response) => {
  const newItem: InventoryItem = {
    id: uuidv4(),
    ...req.body,
    lastUpdated: new Date().toISOString(),
  };
  inventory.push(newItem);
  res.status(201).json(newItem);
});

// PUT update item
router.put('/:id', (req: Request, res: Response) => {
  const index = inventory.findIndex((i) => i.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Item not found' });
  }
  inventory[index] = { ...inventory[index], ...req.body, lastUpdated: new Date().toISOString() };
  res.json(inventory[index]);
});

// DELETE item
router.delete('/:id', (req: Request, res: Response) => {
  const index = inventory.findIndex((i) => i.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Item not found' });
  }
  const removed = inventory.splice(index, 1);
  res.json(removed[0]);
});
'''
    with open(f'{PROJECT_DIR}/src/routes.ts', 'w') as f:
        f.write(routes_ts)

    # src/types.ts - shared types
    types_ts = '''export interface InventoryItem {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unitPrice: number;
  warehouse: string;
  lastUpdated: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}

export type InventoryCategory =
  | 'Components'
  | 'Actuators'
  | 'Sensors'
  | 'Fasteners'
  | 'Electrical'
  | 'Raw Materials';
'''
    with open(f'{PROJECT_DIR}/src/types.ts', 'w') as f:
        f.write(types_ts)

    # .env file
    env_content = '''PORT=3000
NODE_ENV=development
LOG_LEVEL=debug
'''
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # .gitignore
    gitignore = '''node_modules/
dist/
.env
*.log
coverage/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # NOTE: No Dockerfile - that is the task for the agent to create!

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: package.json, tsconfig.json, src/index.ts, src/routes.ts, src/types.ts, .env, .gitignore')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
