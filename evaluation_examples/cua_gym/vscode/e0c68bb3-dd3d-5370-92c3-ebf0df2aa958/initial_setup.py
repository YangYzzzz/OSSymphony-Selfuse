"""
Initial Setup: Create a Docker + Node.js project with no launch.json
Task ID: vscode_td_084
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_084'
PROJECT_DIR = f'{WORKDIR}/projects/dockerized-node'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Ensure NO .vscode/launch.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(f'{vscode_dir}/launch.json'):
        os.remove(f'{vscode_dir}/launch.json')

    # --- docker-compose.yml ---
    docker_compose = """\
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
      - "9229:9229"
    volumes:
      - ./src:/app/src
      - ./package.json:/app/package.json
    command: node --inspect=0.0.0.0:9229 src/server.js
    environment:
      - NODE_ENV=development
      - PORT=3000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
"""
    with open(f'{PROJECT_DIR}/docker-compose.yml', 'w') as f:
        f.write(docker_compose)

    # --- Dockerfile ---
    dockerfile = """\
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 3000 9229

CMD ["node", "--inspect=0.0.0.0:9229", "src/server.js"]
"""
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write(dockerfile)

    # --- package.json ---
    package_json = {
        "name": "dockerized-node",
        "version": "1.2.0",
        "description": "Inventory management API for warehouse operations",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "debug": "node --inspect=0.0.0.0:9229 src/server.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "winston": "^3.11.0",
            "helmet": "^7.1.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.7.0",
            "eslint": "^8.53.0"
        },
        "author": "Elena Vasquez",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/server.js ---
    server_js = """\
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');

const app = express();
const PORT = process.env.PORT || 3000;

// Logger setup
const logger = winston.createLogger({
  level: 'info',
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

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// In-memory inventory store
let inventory = [
  { id: 1, sku: 'WH-4521', name: 'Industrial Bearing Assembly', quantity: 340, location: 'A-14-03', lastUpdated: '2025-11-20' },
  { id: 2, sku: 'WH-7833', name: 'Hydraulic Pump Filter', quantity: 125, location: 'B-07-11', lastUpdated: '2025-12-01' },
  { id: 3, sku: 'WH-2190', name: 'Steel Mounting Bracket', quantity: 890, location: 'C-22-05', lastUpdated: '2025-11-28' },
  { id: 4, sku: 'WH-6047', name: 'Pneumatic Valve Set', quantity: 56, location: 'A-03-09', lastUpdated: '2025-12-03' },
  { id: 5, sku: 'WH-1384', name: 'Copper Wire Spool 14AWG', quantity: 210, location: 'D-11-02', lastUpdated: '2025-11-15' },
];

// Routes
app.get('/api/inventory', (req, res) => {
  logger.info('GET /api/inventory');
  res.json({ success: true, data: inventory, count: inventory.length });
});

app.get('/api/inventory/:id', (req, res) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) {
    return res.status(404).json({ success: false, error: 'Item not found' });
  }
  res.json({ success: true, data: item });
});

app.post('/api/inventory', (req, res) => {
  const { sku, name, quantity, location } = req.body;
  const newItem = {
    id: inventory.length + 1,
    sku,
    name,
    quantity,
    location,
    lastUpdated: new Date().toISOString().split('T')[0]
  };
  inventory.push(newItem);
  logger.info(`Created inventory item: ${sku}`);
  res.status(201).json({ success: true, data: newItem });
});

app.put('/api/inventory/:id', (req, res) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) {
    return res.status(404).json({ success: false, error: 'Item not found' });
  }
  Object.assign(item, req.body, { lastUpdated: new Date().toISOString().split('T')[0] });
  logger.info(`Updated inventory item: ${item.sku}`);
  res.json({ success: true, data: item });
});

app.delete('/api/inventory/:id', (req, res) => {
  const index = inventory.findIndex(i => i.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ success: false, error: 'Item not found' });
  }
  const removed = inventory.splice(index, 1);
  logger.info(`Deleted inventory item: ${removed[0].sku}`);
  res.json({ success: true, data: removed[0] });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', uptime: process.uptime() });
});

app.listen(PORT, () => {
  logger.info(`Inventory API running on port ${PORT}`);
});
"""
    with open(f'{PROJECT_DIR}/src/server.js', 'w') as f:
        f.write(server_js)

    # --- .dockerignore ---
    dockerignore = """\
node_modules
npm-debug.log
logs/
.env
.git
.vscode
"""
    with open(f'{PROJECT_DIR}/.dockerignore', 'w') as f:
        f.write(dockerignore)

    # --- .env ---
    dotenv = """\
NODE_ENV=development
PORT=3000
MONGO_URI=mongodb://mongo:27017/inventory
LOG_LEVEL=info
"""
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(dotenv)

    # --- README.md ---
    readme = """\
# Dockerized Node.js Inventory API

A containerized REST API for warehouse inventory management.

## Quick Start

```bash
docker-compose up --build
```

The API will be available at `http://localhost:3000`.

## Debugging

The container exposes port 9229 for Node.js debugging.
Connect your debugger to `localhost:9229`.

## Endpoints

- `GET /api/inventory` - List all items
- `GET /api/inventory/:id` - Get single item
- `POST /api/inventory` - Create item
- `PUT /api/inventory/:id` - Update item
- `DELETE /api/inventory/:id` - Delete item
- `GET /health` - Health check
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Files: docker-compose.yml, Dockerfile, package.json, src/server.js, .dockerignore, .env, README.md')
    print(f'No .vscode/launch.json exists (as required)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
