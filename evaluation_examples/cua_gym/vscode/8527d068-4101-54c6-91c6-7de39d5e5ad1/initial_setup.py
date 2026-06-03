"""
Initial Setup: Configure a Jest test runner in VSCode project
Task ID: vscode_gf5_013
Domain: vscode

Creates ~/projects/api-tests with:
- package.json (no test framework)
- src/utils.js with calculateTax function
- NO jest, NO tests, NO jest.config.js
Opens VSCode with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_013'
PROJECT_DIR = f'{WORKDIR}/projects/api-tests'
SRC_DIR = f'{PROJECT_DIR}/src'

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
    os.makedirs(SRC_DIR, exist_ok=True)

    # --- package.json (no test framework) ---
    package_json = {
        "name": "api-tests",
        "version": "1.0.0",
        "description": "REST API integration and utility functions for the payments service",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "lint": "eslint src/"
        },
        "keywords": ["api", "payments", "utilities"],
        "author": "DevOps Team",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "axios": "^1.6.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/package.json')

    # --- src/utils.js with calculateTax function ---
    utils_js = '''/**
 * Utility functions for the payments service.
 * Handles tax calculations, currency formatting, and validation.
 */

/**
 * Calculate tax amount for a given price and tax rate.
 * @param {number} amount - The base amount before tax
 * @param {number} rate - The tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns {number} The calculated tax amount, rounded to 2 decimal places
 */
function calculateTax(amount, rate) {
    if (typeof amount !== 'number' || typeof rate !== 'number') {
        throw new TypeError('Both amount and rate must be numbers');
    }
    if (amount < 0) {
        throw new RangeError('Amount cannot be negative');
    }
    if (rate < 0 || rate > 1) {
        throw new RangeError('Rate must be between 0 and 1');
    }
    return Math.round(amount * rate * 100) / 100;
}

/**
 * Format a number as USD currency string.
 * @param {number} value - The numeric value
 * @returns {string} Formatted currency string (e.g., "$1,234.56")
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

/**
 * Validate an email address format.
 * @param {string} email - The email to validate
 * @returns {boolean} True if valid email format
 */
function validateEmail(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}

module.exports = { calculateTax, formatCurrency, validateEmail };
'''
    with open(f'{SRC_DIR}/utils.js', 'w') as f:
        f.write(utils_js)
    print(f'Created: {SRC_DIR}/utils.js')

    # --- src/index.js (main entry point) ---
    index_js = '''const express = require('express');
const { calculateTax, formatCurrency } = require('./utils');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/tax', (req, res) => {
    const { amount, rate } = req.query;
    try {
        const tax = calculateTax(parseFloat(amount), parseFloat(rate));
        res.json({
            amount: parseFloat(amount),
            rate: parseFloat(rate),
            tax: tax,
            total: formatCurrency(parseFloat(amount) + tax)
        });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`Payments API running on port ${PORT}`);
});
'''
    with open(f'{SRC_DIR}/index.js', 'w') as f:
        f.write(index_js)
    print(f'Created: {SRC_DIR}/index.js')

    # --- .gitignore ---
    gitignore = '''node_modules/
.env
coverage/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)
    print(f'Created: {PROJECT_DIR}/.gitignore')

    # --- README.md ---
    readme = '''# API Tests - Payments Service

Utility functions and REST API endpoints for the payments processing service.

## Getting Started

```bash
npm install
npm start
```

## API Endpoints

- `GET /api/tax?amount=100&rate=0.08` - Calculate tax for a given amount and rate

## Project Structure

```
src/
  index.js   - Express server and API routes
  utils.js   - Utility functions (tax calculation, formatting, validation)
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)
    print(f'Created: {PROJECT_DIR}/README.md')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
