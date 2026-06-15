"""
Initial Setup: Create a Node.js TypeScript project structure with .vscode directory
Task ID: vscode_gf2_018
Domain: vscode

Creates /home/user/projects/node-server with realistic project files.
The .vscode directory exists but does NOT contain tasks.json (agent must create it).
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_018'
PROJECT_DIR = f'{WORKDIR}/projects/node-server'

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
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.package-lock.json', exist_ok=True)

    # package.json
    package_json = {
        "name": "node-server",
        "version": "1.0.0",
        "description": "REST API server for inventory management",
        "main": "dist/index.js",
        "scripts": {
            "build": "npx tsc",
            "start": "node dist/index.js",
            "test": "npx jest",
            "dev": "ts-node src/index.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/cors": "^2.8.17",
            "@types/node": "^20.11.5",
            "jest": "^29.7.0",
            "@types/jest": "^29.5.11",
            "ts-jest": "^29.1.1"
        },
        "author": "Elena Vasquez",
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
        "exclude": ["node_modules", "dist", "tests"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # src/index.ts
    index_ts = '''import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

interface InventoryItem {
  id: number;
  name: string;
  quantity: number;
  price: number;
  category: string;
}

const inventory: InventoryItem[] = [
  { id: 1, name: "Wireless Mouse", quantity: 150, price: 29.99, category: "Electronics" },
  { id: 2, name: "Mechanical Keyboard", quantity: 85, price: 89.99, category: "Electronics" },
  { id: 3, name: "USB-C Hub", quantity: 200, price: 45.00, category: "Accessories" },
  { id: 4, name: "Monitor Stand", quantity: 60, price: 35.50, category: "Furniture" },
  { id: 5, name: "Desk Lamp", quantity: 120, price: 22.75, category: "Furniture" },
];

app.get('/api/inventory', (req, res) => {
  res.json(inventory);
});

app.get('/api/inventory/:id', (req, res) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) {
    return res.status(404).json({ error: 'Item not found' });
  }
  res.json(item);
});

app.post('/api/inventory', (req, res) => {
  const newItem: InventoryItem = {
    id: inventory.length + 1,
    ...req.body
  };
  inventory.push(newItem);
  res.status(201).json(newItem);
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # src/utils.ts
    utils_ts = '''export function formatCurrency(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

export function validateInventoryItem(item: any): boolean {
  return (
    typeof item.name === 'string' &&
    typeof item.quantity === 'number' &&
    typeof item.price === 'number' &&
    item.quantity >= 0 &&
    item.price >= 0
  );
}
'''
    with open(f'{PROJECT_DIR}/src/utils.ts', 'w') as f:
        f.write(utils_ts)

    # dist/index.js (compiled output)
    index_js = '''"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(express.json());
const inventory = [
    { id: 1, name: "Wireless Mouse", quantity: 150, price: 29.99, category: "Electronics" },
    { id: 2, name: "Mechanical Keyboard", quantity: 85, price: 89.99, category: "Electronics" },
    { id: 3, name: "USB-C Hub", quantity: 200, price: 45.00, category: "Accessories" },
    { id: 4, name: "Monitor Stand", quantity: 60, price: 35.50, category: "Furniture" },
    { id: 5, name: "Desk Lamp", quantity: 120, price: 22.75, category: "Furniture" },
];
app.get('/api/inventory', (req, res) => {
    res.json(inventory);
});
app.get('/api/inventory/:id', (req, res) => {
    const item = inventory.find(i => i.id === parseInt(req.params.id));
    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }
    res.json(item);
});
app.post('/api/inventory', (req, res) => {
    const newItem = Object.assign({ id: inventory.length + 1 }, req.body);
    inventory.push(newItem);
    res.status(201).json(newItem);
});
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
exports.default = app;
'''
    with open(f'{PROJECT_DIR}/dist/index.js', 'w') as f:
        f.write(index_js)

    # tests/inventory.test.ts
    test_ts = '''import { formatCurrency, generateId, validateInventoryItem } from '../src/utils';

describe('Utility Functions', () => {
  test('formatCurrency formats numbers correctly', () => {
    expect(formatCurrency(29.99)).toBe('$29.99');
    expect(formatCurrency(100)).toBe('$100.00');
    expect(formatCurrency(0.5)).toBe('$0.50');
  });

  test('generateId returns a string', () => {
    const id = generateId();
    expect(typeof id).toBe('string');
    expect(id.length).toBeGreaterThan(0);
  });

  test('validateInventoryItem accepts valid items', () => {
    expect(validateInventoryItem({
      name: 'Test Item',
      quantity: 10,
      price: 25.00
    })).toBe(true);
  });

  test('validateInventoryItem rejects invalid items', () => {
    expect(validateInventoryItem({
      name: 123,
      quantity: 'bad',
      price: -5
    })).toBe(false);
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/inventory.test.ts', 'w') as f:
        f.write(test_ts)

    # .env file
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write('PORT=3000\nNODE_ENV=development\n')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('node_modules/\ndist/\n.env\n*.js.map\n')

    # .vscode/settings.json (workspace settings - .vscode exists but no tasks.json)
    vscode_settings = {
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # README.md
    readme = '''# Node Server - Inventory Management API

A lightweight REST API server built with Express and TypeScript for managing product inventory.

## Getting Started

```bash
# Install dependencies
npm install

# Build TypeScript
npx tsc

# Run tests
npx jest

# Start the server
node dist/index.js
```

## API Endpoints

- `GET /api/inventory` - List all items
- `GET /api/inventory/:id` - Get item by ID
- `POST /api/inventory` - Add new item

## Development

Author: Elena Vasquez
License: MIT
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'.vscode directory exists: {os.path.isdir(f"{PROJECT_DIR}/.vscode")}')
    print(f'tasks.json does NOT exist: {not os.path.exists(f"{PROJECT_DIR}/.vscode/tasks.json")}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
