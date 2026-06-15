"""
Initial Setup: Configure VSCode workspace settings for ~/project
Task ID: vscode_wf_022
Domain: vscode

Creates a realistic project directory with node_modules/, dist/, .cache/,
and several .js files with corresponding .js.map source maps.
Does NOT create .vscode/settings.json (that is the task).
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_022'
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


def create_initial():
    # Create project root
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- Create package.json ---
    package_json = {
        "name": "analytics-dashboard",
        "version": "2.1.0",
        "description": "Real-time analytics dashboard for sales metrics",
        "main": "src/index.js",
        "scripts": {
            "build": "webpack --mode production",
            "start": "webpack serve --mode development",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "chart.js": "^4.3.0",
            "axios": "^1.6.2",
            "date-fns": "^3.0.6"
        },
        "devDependencies": {
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4",
            "babel-loader": "^9.1.3",
            "@babel/core": "^7.23.7",
            "jest": "^29.7.0",
            "eslint": "^8.56.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- Create src/ directory with JS files and source maps ---
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # index.js
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/main.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # index.js.map
    with open(os.path.join(src_dir, 'index.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "index.js", "sources": ["index.ts"], "mappings": "AAAA,OAAO"}, f)

    # App.js
    with open(os.path.join(src_dir, 'App.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import { fetchSalesData } from './api/salesApi';

function App() {
  const [salesData, setSalesData] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState('monthly');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      const data = await fetchSalesData(selectedPeriod);
      setSalesData(data);
      setIsLoading(false);
    }
    loadData();
  }, [selectedPeriod]);

  return (
    <div className="app-container">
      <Sidebar onPeriodChange={setSelectedPeriod} activePeriod={selectedPeriod} />
      <Dashboard data={salesData} loading={isLoading} period={selectedPeriod} />
    </div>
  );
}

export default App;
""")

    # App.js.map
    with open(os.path.join(src_dir, 'App.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "App.js", "sources": ["App.tsx"], "mappings": "AAAA,OAAO,KAAK"}, f)

    # components directory
    comp_dir = os.path.join(src_dir, 'components')
    os.makedirs(comp_dir, exist_ok=True)

    # Dashboard.js
    with open(os.path.join(comp_dir, 'Dashboard.js'), 'w') as f:
        f.write("""import React from 'react';
import SalesChart from './SalesChart';
import MetricsCard from './MetricsCard';

function Dashboard({ data, loading, period }) {
  if (loading) return <div className="spinner">Loading analytics...</div>;

  const totalRevenue = data.reduce((sum, item) => sum + item.revenue, 0);
  const avgOrderValue = totalRevenue / (data.length || 1);
  const topProduct = data.sort((a, b) => b.revenue - a.revenue)[0];

  return (
    <main className="dashboard">
      <h1>Sales Analytics - {period.charAt(0).toUpperCase() + period.slice(1)}</h1>
      <div className="metrics-grid">
        <MetricsCard title="Total Revenue" value={`$${totalRevenue.toLocaleString()}`} />
        <MetricsCard title="Avg Order Value" value={`$${avgOrderValue.toFixed(2)}`} />
        <MetricsCard title="Top Product" value={topProduct?.name || 'N/A'} />
        <MetricsCard title="Total Orders" value={data.length} />
      </div>
      <SalesChart data={data} period={period} />
    </main>
  );
}

export default Dashboard;
""")

    # Dashboard.js.map
    with open(os.path.join(comp_dir, 'Dashboard.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "Dashboard.js", "sources": ["Dashboard.tsx"], "mappings": "AAAA"}, f)

    # SalesChart.js
    with open(os.path.join(comp_dir, 'SalesChart.js'), 'w') as f:
        f.write("""import React, { useRef, useEffect } from 'react';
import Chart from 'chart.js/auto';

function SalesChart({ data, period }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) chartRef.current.destroy();
    const ctx = canvasRef.current.getContext('2d');
    chartRef.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          label: `Revenue (${period})`,
          data: data.map(d => d.revenue),
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
    return () => chartRef.current?.destroy();
  }, [data, period]);

  return <canvas ref={canvasRef} />;
}

export default SalesChart;
""")

    # SalesChart.js.map
    with open(os.path.join(comp_dir, 'SalesChart.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "SalesChart.js", "sources": ["SalesChart.tsx"], "mappings": "AAAA"}, f)

    # --- Create API directory ---
    api_dir = os.path.join(src_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)

    with open(os.path.join(api_dir, 'salesApi.js'), 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.example.com/v2';

export async function fetchSalesData(period = 'monthly') {
  const response = await axios.get(`${API_BASE}/sales`, {
    params: { period, limit: 50 },
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
  return response.data.results;
}

export async function fetchProductMetrics(productId) {
  const response = await axios.get(`${API_BASE}/products/${productId}/metrics`);
  return response.data;
}

function getToken() {
  return localStorage.getItem('auth_token') || '';
}
""")

    with open(os.path.join(api_dir, 'salesApi.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "salesApi.js", "sources": ["salesApi.ts"], "mappings": "AAAA"}, f)

    # --- Create styles directory ---
    styles_dir = os.path.join(src_dir, 'styles')
    os.makedirs(styles_dir, exist_ok=True)

    with open(os.path.join(styles_dir, 'main.css'), 'w') as f:
        f.write("""/* Analytics Dashboard Styles */
:root {
  --primary-color: #2563eb;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
}

body { margin: 0; font-family: 'Inter', sans-serif; background: var(--bg-color); }
.app-container { display: flex; min-height: 100vh; }
.dashboard { flex: 1; padding: 2rem; }
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin: 1.5rem 0; }
.spinner { display: flex; align-items: center; justify-content: center; height: 100vh; font-size: 1.2rem; color: var(--text-secondary); }
""")

    # --- Create node_modules/ with some realistic content ---
    nm_dir = os.path.join(PROJECT_DIR, 'node_modules')
    os.makedirs(os.path.join(nm_dir, 'react', 'cjs'), exist_ok=True)
    with open(os.path.join(nm_dir, 'react', 'package.json'), 'w') as f:
        json.dump({"name": "react", "version": "18.2.0", "main": "index.js"}, f)
    with open(os.path.join(nm_dir, 'react', 'index.js'), 'w') as f:
        f.write("'use strict';\nmodule.exports = require('./cjs/react.production.min.js');\n")

    os.makedirs(os.path.join(nm_dir, 'axios', 'lib'), exist_ok=True)
    with open(os.path.join(nm_dir, 'axios', 'package.json'), 'w') as f:
        json.dump({"name": "axios", "version": "1.6.2", "main": "index.js"}, f)

    os.makedirs(os.path.join(nm_dir, '.package-lock.json'), exist_ok=True)

    # --- Create dist/ with build artifacts ---
    dist_dir = os.path.join(PROJECT_DIR, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, 'bundle.js'), 'w') as f:
        f.write("// Webpack bundled output - minified\n!function(e,t){\"object\"==typeof exports}();\n")
    with open(os.path.join(dist_dir, 'bundle.js.map'), 'w') as f:
        json.dump({"version": 3, "file": "bundle.js", "sources": [], "mappings": ""}, f)
    with open(os.path.join(dist_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html><html><head><title>Analytics</title></head><body><div id="root"></div><script src="bundle.js"></script></body></html>\n')

    # --- Create .cache/ directory ---
    cache_dir = os.path.join(PROJECT_DIR, '.cache')
    os.makedirs(os.path.join(cache_dir, 'babel-loader'), exist_ok=True)
    with open(os.path.join(cache_dir, 'babel-loader', 'cache-main.json'), 'w') as f:
        json.dump({"version": "9.1.3", "entries": {}, "last_build": "2025-12-15T10:30:00Z"}, f)
    with open(os.path.join(cache_dir, '.eslintcache'), 'w') as f:
        f.write('[]\n')

    # --- Create config files at project root ---
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("node_modules/\ndist/\n.cache/\n*.js.map\n.env\n")

    with open(os.path.join(PROJECT_DIR, 'webpack.config.js'), 'w') as f:
        f.write("""const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true,
  },
  module: {
    rules: [
      { test: /\\.jsx?$/, exclude: /node_modules/, use: 'babel-loader' },
      { test: /\\.css$/, use: ['style-loader', 'css-loader'] },
    ],
  },
  plugins: [new HtmlWebpackPlugin({ template: './public/index.html' })],
  devtool: 'source-map',
};
""")

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Analytics Dashboard

Real-time sales analytics dashboard built with React and Chart.js.

## Quick Start

```bash
npm install
npm start
```

## Build

```bash
npm run build
```

Output goes to `dist/` directory.
""")

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
