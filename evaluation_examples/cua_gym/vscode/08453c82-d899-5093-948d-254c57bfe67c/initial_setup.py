"""
Initial Setup: Configure VSCode to auto-fix ESLint issues on save
Task ID: vscode_web_003
Domain: vscode

Creates a webapp project with .js files that have ESLint-fixable warnings,
an ESLint config, and opens VSCode. No .vscode/settings.json exists yet.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_003'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
ESLINT_CONFIG = f'{PROJECT_DIR}/.eslintrc.json'


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

    # Ensure .vscode/settings.json does NOT exist
    if os.path.exists(VSCODE_DIR):
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        if os.path.exists(settings_path):
            os.remove(settings_path)

    # Create package.json
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "Customer portal web application",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "devDependencies": {
            "eslint": "^8.50.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create ESLint config
    eslint_config = {
        "env": {
            "browser": True,
            "node": True,
            "es2021": True
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "no-unused-vars": "warn",
            "no-extra-semi": "warn",
            "semi": ["warn", "always"],
            "quotes": ["warn", "single"],
            "indent": ["warn", 2],
            "no-trailing-spaces": "warn",
            "eol-last": ["warn", "always"],
            "no-multiple-empty-lines": ["warn", {"max": 1}]
        }
    }
    with open(ESLINT_CONFIG, 'w') as f:
        json.dump(eslint_config, f, indent=2)

    # Create src directory
    src_dir = f'{PROJECT_DIR}/src'
    os.makedirs(src_dir, exist_ok=True)

    # Create index.js with ESLint-fixable issues (wrong quotes, missing semicolons, extra spaces)
    index_js = '''const express = require("express")
const app = express()
const PORT = 3000

app.get("/", (req, res) => {
    res.send("Welcome to the Customer Portal");;
})

app.get("/api/customers", (req, res) => {
    const customers = [
        { id: 1, name: "Sarah Chen", email: "sarah@example.com" },
        { id: 2, name: "Marcus Johnson", email: "marcus@example.com" },
        { id: 3, name: "Priya Patel", email: "priya@example.com" }
    ]
    res.json(customers)
})

app.listen(PORT, () => {
    console.log("Server running on port " + PORT)
})
'''
    with open(f'{src_dir}/index.js', 'w') as f:
        f.write(index_js)

    # Create utils.js with more ESLint-fixable issues
    utils_js = '''function formatCurrency(amount) {
    return "$" + amount.toFixed(2)
}

function validateEmail(email) {
    const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/
    return regex.test(email)
}


function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1)
}

function getTimestamp() {
    return new Date().toISOString();;
}

module.exports = { formatCurrency, validateEmail, capitalize, getTimestamp }
'''
    with open(f'{src_dir}/utils.js', 'w') as f:
        f.write(utils_js)

    # Create config.js with more fixable issues
    config_js = '''const config = {
    appName: "Customer Portal",
    version: "1.0.0",
    database: {
        host: "localhost",
        port: 5432,
        name: "customers_db"
    },
    auth: {
        tokenExpiry: 3600,
        refreshTokenExpiry: 86400,
        secretKey: "dev-secret-key-change-in-production"
    },
    logging: {
        level: "info",
        format: "json"
    }
}

module.exports = config
'''
    with open(f'{src_dir}/config.js', 'w') as f:
        f.write(config_js)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'ESLint config: {ESLINT_CONFIG}')
    print(f'No .vscode/settings.json exists (as required)')

    # Install ESLint extension if not already present
    try:
        subprocess.run(['code', '--install-extension', 'dbaeumer.vscode-eslint'],
                       capture_output=True, text=True, timeout=30)
        print('ESLint extension installed/verified')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
