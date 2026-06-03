"""
Initial Setup: Rename helper.js to utils.js with import updates
Task ID: vscode_lp_058
Domain: vscode

Creates a JavaScript project with src/helper.js imported by 4 other files.
VSCode is opened with the project folder and updateImportsOnFileMove enabled.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_058'
PROJECT_DIR = os.path.join(WORKDIR, 'src')

# VSCode config paths
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


def create_project():
    """Create the JavaScript project with helper.js and importing files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "inventory-tracker",
        "version": "2.1.0",
        "description": "Warehouse inventory tracking system",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3"
        }
    }
    with open(os.path.join(WORKDIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/helper.js --- (the file to be renamed)
    helper_js = '''/**
 * Helper utilities for the inventory tracking system.
 * Provides date formatting, string manipulation, debounce, and ID generation.
 */

function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function capitalize(str) {
    if (!str || typeof str !== 'string') return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function debounce(fn, delay = 300) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

function generateId(prefix = 'INV') {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    return `${prefix}-${timestamp}-${random}`;
}

module.exports = { formatDate, capitalize, debounce, generateId };
'''
    with open(os.path.join(PROJECT_DIR, 'helper.js'), 'w') as f:
        f.write(helper_js)

    # --- src/app.js --- (imports helper)
    app_js = '''const express = require('express');
const { formatDate, generateId } = require('./helper');
const routes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api', routes);

app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: formatDate(new Date()),
        requestId: generateId('REQ')
    });
});

app.listen(PORT, () => {
    console.log(`Inventory tracker running on port ${PORT}`);
});

module.exports = app;
'''
    with open(os.path.join(PROJECT_DIR, 'app.js'), 'w') as f:
        f.write(app_js)

    # --- src/routes.js --- (imports helper)
    routes_js = '''const express = require('express');
const { capitalize, generateId } = require('./helper');
const router = express.Router();

const inventory = [];

router.post('/items', (req, res) => {
    const { name, category, quantity } = req.body;
    const item = {
        id: generateId('ITEM'),
        name: capitalize(name),
        category: capitalize(category),
        quantity: parseInt(quantity, 10) || 0,
        createdAt: new Date().toISOString()
    };
    inventory.push(item);
    res.status(201).json(item);
});

router.get('/items', (req, res) => {
    res.json(inventory);
});

router.get('/items/:id', (req, res) => {
    const item = inventory.find(i => i.id === req.params.id);
    if (!item) return res.status(404).json({ error: 'Item not found' });
    res.json(item);
});

module.exports = router;
'''
    with open(os.path.join(PROJECT_DIR, 'routes.js'), 'w') as f:
        f.write(routes_js)

    # --- src/middleware.js --- (imports helper)
    middleware_js = '''const { formatDate, debounce } = require('./helper');

const requestLogger = (req, res, next) => {
    const timestamp = formatDate(new Date());
    console.log(`[${timestamp}] ${req.method} ${req.url}`);
    next();
};

const rateLimiter = (() => {
    const requests = new Map();
    const WINDOW_MS = 60000;
    const MAX_REQUESTS = 100;

    return (req, res, next) => {
        const ip = req.ip || req.connection.remoteAddress;
        const now = Date.now();
        const windowStart = now - WINDOW_MS;

        if (!requests.has(ip)) {
            requests.set(ip, []);
        }

        const ipRequests = requests.get(ip).filter(t => t > windowStart);
        ipRequests.push(now);
        requests.set(ip, ipRequests);

        if (ipRequests.length > MAX_REQUESTS) {
            return res.status(429).json({
                error: 'Too many requests',
                retryAfter: Math.ceil(WINDOW_MS / 1000)
            });
        }
        next();
    };
})();

module.exports = { requestLogger, rateLimiter };
'''
    with open(os.path.join(PROJECT_DIR, 'middleware.js'), 'w') as f:
        f.write(middleware_js)

    # --- src/index.js --- (imports helper)
    index_js = '''const { formatDate, capitalize, generateId } = require('./helper');

console.log('=== Inventory Tracker System ===');
console.log(`Started at: ${formatDate(new Date())}`);
console.log(`Session ID: ${generateId('SES')}`);

const categories = ['electronics', 'furniture', 'clothing', 'groceries'];
categories.forEach(cat => {
    console.log(`  Category: ${capitalize(cat)}`);
});

// Re-export for convenience
module.exports = {
    formatDate,
    capitalize,
    generateId
};
'''
    with open(os.path.join(PROJECT_DIR, 'index.js'), 'w') as f:
        f.write(index_js)

    print(f'Project created at {PROJECT_DIR}')
    print(f'Files: helper.js, app.js, routes.js, middleware.js, index.js')


def configure_vscode():
    """Enable updateImportsOnFileMove in VSCode settings."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    settings.update({
        "javascript.updateImportsOnFileMove.enabled": "always",
        "typescript.updateImportsOnFileMove.enabled": "always",
        "editor.fontSize": 14,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured: updateImportsOnFileMove enabled')


def main():
    create_project()
    configure_vscode()

    # Open VSCode with the project folder
    launch_gui(f'code "{WORKDIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
