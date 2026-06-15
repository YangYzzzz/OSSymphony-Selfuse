"""
Initial Setup: Install Prettier extension and set as default formatter
Task ID: vscode_we_052
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_052'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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

    # Create package.json
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "A simple web application for managing customer orders",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.2"
        },
        "author": "Sarah Chen",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src/index.js
    index_js = '''const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const orders = [
    { id: 1, customer: 'Marcus Johnson', product: 'Laptop Pro 15', quantity: 2, total: 2499.98, status: 'shipped' },
    { id: 2, customer: 'Elena Rodriguez', product: 'Wireless Mouse', quantity: 5, total: 149.95, status: 'pending' },
    { id: 3, customer: 'Aisha Patel', product: 'USB-C Hub', quantity: 3, total: 89.97, status: 'delivered' },
    { id: 4, customer: 'James O\\'Brien', product: 'Mechanical Keyboard', quantity: 1, total: 129.99, status: 'processing' },
    { id: 5, customer: 'Lin Wei', product: '27-inch Monitor', quantity: 2, total: 879.98, status: 'shipped' },
];

app.get('/api/orders', (req, res) => {
    res.json({ success: true, data: orders });
});

app.get('/api/orders/:id', (req, res) => {
    const order = orders.find(o => o.id === parseInt(req.params.id));
    if (!order) {
        return res.status(404).json({ success: false, message: 'Order not found' });
    }
    res.json({ success: true, data: order });
});

app.post('/api/orders', (req, res) => {
    const { customer, product, quantity, total } = req.body;
    const newOrder = {
        id: orders.length + 1,
        customer,
        product,
        quantity,
        total,
        status: 'pending'
    };
    orders.push(newOrder);
    res.status(201).json({ success: true, data: newOrder });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # Create src/utils.js
    utils_js = '''function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function generateOrderId() {
    return 'ORD-' + Date.now().toString(36).toUpperCase();
}

function validateEmail(email) {
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}

module.exports = { formatCurrency, generateOrderId, validateEmail };
'''
    with open(f'{PROJECT_DIR}/src/utils.js', 'w') as f:
        f.write(utils_js)

    # Create .env
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write('PORT=3000\nNODE_ENV=development\nDB_HOST=localhost\n')

    # Create .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('node_modules/\n.env\ndist/\ncoverage/\n')

    # Ensure NO .vscode/settings.json exists (task requires creating it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    settings_path = f'{vscode_dir}/settings.json'
    if os.path.exists(settings_path):
        os.remove(settings_path)

    # Ensure Prettier extension is NOT installed
    subprocess.run(['code', '--uninstall-extension', 'esbenp.prettier-vscode'],
                   capture_output=True, text=True)

    print(f'Initial project created: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
