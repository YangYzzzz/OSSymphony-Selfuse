"""
Initial Setup: Create a Node.js project with VSCode open, no tasks.json, empty keybindings.
Task ID: vscode_rrt_075
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_075'
PROJECT_DIR = os.path.join(WORKDIR, 'workspace')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')


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
    # --- Create Node.js project structure ---
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'test'), exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-tracker",
        "version": "1.2.0",
        "description": "A lightweight inventory tracking system for small businesses",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/ test/",
            "build": "babel src -d dist"
        },
        "keywords": ["inventory", "tracking", "business"],
        "author": "Sarah Chen <sarah.chen@inventorytech.com>",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "winston": "^3.11.0"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "eslint": "^8.53.0",
            "@babel/core": "^7.23.3",
            "@babel/cli": "^7.23.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    index_js = '''\
const express = require('express');
const mongoose = require('mongoose');
const { logger } = require('./utils/logger');
const inventoryRoutes = require('./routes/inventory');
const authRoutes = require('./routes/auth');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/inventory', inventoryRoutes);
app.use('/api/auth', authRoutes);

app.get('/health', (req, res) => {
    res.json({ status: 'ok', uptime: process.uptime() });
});

mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/inventory')
    .then(() => {
        logger.info('Connected to MongoDB');
        app.listen(PORT, () => {
            logger.info(`Server running on port ${PORT}`);
        });
    })
    .catch(err => {
        logger.error('Failed to connect to MongoDB', err);
        process.exit(1);
    });

module.exports = app;
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # src/models/item.js
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'models'), exist_ok=True)
    item_model = '''\
const mongoose = require('mongoose');

const itemSchema = new mongoose.Schema({
    name: { type: String, required: true, trim: true },
    sku: { type: String, required: true, unique: true },
    quantity: { type: Number, required: true, min: 0 },
    price: { type: Number, required: true, min: 0 },
    category: { type: String, enum: ['electronics', 'clothing', 'food', 'tools', 'misc'] },
    supplier: { type: String },
    lastRestocked: { type: Date, default: Date.now },
}, { timestamps: true });

itemSchema.methods.isLowStock = function(threshold = 10) {
    return this.quantity < threshold;
};

module.exports = mongoose.model('Item', itemSchema);
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models', 'item.js'), 'w') as f:
        f.write(item_model)

    # test/item.test.js
    test_js = '''\
const Item = require('../src/models/item');

describe('Item Model', () => {
    test('should flag low stock items', () => {
        const item = new Item({
            name: 'USB-C Cable',
            sku: 'ELEC-001',
            quantity: 5,
            price: 12.99,
            category: 'electronics'
        });
        expect(item.isLowStock()).toBe(true);
        expect(item.isLowStock(3)).toBe(false);
    });

    test('should require name and sku', () => {
        const item = new Item({});
        const err = item.validateSync();
        expect(err.errors.name).toBeDefined();
        expect(err.errors.sku).toBeDefined();
    });
});
'''
    with open(os.path.join(PROJECT_DIR, 'test', 'item.test.js'), 'w') as f:
        f.write(test_js)

    # .env file
    env_content = '''\
PORT=3000
MONGO_URI=mongodb://localhost:27017/inventory_dev
LOG_LEVEL=debug
JWT_SECRET=dev-secret-key-change-in-production
'''
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # Ensure NO .vscode directory exists in the project
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # --- Set up VSCode keybindings as empty ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Keybindings set to empty array at: {KEYBINDINGS_PATH}')

    print(f'Node.js project created at: {PROJECT_DIR}')

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
