"""
Initial Setup: Fix JSON syntax error in .vscode/extensions.json
Task ID: vscode_fix_082
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_082'
PROJECT_DIR = os.path.join(WORKDIR, 'team-project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # Create .vscode/extensions.json with INVALID JSON (trailing comma)
    extensions_content = """{
    "recommendations": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-python.python",
        "eamodio.gitlens",
    ]
}"""
    with open(os.path.join(VSCODE_DIR, 'extensions.json'), 'w') as f:
        f.write(extensions_content)

    # Create .vscode/settings.json (valid, workspace settings)
    settings_content = """{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "python.linting.enabled": true,
    "files.trimTrailingWhitespace": true
}"""
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        f.write(settings_content)

    # Create realistic project files
    # package.json
    package_json = """{
    "name": "team-project",
    "version": "2.1.0",
    "description": "Internal dashboard for sales analytics",
    "main": "src/index.js",
    "scripts": {
        "start": "node src/index.js",
        "test": "jest --coverage",
        "lint": "eslint src/"
    },
    "dependencies": {
        "express": "^4.18.2",
        "pg": "^8.11.3",
        "dotenv": "^16.3.1"
    },
    "devDependencies": {
        "jest": "^29.7.0",
        "eslint": "^8.56.0",
        "prettier": "^3.2.4"
    }
}"""
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write(package_json)

    # src/index.js
    index_js = """const express = require('express');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

app.get('/api/sales', async (req, res) => {
    try {
        const { rows } = await pool.query(
            'SELECT region, SUM(amount) as total FROM sales GROUP BY region ORDER BY total DESC'
        );
        res.json(rows);
    } catch (err) {
        console.error('Database query failed:', err.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/sales/:region', async (req, res) => {
    try {
        const { rows } = await pool.query(
            'SELECT month, amount, rep_name FROM sales WHERE region = $1 ORDER BY month',
            [req.params.region]
        );
        res.json(rows);
    } catch (err) {
        console.error('Query failed:', err.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(port, () => {
    console.log(`Sales dashboard API running on port ${port}`);
});
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # src/utils.js
    utils_js = """/**
 * Utility functions for the sales dashboard
 */

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

function calculateGrowth(current, previous) {
    if (previous === 0) return null;
    return ((current - previous) / previous) * 100;
}

function getQuarter(month) {
    return Math.ceil(month / 3);
}

module.exports = { formatCurrency, calculateGrowth, getQuarter };
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'utils.js'), 'w') as f:
        f.write(utils_js)

    # tests/utils.test.js
    test_js = """const { formatCurrency, calculateGrowth, getQuarter } = require('../src/utils');

describe('formatCurrency', () => {
    test('formats positive amounts', () => {
        expect(formatCurrency(1234.56)).toBe('$1,234.56');
    });

    test('formats zero', () => {
        expect(formatCurrency(0)).toBe('$0.00');
    });
});

describe('calculateGrowth', () => {
    test('calculates positive growth', () => {
        expect(calculateGrowth(150, 100)).toBe(50);
    });

    test('returns null for zero previous', () => {
        expect(calculateGrowth(100, 0)).toBeNull();
    });
});

describe('getQuarter', () => {
    test('returns correct quarters', () => {
        expect(getQuarter(1)).toBe(1);
        expect(getQuarter(6)).toBe(2);
        expect(getQuarter(12)).toBe(4);
    });
});
"""
    with open(os.path.join(PROJECT_DIR, 'tests', 'utils.test.js'), 'w') as f:
        f.write(test_js)

    # README.md
    readme = """# Team Project - Sales Analytics Dashboard

## Overview
Internal dashboard for tracking regional sales performance. Built with Express.js and PostgreSQL.

## Setup
1. Install dependencies: `npm install`
2. Copy `.env.example` to `.env` and configure database URL
3. Run migrations: `npm run migrate`
4. Start server: `npm start`

## API Endpoints
- `GET /api/sales` - Aggregated sales by region
- `GET /api/sales/:region` - Monthly breakdown for a region

## Development
- Run tests: `npm test`
- Lint: `npm run lint`

## Team
- Sarah Chen (Backend Lead)
- Marcus Rivera (Frontend)
- Aisha Patel (Data Engineering)
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # .gitignore
    gitignore = """node_modules/
.env
coverage/
dist/
*.log
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'extensions.json with trailing comma (invalid JSON) at: {VSCODE_DIR}/extensions.json')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
