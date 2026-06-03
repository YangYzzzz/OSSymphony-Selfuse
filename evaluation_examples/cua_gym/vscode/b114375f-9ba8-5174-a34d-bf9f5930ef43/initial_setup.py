"""
Initial Setup: VSCode with a JavaScript project using path aliases.
Task ID: vscode_we_082
Domain: vscode

Creates a JS project workspace with src/ directory structure that uses
@ path aliases. VSCode opens with empty user settings and no
Path Intellisense extension installed.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_082'
WORKSPACE = f'{WORKDIR}/workspace'
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


def create_project():
    """Create a realistic JavaScript project with path aliases."""
    # Directory structure
    dirs = [
        f'{WORKSPACE}/src/components',
        f'{WORKSPACE}/src/utils',
        f'{WORKSPACE}/src/services',
        f'{WORKSPACE}/src/styles',
        f'{WORKSPACE}/node_modules/.package-lock',
        f'{WORKSPACE}/public',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.2.0",
        "description": "Warehouse inventory tracking dashboard",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "react-scripts": "5.0.1"
        }
    }
    with open(f'{WORKSPACE}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # jsconfig.json with @ alias (project already uses aliases)
    jsconfig = {
        "compilerOptions": {
            "baseUrl": ".",
            "paths": {
                "@/*": ["src/*"]
            }
        },
        "include": ["src"]
    }
    with open(f'{WORKSPACE}/jsconfig.json', 'w') as f:
        json.dump(jsconfig, f, indent=2)

    # src/index.js
    with open(f'{WORKSPACE}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '@/components/App';
import '@/styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/components/App.js
    with open(f'{WORKSPACE}/src/components/App.js', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from '@/components/Dashboard';
import InventoryList from '@/components/InventoryList';
import { formatCurrency } from '@/utils/format';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <h1>Warehouse Inventory Dashboard</h1>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inventory" element={<InventoryList />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.js
    with open(f'{WORKSPACE}/src/components/Dashboard.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchInventorySummary } from '@/services/api';
import { formatCurrency, formatDate } from '@/utils/format';

function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetchInventorySummary().then(data => setSummary(data));
  }, []);

  if (!summary) return <div>Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <div className="metric-card">
        <h3>Total Items</h3>
        <span>{summary.totalItems}</span>
      </div>
      <div className="metric-card">
        <h3>Total Value</h3>
        <span>{formatCurrency(summary.totalValue)}</span>
      </div>
      <div className="metric-card">
        <h3>Last Updated</h3>
        <span>{formatDate(summary.lastUpdated)}</span>
      </div>
    </div>
  );
}

export default Dashboard;
""")

    # src/components/InventoryList.js
    with open(f'{WORKSPACE}/src/components/InventoryList.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchInventoryItems } from '@/services/api';
import { formatCurrency } from '@/utils/format';

function InventoryList() {
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchInventoryItems().then(data => setItems(data));
  }, []);

  const filtered = items.filter(item =>
    item.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="inventory-list">
      <input
        type="text"
        placeholder="Search items..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Quantity</th>
            <th>Unit Price</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.sku}>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.quantity}</td>
              <td>{formatCurrency(item.unitPrice)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default InventoryList;
""")

    # src/services/api.js
    with open(f'{WORKSPACE}/src/services/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001';

export async function fetchInventorySummary() {
  const response = await axios.get(`${API_BASE}/api/summary`);
  return response.data;
}

export async function fetchInventoryItems() {
  const response = await axios.get(`${API_BASE}/api/items`);
  return response.data;
}

export async function updateItemQuantity(sku, newQuantity) {
  const response = await axios.patch(`${API_BASE}/api/items/${sku}`, {
    quantity: newQuantity
  });
  return response.data;
}
""")

    # src/utils/format.js
    with open(f'{WORKSPACE}/src/utils/format.js', 'w') as f:
        f.write("""export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function formatPercentage(value) {
  return `${(value * 100).toFixed(1)}%`;
}
""")

    # src/styles/global.css
    with open(f'{WORKSPACE}/src/styles/global.css', 'w') as f:
        f.write("""* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #2d3748;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.inventory-list table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.inventory-list th,
.inventory-list td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
""")

    # public/index.html
    with open(f'{WORKSPACE}/public/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Inventory Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # .gitignore
    with open(f'{WORKSPACE}/.gitignore', 'w') as f:
        f.write("""node_modules/
build/
.env
.DS_Store
""")

    print(f'Project created at: {WORKSPACE}')


def setup_vscode_settings():
    """Ensure VSCode user settings are empty (as per initial state)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json created at: {SETTINGS_PATH}')


def ensure_extension_not_installed():
    """Make sure path-intellisense is NOT installed in initial env."""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'christian-kohler.path-intellisense' in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', 'christian-kohler.path-intellisense'],
                capture_output=True, text=True, timeout=60
            )
            print('Uninstalled path-intellisense from initial env')
        else:
            print('path-intellisense not installed (good)')
    except Exception as e:
        print(f'Extension check note: {e}')


def main():
    create_project()
    setup_vscode_settings()
    ensure_extension_not_installed()

    # Launch VSCode with workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace on DISPLAY=:0')


main()
