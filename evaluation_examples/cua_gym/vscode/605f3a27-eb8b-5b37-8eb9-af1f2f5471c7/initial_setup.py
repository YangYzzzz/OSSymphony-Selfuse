"""
Initial Setup: Set up a multi-command keybinding using runCommands
Task ID: vscode_rrt_090
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_090'
WORKSPACE = f'{WORKDIR}/workspace'

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")


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
    # --- Create Node.js project workspace ---
    os.makedirs(os.path.join(WORKSPACE, 'src'), exist_ok=True)

    # package.json
    package_json = {
        "name": "invoice-processor",
        "version": "1.2.0",
        "description": "Automated invoice processing and reporting system",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "build": "echo 'Compiling TypeScript...' && tsc && echo 'Build complete.'",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "winston": "^3.11.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "jest": "^29.7.0",
            "eslint": "^8.56.0",
            "@types/node": "^20.11.0",
            "@types/express": "^4.17.21"
        },
        "author": "Amara Okonkwo",
        "license": "MIT"
    }
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    index_js = '''\
const express = require('express');
const { Pool } = require('pg');
const { logger } = require('./utils');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

app.get('/api/invoices', async (req, res) => {
    try {
        const { rows } = await pool.query(
            'SELECT * FROM invoices ORDER BY created_at DESC LIMIT 50'
        );
        logger.info(`Fetched ${rows.length} invoices`);
        res.json({ success: true, data: rows });
    } catch (err) {
        logger.error('Failed to fetch invoices', { error: err.message });
        res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

app.post('/api/invoices', async (req, res) => {
    const { vendor, amount, due_date, description } = req.body;
    try {
        const { rows } = await pool.query(
            `INSERT INTO invoices (vendor, amount, due_date, description)
             VALUES ($1, $2, $3, $4) RETURNING *`,
            [vendor, amount, due_date, description]
        );
        logger.info(`Created invoice for ${vendor}: $${amount}`);
        res.status(201).json({ success: true, data: rows[0] });
    } catch (err) {
        logger.error('Failed to create invoice', { error: err.message });
        res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

app.delete('/api/invoices/:id', async (req, res) => {
    try {
        await pool.query('DELETE FROM invoices WHERE id = $1', [req.params.id]);
        logger.info(`Deleted invoice ${req.params.id}`);
        res.json({ success: true });
    } catch (err) {
        logger.error('Failed to delete invoice', { error: err.message });
        res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    logger.info(`Invoice processor running on port ${PORT}`);
});
'''
    with open(os.path.join(WORKSPACE, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # src/utils.js
    utils_js = '''\
const winston = require('winston');

const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
        new winston.transports.File({ filename: 'logs/combined.log' }),
    ],
});

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

function validateInvoice(invoice) {
    const required = ['vendor', 'amount', 'due_date'];
    const missing = required.filter(field => !invoice[field]);
    if (missing.length > 0) {
        throw new Error(`Missing required fields: ${missing.join(', ')}`);
    }
    if (typeof invoice.amount !== 'number' || invoice.amount <= 0) {
        throw new Error('Amount must be a positive number');
    }
    return true;
}

module.exports = { logger, formatCurrency, validateInvoice };
'''
    with open(os.path.join(WORKSPACE, 'src', 'utils.js'), 'w') as f:
        f.write(utils_js)

    # .env file
    env_content = '''\
PORT=3000
DATABASE_URL=postgresql://admin:secret@localhost:5432/invoices_db
LOG_LEVEL=info
NODE_ENV=development
'''
    with open(os.path.join(WORKSPACE, '.env'), 'w') as f:
        f.write(env_content)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(WORKSPACE, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- Set keybindings.json to empty array ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'keybindings.json set to empty at: {KEYBINDINGS_PATH}')

    print(f'Workspace created at: {WORKSPACE}')

    # --- Launch VSCode with workspace ---
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
