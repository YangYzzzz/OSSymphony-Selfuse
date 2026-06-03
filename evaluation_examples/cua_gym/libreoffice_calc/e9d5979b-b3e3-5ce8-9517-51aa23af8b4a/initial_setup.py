"""
Initial Setup: VSCode rename symbol - React component App -> MainApplication
Task ID: vscode_wf_033
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_033'
PROJECT_DIR = f'{WORKDIR}/project'
SRC_DIR = f'{PROJECT_DIR}/src'
COMPONENTS_DIR = f'{SRC_DIR}/components'


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
    os.makedirs(COMPONENTS_DIR, exist_ok=True)

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
  "name": "inventory-dashboard",
  "version": "2.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "axios": "^1.6.2"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
''')

    # --- src/components/App.jsx ---
    # Exports the 'App' component (pre-rename state)
    with open(f'{COMPONENTS_DIR}/App.jsx', 'w') as f:
        f.write('''import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * App component - Main application entry point for the Inventory Dashboard.
 * Manages global state and renders the primary layout.
 */
function App() {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const response = await axios.get('/api/inventory');
        setInventory(response.data);
      } catch (err) {
        setError('Failed to load inventory data');
        console.error('Inventory fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchInventory();
  }, []);

  if (loading) {
    return <div className="loading-spinner">Loading inventory...</div>;
  }

  if (error) {
    return <div className="error-banner">{error}</div>;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Inventory Dashboard</h1>
        <span className="item-count">{inventory.length} items tracked</span>
      </header>
      <main className="app-content">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>SKU</th>
              <th>Product</th>
              <th>Quantity</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((item) => (
              <tr key={item.sku}>
                <td>{item.sku}</td>
                <td>{item.name}</td>
                <td>{item.quantity}</td>
                <td>{item.warehouse}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}

export default App;
''')

    # --- src/index.jsx ---
    # Imports App from './components/App'
    with open(f'{SRC_DIR}/index.jsx', 'w') as f:
        f.write('''import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './components/App';
import './styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
''')

    # --- src/routes.jsx ---
    # Imports App from './components/App'
    with open(f'{SRC_DIR}/routes.jsx', 'w') as f:
        f.write('''import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import App from './components/App';

/**
 * Application route definitions.
 * Maps URL paths to their corresponding page components.
 */
const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/dashboard" element={<App />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
''')

    # --- src/styles/global.css ---
    os.makedirs(f'{SRC_DIR}/styles', exist_ok=True)
    with open(f'{SRC_DIR}/styles/global.css', 'w') as f:
        f.write('''/* Inventory Dashboard - Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f6f9;
  color: #333;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e0e4e8;
}

.inventory-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th,
.inventory-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e0e4e8;
}

.inventory-table th {
  background-color: #2c3e50;
  color: white;
  font-weight: 600;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #7f8c8d;
}

.error-banner {
  padding: 16px;
  background-color: #e74c3c;
  color: white;
  border-radius: 4px;
  margin: 24px;
}
''')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: App.jsx, index.jsx, routes.jsx, package.json, global.css')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open App.jsx specifically so the agent can see the target file
    launch_gui(f'code "{COMPONENTS_DIR}/App.jsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
