"""
Initial Setup: Create a Node.js project workspace for debugger attach task
Task ID: vscode_td_050
Domain: vs_code

Creates ~/projects/node-service with realistic Node.js files,
starts a Node.js process with --inspect on port 9229,
and opens VSCode with the project folder.
No .vscode/launch.json exists yet.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_050'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'node-service')


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
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    routes_dir = os.path.join(src_dir, 'routes')
    os.makedirs(routes_dir, exist_ok=True)
    models_dir = os.path.join(src_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    # package.json
    package_json = {
        "name": "node-service",
        "version": "1.2.0",
        "description": "Customer order management microservice",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "node --inspect=9229 src/server.js",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.2"
        },
        "author": "Wei Zhang",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/server.js
    server_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const orderRoutes = require('./routes/orders');
const customerRoutes = require('./routes/customers');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

app.use('/api/orders', orderRoutes);
app.use('/api/customers', customerRoutes);

app.get('/health', (req, res) => {
    res.json({ status: 'ok', uptime: process.uptime() });
});

app.listen(PORT, () => {
    console.log(`Order service listening on port ${PORT}`);
});

module.exports = app;
'''
    with open(os.path.join(src_dir, 'server.js'), 'w') as f:
        f.write(server_js)

    # src/routes/orders.js
    orders_js = '''const express = require('express');
const router = express.Router();

const orders = [
    { id: 1, customer: 'Acme Corp', product: 'Widget Pro', quantity: 150, total: 4500.00, status: 'shipped' },
    { id: 2, customer: 'TechStart Inc', product: 'Gadget X', quantity: 75, total: 2250.00, status: 'processing' },
    { id: 3, customer: 'Global Trade LLC', product: 'Module Alpha', quantity: 300, total: 12000.00, status: 'delivered' },
];

router.get('/', (req, res) => {
    const { status } = req.query;
    if (status) {
        return res.json(orders.filter(o => o.status === status));
    }
    res.json(orders);
});

router.get('/:id', (req, res) => {
    const order = orders.find(o => o.id === parseInt(req.params.id));
    if (!order) return res.status(404).json({ error: 'Order not found' });
    res.json(order);
});

router.post('/', (req, res) => {
    const { customer, product, quantity, total } = req.body;
    const newOrder = { id: orders.length + 1, customer, product, quantity, total, status: 'pending' };
    orders.push(newOrder);
    res.status(201).json(newOrder);
});

module.exports = router;
'''
    with open(os.path.join(routes_dir, 'orders.js'), 'w') as f:
        f.write(orders_js)

    # src/routes/customers.js
    customers_js = '''const express = require('express');
const router = express.Router();

const customers = [
    { id: 1, name: 'Acme Corp', contact: 'sarah.chen@acme.com', tier: 'enterprise' },
    { id: 2, name: 'TechStart Inc', contact: 'marcus.johnson@techstart.io', tier: 'standard' },
    { id: 3, name: 'Global Trade LLC', contact: 'elena.rivera@globaltrade.com', tier: 'enterprise' },
    { id: 4, name: 'DataFlow Systems', contact: 'raj.patel@dataflow.dev', tier: 'premium' },
];

router.get('/', (req, res) => {
    res.json(customers);
});

router.get('/:id', (req, res) => {
    const customer = customers.find(c => c.id === parseInt(req.params.id));
    if (!customer) return res.status(404).json({ error: 'Customer not found' });
    res.json(customer);
});

module.exports = router;
'''
    with open(os.path.join(routes_dir, 'customers.js'), 'w') as f:
        f.write(customers_js)

    # src/models/order.js
    order_model = '''const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
    customer: { type: String, required: true },
    product: { type: String, required: true },
    quantity: { type: Number, required: true, min: 1 },
    total: { type: Number, required: true },
    status: {
        type: String,
        enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
        default: 'pending'
    },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
});

orderSchema.pre('save', function(next) {
    this.updatedAt = Date.now();
    next();
});

module.exports = mongoose.model('Order', orderSchema);
'''
    with open(os.path.join(models_dir, 'order.js'), 'w') as f:
        f.write(order_model)

    # .env file
    env_content = '''PORT=3000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/node-service
LOG_LEVEL=debug
'''
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # .gitignore
    gitignore = '''node_modules/
.env
coverage/
dist/
*.log
'''
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # README.md
    readme = '''# Node Service - Order Management

A RESTful microservice for managing customer orders.

## Endpoints

- `GET /api/orders` - List all orders (filter by ?status=)
- `GET /api/orders/:id` - Get order by ID
- `POST /api/orders` - Create new order
- `GET /api/customers` - List all customers
- `GET /api/customers/:id` - Get customer by ID
- `GET /health` - Health check

## Development

```bash
npm install
npm run dev    # starts with --inspect=9229
npm start      # production mode
```
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Ensure NO .vscode/launch.json exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json_path = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Project created at: {PROJECT_DIR}')

    # Simulate a process listening on port 9229 (Node.js inspect port)
    # Use a simple Python socket server since node may not be installed
    listener_script = os.path.join(WORKDIR, '_inspect_listener.py')
    with open(listener_script, 'w') as f:
        f.write('import socket, time\n')
        f.write('s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n')
        f.write('s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n')
        f.write('s.bind(("127.0.0.1", 9229))\n')
        f.write('s.listen(1)\n')
        f.write('while True: time.sleep(60)\n')

    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        ['python3', listener_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(1)
    print('Simulated inspect process listening on port 9229')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
