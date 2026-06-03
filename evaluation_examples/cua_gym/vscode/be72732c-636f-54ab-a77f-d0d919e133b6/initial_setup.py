"""
Initial Setup: Configure ESLint in a React app via VSCode
Task ID: vscode_gf5_012
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_012'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'


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
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules', exist_ok=True)

    # --- package.json (standard CRA, NO eslint devDeps) ---
    package_json = {
        "name": "react-app",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "web-vitals": "^2.1.4"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- public/index.html ---
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Task management dashboard" />
    <title>TaskFlow - Project Dashboard</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
"""
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)

    # --- src/index.js ---
    index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # --- src/index.css ---
    index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}
"""
    with open(f'{PROJECT_DIR}/src/index.css', 'w') as f:
        f.write(index_css)

    # --- src/App.css ---
    app_css = """.app-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.app-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
}

.app-header p {
  margin: 0;
  opacity: 0.85;
  font-size: 16px;
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow 0.2s;
}

.task-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.task-title {
  font-weight: 600;
  color: #2d3748;
}

.task-assignee {
  color: #718096;
  font-size: 14px;
}

.task-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active {
  background: #c6f6d5;
  color: #276749;
}

.status-review {
  background: #fefcbf;
  color: #975a16;
}

.status-blocked {
  background: #fed7d7;
  color: #9b2c2c;
}
"""
    with open(f'{PROJECT_DIR}/src/App.css', 'w') as f:
        f.write(app_css)

    # --- src/App.js --- (WITH 3 intentional linting issues)
    # Issue 1: unused import (useState is imported but never used)
    # Issue 2: missing key prop in .map()
    # Issue 3: console.log statement
    app_js = """import React, { useState } from 'react';
import './App.css';

const tasks = [
  { id: 1, title: 'Design database schema', assignee: 'Sarah Chen', status: 'active' },
  { id: 2, title: 'Implement auth middleware', assignee: 'Marcus Johnson', status: 'review' },
  { id: 3, title: 'Set up CI/CD pipeline', assignee: 'Priya Patel', status: 'active' },
  { id: 4, title: 'Write API documentation', assignee: 'Alex Rivera', status: 'blocked' },
  { id: 5, title: 'Optimize query performance', assignee: 'Jordan Kim', status: 'review' },
];

function getStatusClass(status) {
  const classMap = {
    active: 'status-active',
    review: 'status-review',
    blocked: 'status-blocked',
  };
  return classMap[status] || '';
}

function App() {
  console.log('Rendering App component with tasks:', tasks.length);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TaskFlow Dashboard</h1>
        <p>Track your team's progress across all active projects</p>
      </header>
      <ul className="task-list">
        {tasks.map((task) => (
          <li className="task-item">
            <div>
              <div className="task-title">{task.title}</div>
              <div className="task-assignee">Assigned to: {task.assignee}</div>
            </div>
            <span className={`task-status ${getStatusClass(task.status)}`}>
              {task.status}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
"""
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write(app_js)

    # --- .gitignore ---
    gitignore = """node_modules/
/build
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = """# TaskFlow - React App

A project management dashboard built with React.

## Getting Started

```bash
npm install
npm start
```

## Team

- Sarah Chen - Backend Lead
- Marcus Johnson - Security Engineer
- Priya Patel - DevOps
- Alex Rivera - Technical Writer
- Jordan Kim - Database Specialist
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open App.js so the agent can see the issues
    launch_gui(f'code "{PROJECT_DIR}/src/App.js"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
