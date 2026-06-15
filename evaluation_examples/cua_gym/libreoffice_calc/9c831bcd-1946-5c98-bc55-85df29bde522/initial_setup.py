"""
Initial Setup: VSCode git branch workflow - React app project
Task ID: vscode_gf2_017
Domain: vscode (git)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_017'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
BARE_REPO = f'{WORKDIR}/projects/react-app-origin.git'


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


def run(cmd, cwd=None, env=None):
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=env
    )
    if result.returncode != 0:
        print(f"WARN: '{cmd}' returned {result.returncode}: {result.stderr.strip()}")
    return result.stdout.strip()


def create_initial():
    # Clean up any previous state
    subprocess.run(f'rm -rf "{PROJECT_DIR}" "{BARE_REPO}"', shell=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "react-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
""")

    # --- public/index.html ---
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="React dashboard application" />
    <title>React App</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
""")

    # --- src/index.js ---
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # --- src/index.css ---
    with open(f'{PROJECT_DIR}/src/index.css', 'w') as f:
        f.write("""body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
""")

    # --- src/App.js ---
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React, { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Project Dashboard</h1>
        <nav className="App-nav">
          <button
            className={activeTab === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={activeTab === 'analytics' ? 'active' : ''}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics
          </button>
          <button
            className={activeTab === 'settings' ? 'active' : ''}
            onClick={() => setActiveTab('settings')}
          >
            Settings
          </button>
        </nav>
      </header>
      <main className="App-main">
        {activeTab === 'dashboard' && (
          <section className="dashboard-panel">
            <h2>Welcome Back</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-value">1,284</span>
                <span className="stat-label">Active Users</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">$45,230</span>
                <span className="stat-label">Revenue</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">98.2%</span>
                <span className="stat-label">Uptime</span>
              </div>
            </div>
          </section>
        )}
        {activeTab === 'analytics' && (
          <section className="analytics-panel">
            <h2>Analytics Overview</h2>
            <p>Charts and metrics will be displayed here.</p>
          </section>
        )}
        {activeTab === 'settings' && (
          <section className="settings-panel">
            <h2>Application Settings</h2>
            <p>Configure your preferences below.</p>
          </section>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 Project Dashboard. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
""")

    # --- src/App.css (NO dark mode comment - that is the task) ---
    with open(f'{PROJECT_DIR}/src/App.css', 'w') as f:
        f.write(""".App {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.App-header {
  background-color: #282c34;
  padding: 20px 40px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.App-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.App-nav {
  display: flex;
  gap: 10px;
}

.App-nav button {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.App-nav button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.App-nav button.active {
  background-color: #61dafb;
  color: #282c34;
  border-color: #61dafb;
  font-weight: 600;
}

.App-main {
  flex: 1;
  padding: 40px;
  background-color: #f5f5f5;
}

.dashboard-panel,
.analytics-panel,
.settings-panel {
  max-width: 900px;
  margin: 0 auto;
  text-align: left;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #282c34;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 8px;
}

.App-footer {
  background-color: #282c34;
  color: rgba(255, 255, 255, 0.6);
  padding: 16px;
  font-size: 0.85rem;
}
""")

    # --- src/App.test.js ---
    with open(f'{PROJECT_DIR}/src/App.test.js', 'w') as f:
        f.write("""import { render, screen } from '@testing-library/react';
import App from './App';

test('renders project dashboard heading', () => {
  render(<App />);
  const heading = screen.getByText(/Project Dashboard/i);
  expect(heading).toBeInTheDocument();
});
""")

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
""")

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# React App - Project Dashboard

A modern React dashboard application with analytics and settings panels.

## Getting Started

```bash
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
""")

    # --- Initialize git repo ---
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Alex Rivera'
    git_env['GIT_AUTHOR_EMAIL'] = 'alex.rivera@techcorp.io'
    git_env['GIT_COMMITTER_NAME'] = 'Alex Rivera'
    git_env['GIT_COMMITTER_EMAIL'] = 'alex.rivera@techcorp.io'

    run('git init -b main', cwd=PROJECT_DIR, env=git_env)
    run('git add -A', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Initial commit: React dashboard app scaffold"', cwd=PROJECT_DIR, env=git_env)

    # Add a second commit for more realistic log
    with open(f'{PROJECT_DIR}/src/utils.js', 'w') as f:
        f.write("""/**
 * Utility functions for the dashboard application.
 */

export function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

export function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value);
}

export function formatPercentage(value) {
  return `${value.toFixed(1)}%`;
}
""")
    run('git add -A', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add utility formatting functions"', cwd=PROJECT_DIR, env=git_env)

    # Create a develop branch with another commit
    run('git checkout -b develop', cwd=PROJECT_DIR, env=git_env)
    with open(f'{PROJECT_DIR}/src/api.js', 'w') as f:
        f.write("""/**
 * API client for fetching dashboard data.
 */

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

export async function fetchDashboardStats() {
  const response = await fetch(`${API_BASE}/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}

export async function fetchAnalyticsData(range = '7d') {
  const response = await fetch(`${API_BASE}/analytics?range=${range}`);
  if (!response.ok) throw new Error('Failed to fetch analytics');
  return response.json();
}
""")
    run('git add -A', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add API client module for dashboard data"', cwd=PROJECT_DIR, env=git_env)

    # Switch back to main
    run('git checkout main', cwd=PROJECT_DIR, env=git_env)

    # Create a bare remote origin
    os.makedirs(BARE_REPO, exist_ok=True)
    run(f'git init --bare', cwd=BARE_REPO, env=git_env)
    run(f'git remote add origin "{BARE_REPO}"', cwd=PROJECT_DIR, env=git_env)

    # Push main and develop to origin
    run('git push origin main', cwd=PROJECT_DIR, env=git_env)
    run('git push origin develop', cwd=PROJECT_DIR, env=git_env)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Bare origin at: {BARE_REPO}')

    # Verify state
    log = run('git log --all --oneline', cwd=PROJECT_DIR, env=git_env)
    print(f'Git log:\n{log}')
    branches = run('git branch -a', cwd=PROJECT_DIR, env=git_env)
    print(f'Branches:\n{branches}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
