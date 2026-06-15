"""
Initial Setup: Create a TypeScript project with VSCode launch config but no preLaunchTask or tasks.json
Task ID: vscode_web_036
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_036'
PROJECT_DIR = f'{WORKDIR}/projects/ts-server'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "ts-server",
        "version": "1.0.0",
        "description": "TypeScript Express API server for inventory management",
        "main": "dist/server.js",
        "scripts": {
            "start": "node dist/server.js",
            "dev": "ts-node src/server.ts"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.11.5",
            "ts-node": "^10.9.2"
        }
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

    # --- src/server.ts ---
    server_ts = '''\
import express, { Request, Response } from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

interface InventoryItem {
    id: number;
    name: string;
    quantity: number;
    price: number;
    category: string;
}

const inventory: InventoryItem[] = [
    { id: 1, name: "Wireless Keyboard", quantity: 45, price: 79.99, category: "Electronics" },
    { id: 2, name: "USB-C Hub", quantity: 120, price: 34.50, category: "Electronics" },
    { id: 3, name: "Standing Desk Mat", quantity: 30, price: 49.95, category: "Office" },
    { id: 4, name: "Monitor Arm", quantity: 15, price: 129.00, category: "Furniture" },
    { id: 5, name: "Noise Cancelling Headphones", quantity: 60, price: 249.99, category: "Electronics" },
];

app.get('/api/inventory', (req: Request, res: Response) => {
    const { category } = req.query;
    if (category) {
        const filtered = inventory.filter(item =>
            item.category.toLowerCase() === (category as string).toLowerCase()
        );
        return res.json(filtered);
    }
    res.json(inventory);
});

app.get('/api/inventory/:id', (req: Request, res: Response) => {
    const item = inventory.find(i => i.id === parseInt(req.params.id));
    if (!item) {
        return res.status(404).json({ error: "Item not found" });
    }
    res.json(item);
});

app.post('/api/inventory', (req: Request, res: Response) => {
    const { name, quantity, price, category } = req.body;
    if (!name || quantity === undefined || price === undefined || !category) {
        return res.status(400).json({ error: "Missing required fields" });
    }
    const newItem: InventoryItem = {
        id: inventory.length + 1,
        name,
        quantity,
        price,
        category,
    };
    inventory.push(newItem);
    res.status(201).json(newItem);
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/server.ts', 'w') as f:
        f.write(server_ts)

    # --- src/utils.ts ---
    utils_ts = '''\
export function formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

export function calculateTotalValue(items: { quantity: number; price: number }[]): number {
    return items.reduce((total, item) => total + item.quantity * item.price, 0);
}

export function generateReport(items: { name: string; quantity: number; price: number }[]): string {
    const lines = items.map(item =>
        `${item.name}: ${item.quantity} units @ ${formatCurrency(item.price)} = ${formatCurrency(item.quantity * item.price)}`
    );
    const total = calculateTotalValue(items);
    lines.push(`\\nTotal Inventory Value: ${formatCurrency(total)}`);
    return lines.join('\\n');
}
'''
    with open(f'{PROJECT_DIR}/src/utils.ts', 'w') as f:
        f.write(utils_ts)

    # --- .vscode/launch.json (NO preLaunchTask) ---
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug Server",
                "type": "node",
                "request": "launch",
                "program": "${workspaceFolder}/dist/server.js",
                "outFiles": ["${workspaceFolder}/dist/**/*.js"],
                "sourceMaps": True,
                "console": "integratedTerminal",
                "env": {
                    "PORT": "3000"
                }
            }
        ]
    }
    with open(f'{VSCODE_DIR}/launch.json', 'w') as f:
        json.dump(launch_json, f, indent=4)

    # Ensure NO tasks.json exists
    tasks_path = f'{VSCODE_DIR}/tasks.json'
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json created (no preLaunchTask)')
    print(f'tasks.json does NOT exist')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
