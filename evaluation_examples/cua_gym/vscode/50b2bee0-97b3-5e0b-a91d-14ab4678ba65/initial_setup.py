"""
Initial Setup: Enable Emmet abbreviation expansion inside JSX
Task ID: vscode_web_008
Domain: vs_code

Creates a react-app project with a .jsx file and .vscode/settings.json
that has NO Emmet settings. Opens VSCode with the project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_008'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SETTINGS_PATH = os.path.join(VSCODE_DIR, 'settings.json')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # Create .vscode/settings.json with basic settings but NO Emmet config
    settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created settings: {SETTINGS_PATH}')

    # Create package.json
    package_json = {
        "name": "react-app",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src/App.jsx - the main component file
    app_jsx_content = """import React from 'react';

function App() {
    return (
        <div className="app">
            <header className="app-header">
                <h1>Welcome to React</h1>
                <p>Edit this file and save to reload.</p>
            </header>
            <main className="content">
                <section className="features">
                    <h2>Features</h2>
                    <ul>
                        <li>Fast Refresh</li>
                        <li>JSX Support</li>
                        <li>Component-Based Architecture</li>
                    </ul>
                </section>
            </main>
        </div>
    );
}

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'App.jsx'), 'w') as f:
        f.write(app_jsx_content)

    # Create src/index.jsx
    index_jsx_content = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.jsx'), 'w') as f:
        f.write(index_jsx_content)

    # Create src/components/Button.jsx
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    button_jsx_content = """import React from 'react';

function Button({ label, onClick, variant = 'primary' }) {
    const className = `btn btn-${variant}`;
    return (
        <button className={className} onClick={onClick}>
            {label}
        </button>
    );
}

export default Button;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Button.jsx'), 'w') as f:
        f.write(button_jsx_content)

    # Create public/index.html
    index_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>React App</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write(index_html_content)

    print(f'Project created at: {PROJECT_DIR}')

    # Launch VSCode with the project folder, opening App.jsx
    launch_gui(f'code "{PROJECT_DIR}" "{PROJECT_DIR}/src/App.jsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
