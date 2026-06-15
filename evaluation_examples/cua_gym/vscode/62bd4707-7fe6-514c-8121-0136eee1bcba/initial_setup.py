"""
Initial Setup: Open VSCode with a JavaScript web-app project for ESLint configuration
Task ID: vscode_gf2_021
Domain: vscode

Creates a realistic JavaScript web-app project at /home/user/projects/web-app
with package.json and source files. Opens VSCode with the project folder.
ESLint is NOT installed and no ESLint settings exist.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_021'
PROJECT_DIR = f'{WORKDIR}/projects/web-app'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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
    """Create a realistic JavaScript web-app project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json — a typical web app with dependencies but NO eslint
    package_json = {
        "name": "web-app",
        "version": "1.0.0",
        "description": "Customer portal web application for Meridian Analytics",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "build": "echo 'Build step placeholder'",
            "test": "echo 'No tests configured yet'"
        },
        "keywords": ["analytics", "dashboard", "portal"],
        "author": "Elena Rodriguez <elena.rodriguez@meridian-analytics.com>",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js — main server file with some style issues ESLint would catch
    index_js = '''const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// Route imports
const dashboardRoutes = require('./routes/dashboard');
const userRoutes = require('./routes/users');

app.use('/api/dashboard', dashboardRoutes);
app.use('/api/users', userRoutes);

app.get('/', (req, res) => {
    res.json({
        message: 'Meridian Analytics API',
        version: '1.0.0',
        endpoints: ['/api/dashboard', '/api/users']
    })
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
});
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # src/routes/dashboard.js
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    dashboard_js = '''const express = require('express');
const router = express.Router();

const metrics = [
    { id: 1, name: 'Monthly Active Users', value: 14523, trend: 'up', change: 12.3 },
    { id: 2, name: 'Revenue', value: 284750, trend: 'up', change: 8.7 },
    { id: 3, name: 'Churn Rate', value: 2.4, trend: 'down', change: -0.5 },
    { id: 4, name: 'Avg Session Duration', value: 340, trend: 'up', change: 15.1 },
    { id: 5, name: 'Support Tickets', value: 87, trend: 'down', change: -22.0 }
];

router.get('/metrics', (req, res) => {
    const { category } = req.query
    if (category) {
        const filtered = metrics.filter(m => m.name.toLowerCase().includes(category.toLowerCase()))
        return res.json(filtered)
    }
    res.json(metrics)
});

router.get('/metrics/:id', (req, res) => {
    const metric = metrics.find(m => m.id === parseInt(req.params.id))
    if (!metric) {
        return res.status(404).json({ error: 'Metric not found' })
    }
    res.json(metric)
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/dashboard.js', 'w') as f:
        f.write(dashboard_js)

    # src/routes/users.js
    users_js = '''const express = require('express');
const router = express.Router();

let users = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@example.com', role: 'admin', lastLogin: '2025-03-28' },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@example.com', role: 'analyst', lastLogin: '2025-03-27' },
    { id: 3, name: 'Priya Patel', email: 'priya.p@example.com', role: 'viewer', lastLogin: '2025-03-25' },
    { id: 4, name: 'James O\\'Brien', email: 'james.ob@example.com', role: 'analyst', lastLogin: '2025-03-26' },
    { id: 5, name: 'Aisha Nakamura', email: 'aisha.n@example.com', role: 'admin', lastLogin: '2025-03-28' }
];

router.get('/', (req, res) => {
    res.json(users)
});

router.post('/', (req, res) => {
    const { name, email, role } = req.body
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' })
    }
    const newUser = {
        id: users.length + 1,
        name,
        email,
        role: role || 'viewer',
        lastLogin: new Date().toISOString().split('T')[0]
    }
    users.push(newUser)
    res.status(201).json(newUser)
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/users.js', 'w') as f:
        f.write(users_js)

    # src/components/DataTable.js — a utility module
    datatable_js = '''class DataTable {
    constructor(data, columns) {
        this.data = data
        this.columns = columns
        this.sortColumn = null
        this.sortDirection = 'asc'
    }

    sort(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
        } else {
            this.sortColumn = column
            this.sortDirection = 'asc'
        }

        this.data.sort((a, b) => {
            const valA = a[column]
            const valB = b[column]
            const modifier = this.sortDirection === 'asc' ? 1 : -1
            if (typeof valA === 'string') {
                return valA.localeCompare(valB) * modifier
            }
            return (valA - valB) * modifier
        })
    }

    filter(predicate) {
        return this.data.filter(predicate)
    }

    paginate(page, pageSize) {
        const start = (page - 1) * pageSize
        return this.data.slice(start, start + pageSize)
    }
}

module.exports = DataTable;
'''
    with open(f'{PROJECT_DIR}/src/components/DataTable.js', 'w') as f:
        f.write(datatable_js)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meridian Analytics Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
        h1 { color: #2c3e50; }
        .card { background: white; border-radius: 8px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Meridian Analytics</h1>
    <div class="card">
        <h2>Dashboard</h2>
        <p>Loading metrics...</p>
    </div>
</body>
</html>
'''
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)

    # .env file
    env_content = '''PORT=3000
NODE_ENV=development
LOG_LEVEL=debug
'''
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # .gitignore
    gitignore = '''node_modules/
.env
dist/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    print(f'Project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up minimal VSCode settings WITHOUT any ESLint config."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Basic editor settings — NO eslint-related settings
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    # Explicitly remove any ESLint settings if they exist
    for key in list(settings.keys()):
        if 'eslint' in key.lower():
            del settings[key]
    if 'editor.codeActionsOnSave' in settings:
        if isinstance(settings['editor.codeActionsOnSave'], dict):
            settings['editor.codeActionsOnSave'].pop('source.fixAll.eslint', None)
            if not settings['editor.codeActionsOnSave']:
                del settings['editor.codeActionsOnSave']

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured at: {SETTINGS_PATH}')


def ensure_eslint_not_installed():
    """Uninstall ESLint extension if it happens to be pre-installed."""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'dbaeumer.vscode-eslint' in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', 'dbaeumer.vscode-eslint'],
                capture_output=True, text=True, timeout=60
            )
            print('Uninstalled pre-existing ESLint extension')
        else:
            print('ESLint extension not installed (good)')
    except Exception as e:
        print(f'Extension check note: {e}')


def main():
    create_project()
    setup_vscode_settings()
    ensure_eslint_not_installed()

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
