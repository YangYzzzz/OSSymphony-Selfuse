"""
Initial Setup: Create a JavaScript config file with single-quoted strings for regex replacement task
Task ID: vscode_gs_074
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_074'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
SRC_DIR = f'{PROJECT_DIR}/src'
OUTPUT = f'{SRC_DIR}/config.js'


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
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create a realistic JavaScript config file with single-quoted strings
    # Contains: 12 single-quoted strings, escaped apostrophes, and template literals
    content = r"""// Application Configuration
// Last updated: 2025-11-18

const environment = 'production';
const hostname = 'localhost';
const apiBase = '/api/v1';
const secretKey = 'sk-92xJ4mNpQrT8vWzY';
const dbHost = 'db.internal.mycompany.io';
const logLevel = 'warning';
const appName = 'WebApp Dashboard';
const region = 'us-east-1';
const cacheDriver = 'redis';
const sessionTimeout = '3600';
const welcomeMsg = 'it\'s working';
const errorMsg = 'something\'s not right';

// Template literals - these should NOT be changed
const dynamicUrl = `https://${hostname}:${port}/health`;
const greeting = `Hello, ${userName}! Welcome to ${appName}`;
const queryString = `SELECT * FROM users WHERE region = '${region}'`;

// Numeric and boolean values - no quotes involved
const maxRetries = 5;
const enableCache = true;
const timeout = 30000;

// Mixed usage in objects
const dbConfig = {
    host: 'db.internal.mycompany.io',
    port: 5432,
    name: 'webapp_prod',
    ssl: true,
    poolSize: 10,
    connectionString: `postgresql://${dbHost}:5432/webapp_prod`
};

const routes = {
    home: '/dashboard',
    login: '/auth/login',
    api: '/api/v1/resources',
    health: '/status/health'
};

module.exports = {
    environment,
    hostname,
    apiBase,
    secretKey,
    dbHost,
    logLevel,
    appName,
    region,
    cacheDriver,
    sessionTimeout,
    welcomeMsg,
    errorMsg,
    dynamicUrl,
    greeting,
    queryString,
    maxRetries,
    enableCache,
    timeout,
    dbConfig,
    routes
};
"""

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Also create a basic package.json for realism
    pkg_json = '''{
  "name": "webapp-dashboard",
  "version": "2.4.1",
  "description": "Internal web application dashboard",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  }
}
'''
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(pkg_json)

    # Open VSCode with the project folder and the config file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
