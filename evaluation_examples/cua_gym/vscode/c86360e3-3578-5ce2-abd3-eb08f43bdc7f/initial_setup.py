"""
Initial Setup: Install ESLint extension, create .eslintrc.json, configure auto-fix on save
Task ID: vscode_wf_015
Domain: vscode

Initial state: ~/project with JS files, ESLint globally installed via npm,
NO ESLint extension, NO .eslintrc.json, NO codeActionsOnSave setting.
VSCode open with ~/project.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_015'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
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


def create_initial():
    # --- Create ~/project directory with JS files ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # app.js — has linting issues (unused vars, missing semicolons, double quotes)
    app_js = '''\
const express = require("express");
const app = express();
const unusedMiddleware = require("body-parser")

const PORT = 3000

app.get("/", (req, res) => {
    const greeting = "Hello, World!"
    res.send(greeting)
})

app.get("/users", (req, res) => {
    const users = [
        { name: "Alice Chen", age: 28 },
        { name: "Bob Martinez", age: 34 },
        { name: "Carol Williams", age: 25 }
    ]
    const unusedFilter = "active"
    res.json(users)
})

app.get("/products", (req, res) => {
    const products = [
        { id: 1, name: "Wireless Mouse", price: 29.99 },
        { id: 2, name: "Mechanical Keyboard", price: 89.50 },
        { id: 3, name: "USB-C Hub", price: 45.00 }
    ]
    const discountRate = 0.15
    res.json(products)
})

app.listen(PORT, () => {
    console.log("Server running on port " + PORT)
})
'''
    with open(os.path.join(PROJECT_DIR, 'app.js'), 'w') as f:
        f.write(app_js)

    # utils.js — more linting issues
    utils_js = '''\
const fs = require("fs")
const path = require("path")

function formatDate(date) {
    const options = { year: "numeric", month: "long", day: "numeric" }
    return date.toLocaleDateString("en-US", options)
}

function calculateTotal(items) {
    const taxRate = 0.08
    let subtotal = 0
    for (let i = 0; i < items.length; i++) {
        subtotal += items[i].price * items[i].quantity
    }
    const tax = subtotal * taxRate
    return subtotal + tax
}

function parseConfig(filePath) {
    const rawData = fs.readFileSync(filePath, "utf-8")
    const config = JSON.parse(rawData)
    const unusedDefault = { timeout: 5000 }
    return config
}

function generateId() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    let result = ""
    for (let i = 0; i < 12; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return result
}

module.exports = { formatDate, calculateTotal, parseConfig, generateId }
'''
    with open(os.path.join(PROJECT_DIR, 'utils.js'), 'w') as f:
        f.write(utils_js)

    # config.js — configuration file with issues
    config_js = '''\
const dotenv = require("dotenv")
dotenv.config()

const config = {
    database: {
        host: process.env.DB_HOST || "localhost",
        port: parseInt(process.env.DB_PORT) || 5432,
        name: process.env.DB_NAME || "myapp_dev",
        user: process.env.DB_USER || "admin",
        password: process.env.DB_PASSWORD || "secret123"
    },
    server: {
        port: parseInt(process.env.SERVER_PORT) || 3000,
        env: process.env.NODE_ENV || "development"
    },
    logging: {
        level: process.env.LOG_LEVEL || "info",
        format: "json"
    }
}

const unusedSecret = "sk-placeholder-key-12345"

module.exports = config
'''
    with open(os.path.join(PROJECT_DIR, 'config.js'), 'w') as f:
        f.write(config_js)

    # package.json
    package_json = {
        "name": "vscode-wf-015-project",
        "version": "1.0.0",
        "description": "Sample Node.js project for ESLint configuration task",
        "main": "app.js",
        "scripts": {
            "start": "node app.js",
            "lint": "eslint ."
        },
        "dependencies": {
            "express": "^4.18.2",
            "body-parser": "^1.20.2",
            "dotenv": "^16.3.1"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- Ensure NO .eslintrc.json exists ---
    eslintrc_path = os.path.join(PROJECT_DIR, '.eslintrc.json')
    if os.path.exists(eslintrc_path):
        os.remove(eslintrc_path)

    # --- Ensure NO ESLint extension is installed ---
    subprocess.run(['code', '--uninstall-extension', 'dbaeumer.vscode-eslint'],
                   capture_output=True, text=True)

    # --- Ensure settings.json does NOT have codeActionsOnSave ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}
    # Remove any existing codeActionsOnSave
    settings.pop('editor.codeActionsOnSave', None)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'JS files: app.js, utils.js, config.js, package.json')
    print(f'ESLint extension uninstalled (if was present)')
    print(f'No .eslintrc.json, no codeActionsOnSave setting')

    # --- GUI-ready: open VSCode with ~/project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
