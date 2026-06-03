"""
Initial Setup: Create monorepo project with API and worker services for debugging
Task ID: vscode_gf2_020
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_020'
PROJECT_DIR = f'{WORKDIR}/projects/monorepo'
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
    os.makedirs(f'{PROJECT_DIR}/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/worker', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- Root package.json ---
    root_package = {
        "name": "acme-monorepo",
        "version": "2.1.0",
        "private": True,
        "description": "ACME Corp monorepo - API service and background worker",
        "workspaces": ["api", "worker"],
        "scripts": {
            "dev:api": "cd api && node --inspect=9229 index.js",
            "dev:worker": "cd worker && node index.js",
            "dev": "concurrently \"npm:dev:api\" \"npm:dev:worker\"",
            "test": "jest --coverage",
            "lint": "eslint ."
        },
        "devDependencies": {
            "concurrently": "^8.2.0",
            "eslint": "^8.56.0",
            "jest": "^29.7.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(root_package, f, indent=2)

    # --- API service ---
    api_package = {
        "name": "@acme/api",
        "version": "2.1.0",
        "description": "REST API service for order management",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "dev": "nodemon --inspect=9229 index.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "cors": "^2.8.5",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        }
    }
    with open(f'{PROJECT_DIR}/api/package.json', 'w') as f:
        json.dump(api_package, f, indent=2)

    api_index = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(express.json());

// In-memory store for demo
const orders = [
  { id: 'ORD-1001', customer: 'Priya Sharma', total: 249.99, status: 'shipped' },
  { id: 'ORD-1002', customer: 'James Liu', total: 89.50, status: 'processing' },
  { id: 'ORD-1003', customer: 'Elena Rodriguez', total: 534.00, status: 'pending' },
];

app.get('/api/orders', (req, res) => {
  res.json({ data: orders, count: orders.length });
});

app.get('/api/orders/:id', (req, res) => {
  const order = orders.find(o => o.id === req.params.id);
  if (!order) return res.status(404).json({ error: 'Order not found' });
  res.json(order);
});

app.post('/api/orders', (req, res) => {
  const { customer, total } = req.body;
  const newOrder = {
    id: `ORD-${1000 + orders.length + 1}`,
    customer,
    total,
    status: 'pending',
  };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});

app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/api/index.js', 'w') as f:
        f.write(api_index)

    # --- Worker service ---
    worker_package = {
        "name": "@acme/worker",
        "version": "2.1.0",
        "description": "Background job processor for order fulfillment",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "test": "jest"
        },
        "dependencies": {
            "bull": "^4.12.0",
            "ioredis": "^5.3.2"
        }
    }
    with open(f'{PROJECT_DIR}/worker/package.json', 'w') as f:
        json.dump(worker_package, f, indent=2)

    worker_index = '''const Bull = require('bull');

const REDIS_URL = process.env.REDIS_URL || 'redis://127.0.0.1:6379';
const QUEUE_NAME = 'order-fulfillment';

console.log(`Worker starting — connecting to ${REDIS_URL}`);

const fulfillmentQueue = new Bull(QUEUE_NAME, REDIS_URL);

fulfillmentQueue.process(async (job) => {
  const { orderId, customer, total } = job.data;
  console.log(`Processing order ${orderId} for ${customer} ($${total})`);

  // Simulate fulfillment steps
  await delay(500);
  console.log(`  -> Inventory reserved for ${orderId}`);

  await delay(300);
  console.log(`  -> Payment captured for ${orderId}`);

  await delay(200);
  console.log(`  -> Shipping label generated for ${orderId}`);

  return { orderId, status: 'fulfilled' };
});

fulfillmentQueue.on('completed', (job, result) => {
  console.log(`Order ${result.orderId} fulfilled successfully`);
});

fulfillmentQueue.on('failed', (job, err) => {
  console.error(`Order ${job.data.orderId} failed: ${err.message}`);
});

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

console.log(`Worker ready — listening on queue "${QUEUE_NAME}"`);
'''
    with open(f'{PROJECT_DIR}/worker/index.js', 'w') as f:
        f.write(worker_index)

    # --- .gitignore ---
    gitignore = '''node_modules/
dist/
.env
*.log
coverage/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README ---
    readme = '''# ACME Monorepo

Order management system with REST API and background worker.

## Services

- **api/** - Express REST API for order CRUD (port 3000)
- **worker/** - Bull queue processor for order fulfillment

## Development

```bash
npm install
npm run dev        # starts both API and worker
npm run dev:api    # API only with --inspect on port 9229
npm run dev:worker # worker only
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # NOTE: Do NOT create .vscode/launch.json — that's the task!
    # .vscode directory exists but is empty (or has no launch.json)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'.vscode directory exists: {os.path.isdir(VSCODE_DIR)}')
    print(f'launch.json exists: {os.path.isfile(f"{VSCODE_DIR}/launch.json")}')

    # GUI-ready: open VSCode with the monorepo folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
