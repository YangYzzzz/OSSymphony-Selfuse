"""
Initial Setup: Create a TypeScript Express project without launch.json
Task ID: vscode_web_021
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_021'
PROJECT_DIR = f'{WORKDIR}/projects/api-server'


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
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.package-lock.json', exist_ok=True)

    # package.json
    package_json = {
        "name": "api-server",
        "version": "1.0.0",
        "description": "TypeScript Express API Server for inventory management",
        "main": "dist/server.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/server.js",
            "dev": "ts-node src/server.ts",
            "lint": "eslint src/**/*.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "ts-node": "^10.9.2",
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.11.5",
            "@types/cors": "^2.8.17",
            "@types/morgan": "^1.9.9",
            "eslint": "^8.56.0",
            "@typescript-eslint/parser": "^6.19.0",
            "@typescript-eslint/eslint-plugin": "^6.19.0"
        },
        "author": "DevOps Team",
        "license": "MIT"
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

    # src/server.ts - the main Express server file
    server_ts = '''import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// In-memory inventory store
interface InventoryItem {
  id: number;
  name: string;
  quantity: number;
  price: number;
  category: string;
}

let inventory: InventoryItem[] = [
  { id: 1, name: 'Wireless Mouse', quantity: 150, price: 29.99, category: 'Electronics' },
  { id: 2, name: 'USB-C Hub', quantity: 75, price: 49.99, category: 'Electronics' },
  { id: 3, name: 'Standing Desk Mat', quantity: 200, price: 34.95, category: 'Office' },
  { id: 4, name: 'Mechanical Keyboard', quantity: 60, price: 89.99, category: 'Electronics' },
  { id: 5, name: 'Monitor Arm', quantity: 45, price: 119.00, category: 'Office' },
];

let nextId = 6;

// Routes
app.get('/api/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/inventory', (_req: Request, res: Response) => {
  res.json(inventory);
});

app.get('/api/inventory/:id', (req: Request, res: Response) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) {
    return res.status(404).json({ error: 'Item not found' });
  }
  res.json(item);
});

app.post('/api/inventory', (req: Request, res: Response) => {
  const { name, quantity, price, category } = req.body;
  if (!name || quantity === undefined || price === undefined || !category) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  const newItem: InventoryItem = { id: nextId++, name, quantity, price, category };
  inventory.push(newItem);
  res.status(201).json(newItem);
});

app.put('/api/inventory/:id', (req: Request, res: Response) => {
  const index = inventory.findIndex(i => i.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'Item not found' });
  }
  inventory[index] = { ...inventory[index], ...req.body };
  res.json(inventory[index]);
});

app.delete('/api/inventory/:id', (req: Request, res: Response) => {
  const index = inventory.findIndex(i => i.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'Item not found' });
  }
  const deleted = inventory.splice(index, 1);
  res.json(deleted[0]);
});

// Error handling middleware
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error('Unhandled error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
});

export default app;
'''
    with open(f'{PROJECT_DIR}/src/server.ts', 'w') as f:
        f.write(server_ts)

    # src/types.ts - additional TypeScript file for realism
    types_ts = '''export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}

export interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}

export interface InventoryFilter {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  inStock?: boolean;
}
'''
    with open(f'{PROJECT_DIR}/src/types.ts', 'w') as f:
        f.write(types_ts)

    # .gitignore
    gitignore = '''node_modules/
dist/
*.js.map
.env
.env.local
coverage/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # README.md
    readme = '''# API Server

TypeScript Express API server for inventory management.

## Getting Started

```bash
npm install
npm run dev
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/inventory` - List all items
- `GET /api/inventory/:id` - Get item by ID
- `POST /api/inventory` - Create new item
- `PUT /api/inventory/:id` - Update item
- `DELETE /api/inventory/:id` - Delete item
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # .vscode/settings.json (workspace settings, but NO launch.json)
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "typescript.preferences.importModuleSpecifier": "relative"
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # Ensure NO launch.json exists
    launch_path = f'{PROJECT_DIR}/.vscode/launch.json'
    if os.path.exists(launch_path):
        os.remove(launch_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: package.json, tsconfig.json, src/server.ts, src/types.ts')
    print(f'No .vscode/launch.json exists (task requires creating one)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
