"""
Initial Setup: VSCode git repository initialization task
Task ID: vscode_wf_016
Domain: vscode (os/git)

Creates ~/project with package.json, src/index.js, node_modules/, and .env.
Git is NOT initialized. No .gitignore exists.
Opens VSCode with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
SRC_DIR = os.path.join(PROJECT, 'src')
NODE_MODULES = os.path.join(PROJECT, 'node_modules')
NODE_EXPRESS = os.path.join(NODE_MODULES, 'express')


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
    # Clean up any previous state
    if os.path.exists(PROJECT):
        import shutil
        shutil.rmtree(PROJECT)

    # Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(NODE_EXPRESS, exist_ok=True)

    # package.json - realistic Node.js project
    package_json = {
        "name": "inventory-tracker",
        "version": "1.0.0",
        "description": "A lightweight inventory tracking service for warehouse management",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "build": "webpack --mode production"
        },
        "dependencies": {
            "express": "^4.18.2",
            "dotenv": "^16.3.1",
            "mongoose": "^7.6.3",
            "cors": "^2.8.5"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.7.0",
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4"
        },
        "author": "Sarah Chen <sarah.chen@inventorytracker.io>",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js - realistic Express server
    index_js = '''\
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// In-memory inventory store (replace with MongoDB in production)
let inventory = [
  { id: 1, name: 'Widget A', quantity: 150, warehouse: 'W-East', lastUpdated: '2025-11-01' },
  { id: 2, name: 'Gadget B', quantity: 42, warehouse: 'W-West', lastUpdated: '2025-10-28' },
  { id: 3, name: 'Component C', quantity: 320, warehouse: 'W-East', lastUpdated: '2025-11-03' },
];

app.get('/api/inventory', (req, res) => {
  res.json(inventory);
});

app.get('/api/inventory/:id', (req, res) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: 'Item not found' });
  res.json(item);
});

app.post('/api/inventory', (req, res) => {
  const { name, quantity, warehouse } = req.body;
  const newItem = {
    id: inventory.length + 1,
    name,
    quantity,
    warehouse,
    lastUpdated: new Date().toISOString().split('T')[0],
  };
  inventory.push(newItem);
  res.status(201).json(newItem);
});

app.listen(PORT, () => {
  console.log(`Inventory Tracker API running on port ${PORT}`);
});
'''
    with open(os.path.join(SRC_DIR, 'index.js'), 'w') as f:
        f.write(index_js)

    # .env - realistic environment variables (secrets that should NOT be committed)
    env_content = '''\
PORT=3000
MONGODB_URI=mongodb+srv://admin:s3cretPa55w0rd@cluster0.abc123.mongodb.net/inventory
JWT_SECRET=a7f2e9c4b1d8f3a6e5c2b9d4f7a1e8c3
API_KEY=sk-inv-prod-8f2a4c6e1b3d5f7a9c2e4b6d8f1a3c5e
NODE_ENV=development
'''
    with open(os.path.join(PROJECT, '.env'), 'w') as f:
        f.write(env_content)

    # node_modules/ - simulate installed packages with minimal structure
    # express package
    express_pkg = {
        "name": "express",
        "version": "4.18.2",
        "description": "Fast, unopinionated, minimalist web framework",
        "main": "index.js"
    }
    with open(os.path.join(NODE_EXPRESS, 'package.json'), 'w') as f:
        json.dump(express_pkg, f, indent=2)

    with open(os.path.join(NODE_EXPRESS, 'index.js'), 'w') as f:
        f.write("module.exports = require('./lib/express');\n")

    os.makedirs(os.path.join(NODE_EXPRESS, 'lib'), exist_ok=True)
    with open(os.path.join(NODE_EXPRESS, 'lib', 'express.js'), 'w') as f:
        f.write("// Express framework placeholder\nmodule.exports = function() {};\n")

    # dotenv package
    dotenv_dir = os.path.join(NODE_MODULES, 'dotenv')
    os.makedirs(dotenv_dir, exist_ok=True)
    with open(os.path.join(dotenv_dir, 'package.json'), 'w') as f:
        json.dump({"name": "dotenv", "version": "16.3.1", "main": "lib/main.js"}, f, indent=2)

    print(f'Initial project created at: {PROJECT}')
    print(f'  - package.json')
    print(f'  - src/index.js')
    print(f'  - node_modules/ (express, dotenv)')
    print(f'  - .env')

    # Verify no .git directory exists
    git_dir = os.path.join(PROJECT, '.git')
    assert not os.path.exists(git_dir), f'.git should NOT exist in initial state!'
    print('Verified: no .git directory exists')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
