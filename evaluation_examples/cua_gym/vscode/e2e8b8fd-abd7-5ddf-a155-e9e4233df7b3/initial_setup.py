"""
Initial Setup: Create web project without .editorconfig file
Task ID: vscode_file_062
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_062'
PROJECT_DIR = f'{WORKDIR}/web-project'


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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Create package.json with realistic content
    package_json = '''{
  "name": "web-project",
  "version": "1.0.0",
  "description": "A modern web application",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "build": "webpack --mode production",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "webpack": "^5.88.0",
    "webpack-cli": "^5.1.0"
  },
  "author": "Dev Team",
  "license": "MIT"
}
'''
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(package_json)

    # Create src/app.js with realistic content
    app_js = '''const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.get('/api/status', (req, res) => {
    res.json({
        status: 'running',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

app.get('/api/users', (req, res) => {
    const users = [
        { id: 1, name: 'Sarah Chen', role: 'admin' },
        { id: 2, name: 'Marcus Johnson', role: 'editor' },
        { id: 3, name: 'Elena Rodriguez', role: 'viewer' }
    ];
    res.json(users);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write(app_js)

    # Create src/styles.css with realistic content
    styles_css = '''/* Main stylesheet for web-project */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --accent-color: #e74c3c;
    --bg-color: #f8f9fa;
    --text-color: #333333;
    --font-size-base: 16px;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: var(--font-size-base);
    color: var(--text-color);
    background-color: var(--bg-color);
    line-height: 1.6;
}

header {
    background-color: var(--secondary-color);
    color: #ffffff;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 1.5rem;
}

nav ul li a {
    color: #ffffff;
    text-decoration: none;
    transition: color 0.3s;
}

nav ul li a:hover {
    color: var(--primary-color);
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.card {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

button {
    background-color: var(--primary-color);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #2980b9;
}
'''
    with open(f'{PROJECT_DIR}/src/styles.css', 'w') as f:
        f.write(styles_css)

    # Verify NO .editorconfig exists in the project
    editorconfig_path = f'{PROJECT_DIR}/.editorconfig'
    if os.path.exists(editorconfig_path):
        os.remove(editorconfig_path)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'  - {PROJECT_DIR}/package.json')
    print(f'  - {PROJECT_DIR}/src/app.js')
    print(f'  - {PROJECT_DIR}/src/styles.css')
    print(f'  - No .editorconfig (agent must create it)')

    # GUI-ready startup: open VSCode with the web-project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with web-project folder (DISPLAY=:0)')


create_initial()
