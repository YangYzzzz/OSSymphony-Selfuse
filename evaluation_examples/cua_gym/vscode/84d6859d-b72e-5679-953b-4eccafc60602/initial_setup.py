"""
Initial Setup: Configure Live Share code review session in VSCode
Task ID: vscode_gf3_080
Domain: vscode

Creates a realistic api-service project directory and opens VSCode.
Does NOT include any Live Share settings or .vsls.json file.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_080'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'api-service')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip comments)
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_project():
    """Create a realistic api-service project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    pkg = {
        "name": "api-service",
        "version": "2.4.1",
        "description": "Internal REST API service for customer data management",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --coverage",
            "lint": "eslint src/",
            "build": "tsc && node scripts/build.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "winston": "^3.11.0"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.2",
            "eslint": "^8.53.0",
            "typescript": "^5.3.2"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # .env file (sensitive - should be excluded from Live Share)
    env_content = """# Database Configuration
DB_HOST=prod-db-cluster.internal.acme.io
DB_PORT=27017
DB_NAME=customer_api
DB_USER=api_service_prod
DB_PASSWORD=kX9$mP2vL#nQ8wR4

# JWT Configuration
JWT_SECRET=a7f3e2d1c9b8a6f5e4d3c2b1a0f9e8d7
JWT_EXPIRY=3600

# External API Keys
STRIPE_API_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dc
SENDGRID_API_KEY=SG.xYzAbCdEfGhIjKlMnOpQrS.1234567890abcdefghijklmnop

# Server Config
PORT=3000
NODE_ENV=production
"""
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    with open(os.path.join(PROJECT_DIR, '.env.development'), 'w') as f:
        f.write("DB_HOST=localhost\nDB_PORT=27017\nDB_NAME=customer_api_dev\nDB_USER=dev\nDB_PASSWORD=devpass123\nPORT=3001\nNODE_ENV=development\n")

    # src directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    index_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { connectDB } = require('./config/database');
const customerRoutes = require('./routes/customers');
const authRoutes = require('./routes/auth');
const { errorHandler } = require('./middleware/errorHandler');
const logger = require('./utils/logger');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/customers', customerRoutes);
app.use(errorHandler);

connectDB().then(() => {
    app.listen(PORT, () => {
        logger.info(`API service running on port ${PORT}`);
    });
});

module.exports = app;
'''
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # Routes directory
    routes_dir = os.path.join(src_dir, 'routes')
    os.makedirs(routes_dir, exist_ok=True)

    customers_route = '''const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const Customer = require('../models/Customer');

router.get('/', authenticate, async (req, res) => {
    try {
        const customers = await Customer.find()
            .sort({ createdAt: -1 })
            .limit(parseInt(req.query.limit) || 50);
        res.json({ success: true, data: customers });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

router.post('/', authenticate, async (req, res) => {
    try {
        const customer = new Customer(req.body);
        await customer.save();
        res.status(201).json({ success: true, data: customer });
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
});

module.exports = router;
'''
    with open(os.path.join(routes_dir, 'customers.js'), 'w') as f:
        f.write(customers_route)

    # .gitignore
    gitignore = """node_modules/
dist/
.env
.env.*
*.log
coverage/
.DS_Store
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # Create stub node_modules and dist directories
    os.makedirs(os.path.join(PROJECT_DIR, 'node_modules', 'express'), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'node_modules', 'express', 'index.js'), 'w') as f:
        f.write('// express stub\n')

    os.makedirs(os.path.join(PROJECT_DIR, 'dist'), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'dist', 'bundle.js'), 'w') as f:
        f.write('// compiled output\n')

    # A log file
    with open(os.path.join(PROJECT_DIR, 'app.log'), 'w') as f:
        f.write('[2025-11-15T08:23:41Z] INFO: API service started on port 3000\n')
        f.write('[2025-11-15T08:23:42Z] INFO: Connected to MongoDB at prod-db-cluster.internal.acme.io\n')
        f.write('[2025-11-15T09:14:02Z] WARN: Rate limit exceeded for IP 192.168.1.45\n')

    print(f'Project created at: {PROJECT_DIR}')


def setup_initial_settings():
    """Set some baseline VSCode settings but NO liveshare settings."""
    # Remove any existing liveshare settings if present
    settings = load_settings()
    keys_to_remove = [k for k in settings if k.startswith('liveshare.')]
    for k in keys_to_remove:
        del settings[k]

    # Add some baseline settings
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.formatOnSave": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "terminal.integrated.defaultProfile.linux": "bash"
    })

    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Settings written to: {SETTINGS_PATH}')


def main():
    create_project()
    setup_initial_settings()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
