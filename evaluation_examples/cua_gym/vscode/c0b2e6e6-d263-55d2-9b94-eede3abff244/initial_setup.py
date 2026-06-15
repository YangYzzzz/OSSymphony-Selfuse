"""
Initial Setup: VSCode Find in Folder task
Task ID: vscode_file_061
Domain: vs_code

Creates a project directory structure with JS files containing TODO comments,
then opens VSCode with the project folder ready for the agent to interact.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_061'
PROJECT_DIR = f'{WORKDIR}/project'


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


def create_project_structure():
    """Create the project directory structure with JS files."""

    # Create directories
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- src/app.js: contains a TODO comment on line 15 ---
    app_js_content = """\
// app.js - Main application entry point
const express = require('express');
const { initializeConfig } = require('./config');
const { formatDate, calculateTotal } = require('./utils');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize application configuration
initializeConfig();

// Middleware setup
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
// TODO: Add authentication middleware before routes are registered

app.get('/', (req, res) => {
    const currentDate = formatDate(new Date());
    res.json({
        message: 'Welcome to the API',
        date: currentDate,
        version: '1.0.0'
    });
});

app.get('/orders', (req, res) => {
    const orders = [
        { id: 1, item: 'Widget A', quantity: 5, price: 9.99 },
        { id: 2, item: 'Widget B', quantity: 3, price: 14.99 },
        { id: 3, item: 'Gadget Pro', quantity: 2, price: 29.99 }
    ];
    const total = calculateTotal(orders);
    res.json({ orders, total });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
"""

    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write(app_js_content)

    # --- src/utils.js: contains two TODO comments ---
    utils_js_content = """\
// utils.js - Utility functions for the application

/**
 * Formats a date object to a human-readable string
 * @param {Date} date - The date to format
 * @returns {string} - Formatted date string
 */
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Calculates the total cost of orders
 * @param {Array} orders - Array of order objects
 * @returns {number} - Total cost
 */
function calculateTotal(orders) {
    // TODO: Apply discount logic based on order volume thresholds
    return orders.reduce((sum, order) => {
        return sum + (order.quantity * order.price);
    }, 0);
}

/**
 * Validates user input data
 * @param {Object} data - The input data to validate
 * @returns {boolean} - Whether the data is valid
 */
function validateInput(data) {
    if (!data || typeof data !== 'object') {
        return false;
    }
    const requiredFields = ['name', 'email', 'quantity'];
    return requiredFields.every(field => field in data && data[field] !== null);
}

/**
 * Generates a unique order ID
 * @returns {string} - A unique identifier
 */
function generateOrderId() {
    // TODO: Replace with UUID library for production use
    const timestamp = Date.now().toString(36);
    const randomPart = Math.random().toString(36).substring(2, 8);
    return `ORD-${timestamp}-${randomPart}`.toUpperCase();
}

module.exports = {
    formatDate,
    calculateTotal,
    validateInput,
    generateOrderId
};
"""

    with open(f'{PROJECT_DIR}/src/utils.js', 'w') as f:
        f.write(utils_js_content)

    # --- src/config.js: no TODO comments ---
    config_js_content = """\
// config.js - Application configuration management

const DEFAULT_CONFIG = {
    port: 3000,
    env: 'development',
    logLevel: 'info',
    database: {
        host: 'localhost',
        port: 5432,
        name: 'app_db',
        pool: {
            min: 2,
            max: 10
        }
    },
    cache: {
        enabled: true,
        ttl: 3600,
        maxSize: 1000
    },
    api: {
        rateLimit: 100,
        timeout: 30000
    }
};

let currentConfig = { ...DEFAULT_CONFIG };

/**
 * Initialize application configuration
 * Merges environment-specific overrides with defaults
 */
function initializeConfig() {
    const env = process.env.NODE_ENV || 'development';
    currentConfig.env = env;

    if (env === 'production') {
        currentConfig.logLevel = 'warn';
        currentConfig.database.pool.min = 5;
        currentConfig.database.pool.max = 20;
    } else if (env === 'test') {
        currentConfig.logLevel = 'error';
        currentConfig.database.name = 'app_test_db';
    }

    if (process.env.PORT) {
        currentConfig.port = parseInt(process.env.PORT, 10);
    }

    if (process.env.DB_HOST) {
        currentConfig.database.host = process.env.DB_HOST;
    }

    return currentConfig;
}

/**
 * Get the current configuration
 * @returns {Object} - Current configuration object
 */
function getConfig() {
    return { ...currentConfig };
}

/**
 * Update a specific configuration key
 * @param {string} key - Configuration key to update
 * @param {*} value - New value for the key
 */
function setConfigValue(key, value) {
    if (key in DEFAULT_CONFIG) {
        currentConfig[key] = value;
    }
}

module.exports = {
    initializeConfig,
    getConfig,
    setConfigValue
};
"""

    with open(f'{PROJECT_DIR}/src/config.js', 'w') as f:
        f.write(config_js_content)

    # --- tests/test_app.js: contains a TODO comment ---
    test_app_js_content = """\
// test_app.js - Tests for the main application module
const assert = require('assert');

// Mock the express module for testing
const mockApp = {
    routes: [],
    use: function(middleware) { this.routes.push({ type: 'middleware', fn: middleware }); },
    get: function(path, handler) { this.routes.push({ type: 'get', path, handler }); },
    listen: function(port, callback) { if (callback) callback(); }
};

describe('Application Routes', function() {
    it('should register the root route', function() {
        const rootRoute = mockApp.routes.find(r => r.type === 'get' && r.path === '/');
        assert.ok(rootRoute, 'Root route should be registered');
    });

    it('should register the orders route', function() {
        const ordersRoute = mockApp.routes.find(r => r.type === 'get' && r.path === '/orders');
        assert.ok(ordersRoute, 'Orders route should be registered');
    });

    // TODO: Add tests for POST /orders and PUT /orders/:id endpoints

    it('should return valid JSON from root route', function() {
        let responseData = null;
        const mockRes = {
            json: function(data) { responseData = data; }
        };
        assert.ok(true, 'JSON response test placeholder');
    });
});

describe('Server Configuration', function() {
    it('should use default port 3000 when PORT env is not set', function() {
        const defaultPort = process.env.PORT || 3000;
        assert.strictEqual(parseInt(defaultPort), 3000);
    });

    it('should start successfully', function() {
        assert.ok(true, 'Server start test placeholder');
    });
});
"""

    with open(f'{PROJECT_DIR}/tests/test_app.js', 'w') as f:
        f.write(test_app_js_content)

    # --- package.json ---
    package_json = {
        "name": "my-express-app",
        "version": "1.0.0",
        "description": "A simple Express.js web application",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js",
            "test": "mocha tests/"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "devDependencies": {
            "mocha": "^10.2.0",
            "nodemon": "^3.0.1"
        },
        "keywords": ["express", "nodejs", "api"],
        "author": "Development Team",
        "license": "MIT"
    }

    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    print(f'Project structure created at: {PROJECT_DIR}')
    print('  src/app.js   (1 TODO comment on line 15)')
    print('  src/utils.js (2 TODO comments)')
    print('  src/config.js (no TODO comments)')
    print('  tests/test_app.js (1 TODO comment)')
    print('  package.json')


def create_initial():
    create_project_structure()

    # Configure VSCode settings for proper explorer view
    vscode_user_dir = '/home/user/.config/Code/User'
    os.makedirs(vscode_user_dir, exist_ok=True)
    settings_path = os.path.join(vscode_user_dir, 'settings.json')

    # Load existing settings if any
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Configure settings for better explorer and search visibility
    settings.update({
        "workbench.activityBar.location": "default",
        "explorer.openEditors.visible": 1,
        "workbench.sideBar.location": "left",
    })

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

    print('VSCode settings configured.')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
