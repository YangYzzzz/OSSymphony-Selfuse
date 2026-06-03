"""
Initial Setup: Install Prettier extension and configure as default JS formatter with format-on-save
Task ID: vscode_wf_006
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_006'
PROJECT_DIR = f'{WORKDIR}/project'
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


def create_js_files():
    """Create realistic JavaScript project files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-tracker",
        "version": "1.2.0",
        "description": "Warehouse inventory tracking system",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)

    # src/index.js
    index_js = '''const express = require('express');
const { connectDB } = require('./database');
const inventoryRouter = require('./routes/inventory');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/inventory', inventoryRouter);

app.get('/health', (req, res) => {
    res.json({ status: 'ok', uptime: process.uptime() });
});

async function startServer() {
    await connectDB();
    app.listen(PORT, () => {
        console.log(`Inventory Tracker running on port ${PORT}`);
    });
}

startServer().catch(err => {
    console.error('Failed to start server:', err);
    process.exit(1);
});
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # src/database.js
    database_js = '''const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/inventory';

async function connectDB() {
    try {
        await mongoose.connect(MONGO_URI);
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB connection failed:', error.message);
        throw error;
    }
}

module.exports = { connectDB };
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'database.js'), 'w') as f:
        f.write(database_js)

    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'routes'), exist_ok=True)

    # src/routes/inventory.js
    inventory_js = '''const express = require('express');
const router = express.Router();

let items = [
    { id: 1, name: 'Widget A', quantity: 150, warehouse: 'North', lastUpdated: '2025-11-03' },
    { id: 2, name: 'Gadget B', quantity: 87, warehouse: 'South', lastUpdated: '2025-11-01' },
    { id: 3, name: 'Component C', quantity: 320, warehouse: 'North', lastUpdated: '2025-10-28' },
];

router.get('/', (req, res) => {
    const { warehouse } = req.query;
    if (warehouse) {
        return res.json(items.filter(item => item.warehouse === warehouse));
    }
    res.json(items);
});

router.post('/', (req, res) => {
    const { name, quantity, warehouse } = req.body;
    if (!name || quantity == null || !warehouse) {
        return res.status(400).json({ error: 'Missing required fields: name, quantity, warehouse' });
    }
    const newItem = {
        id: items.length + 1,
        name,
        quantity,
        warehouse,
        lastUpdated: new Date().toISOString().split('T')[0]
    };
    items.push(newItem);
    res.status(201).json(newItem);
});

router.put('/:id', (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id));
    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }
    Object.assign(item, req.body, { lastUpdated: new Date().toISOString().split('T')[0] });
    res.json(item);
});

module.exports = router;
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'routes', 'inventory.js'), 'w') as f:
        f.write(inventory_js)

    # src/utils.js
    utils_js = '''function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function calculateReorderPoint(avgDailySales, leadTimeDays, safetyStock) {
    return (avgDailySales * leadTimeDays) + safetyStock;
}

function generateSKU(category, sequenceNum) {
    const prefix = category.substring(0, 3).toUpperCase();
    const num = String(sequenceNum).padStart(5, '0');
    return `${prefix}-${num}`;
}

module.exports = { formatCurrency, calculateReorderPoint, generateSKU };
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'utils.js'), 'w') as f:
        f.write(utils_js)

    print(f'Created JS project files in {PROJECT_DIR}')


def setup_empty_settings():
    """Ensure VSCode settings.json is empty."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Created empty settings.json at {SETTINGS_PATH}')


def ensure_prettier_not_installed():
    """Make sure Prettier extension is not installed."""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=15
        )
        if 'esbenp.prettier-vscode' in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', 'esbenp.prettier-vscode'],
                capture_output=True, text=True, timeout=30
            )
            print('Uninstalled existing Prettier extension')
        else:
            print('Prettier extension not installed (as expected)')
    except Exception as e:
        print(f'Extension check warning: {e}')


def main():
    create_js_files()
    setup_empty_settings()
    ensure_prettier_not_installed()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
