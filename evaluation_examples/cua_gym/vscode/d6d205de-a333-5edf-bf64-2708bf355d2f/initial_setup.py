"""
Initial Setup: Create a webapp project structure with dist/, coverage/, src/generated/,
and node_modules/ directories but no .prettierignore or .eslintignore files.
Task ID: vscode_web_047
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_047'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # Create project root
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- package.json ---
    create_file(f'{PROJECT_DIR}/package.json', """{
  "name": "webapp",
  "version": "2.1.0",
  "description": "Internal dashboard for sales analytics",
  "main": "src/index.js",
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack serve --mode development",
    "lint": "eslint src/",
    "format": "prettier --write 'src/**/*.{js,jsx,css,json}'",
    "test": "jest --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "chart.js": "^4.4.1",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "prettier": "^3.1.0",
    "eslint": "^8.56.0",
    "webpack": "^5.89.0",
    "jest": "^29.7.0"
  }
}
""")

    # --- .prettierrc ---
    create_file(f'{PROJECT_DIR}/.prettierrc', """{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
""")

    # --- .eslintrc.json ---
    create_file(f'{PROJECT_DIR}/.eslintrc.json', """{
  "env": {
    "browser": true,
    "es2021": true,
    "jest": true
  },
  "extends": ["eslint:recommended"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off",
    "indent": ["error", 2],
    "quotes": ["error", "single"]
  }
}
""")

    # --- Source files ---
    create_file(f'{PROJECT_DIR}/src/index.js', """import React from 'react';
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

    create_file(f'{PROJECT_DIR}/src/App.jsx', """import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import { fetchSalesData } from './api/salesApi';

function App() {
  const [salesData, setSalesData] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        const data = await fetchSalesData(selectedRegion);
        setSalesData(data);
      } catch (error) {
        console.error('Failed to fetch sales data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [selectedRegion]);

  return (
    <div className="app-container">
      <Sidebar
        selectedRegion={selectedRegion}
        onRegionChange={setSelectedRegion}
      />
      <Dashboard
        data={salesData}
        isLoading={isLoading}
        region={selectedRegion}
      />
    </div>
  );
}

export default App;
""")

    create_file(f'{PROJECT_DIR}/src/components/Dashboard.jsx', """import React from 'react';
import SalesChart from './SalesChart';
import MetricCard from './MetricCard';

function Dashboard({ data, isLoading, region }) {
  if (isLoading) {
    return <div className="loading-spinner">Loading analytics...</div>;
  }

  const totalRevenue = data.reduce((sum, item) => sum + item.revenue, 0);
  const avgOrderValue = totalRevenue / (data.length || 1);
  const topPerformer = data.sort((a, b) => b.revenue - a.revenue)[0];

  return (
    <main className="dashboard">
      <h1>Sales Analytics — {region === 'all' ? 'All Regions' : region}</h1>
      <div className="metrics-grid">
        <MetricCard title="Total Revenue" value={`$${totalRevenue.toLocaleString()}`} />
        <MetricCard title="Avg Order Value" value={`$${avgOrderValue.toFixed(2)}`} />
        <MetricCard title="Top Performer" value={topPerformer?.name || 'N/A'} />
        <MetricCard title="Total Orders" value={data.length} />
      </div>
      <SalesChart data={data} />
    </main>
  );
}

export default Dashboard;
""")

    create_file(f'{PROJECT_DIR}/src/components/Sidebar.jsx', """import React from 'react';

const REGIONS = ['all', 'North America', 'Europe', 'Asia Pacific', 'Latin America'];

function Sidebar({ selectedRegion, onRegionChange }) {
  return (
    <nav className="sidebar">
      <div className="logo">
        <h2>SalesView</h2>
        <span className="version">v2.1</span>
      </div>
      <ul className="nav-list">
        {REGIONS.map((region) => (
          <li
            key={region}
            className={`nav-item ${selectedRegion === region ? 'active' : ''}`}
            onClick={() => onRegionChange(region)}
          >
            {region === 'all' ? 'All Regions' : region}
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Sidebar;
""")

    create_file(f'{PROJECT_DIR}/src/components/SalesChart.jsx', """import React, { useRef, useEffect } from 'react';
import Chart from 'chart.js/auto';

function SalesChart({ data }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map((item) => item.name),
        datasets: [
          {
            label: 'Revenue ($)',
            data: data.map((item) => item.revenue),
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Revenue by Sales Rep' },
        },
      },
    });

    return () => {
      if (chartInstance.current) chartInstance.current.destroy();
    };
  }, [data]);

  return <canvas ref={chartRef} />;
}

export default SalesChart;
""")

    create_file(f'{PROJECT_DIR}/src/components/MetricCard.jsx', """import React from 'react';

function MetricCard({ title, value }) {
  return (
    <div className="metric-card">
      <h3 className="metric-title">{title}</h3>
      <p className="metric-value">{value}</p>
    </div>
  );
}

export default MetricCard;
""")

    create_file(f'{PROJECT_DIR}/src/api/salesApi.js', """import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.salesview.internal';

export async function fetchSalesData(region = 'all') {
  const params = region !== 'all' ? { region } : {};
  const response = await axios.get(`${API_BASE}/sales`, { params });
  return response.data;
}

export async function fetchRegionSummary(region) {
  const response = await axios.get(`${API_BASE}/sales/summary/${region}`);
  return response.data;
}
""")

    create_file(f'{PROJECT_DIR}/src/styles/main.css', """* {
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
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: #1e293b;
  color: white;
  padding: 20px;
}

.logo h2 {
  font-size: 1.4rem;
}

.logo .version {
  font-size: 0.75rem;
  opacity: 0.6;
}

.nav-list {
  list-style: none;
  margin-top: 30px;
}

.nav-item {
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 6px;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: #3b82f6;
}

.dashboard {
  flex: 1;
  padding: 30px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 20px 0;
}

.metric-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.metric-title {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #1e293b;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #6b7280;
}
""")

    # --- dist/ (build output) ---
    create_file(f'{PROJECT_DIR}/dist/bundle.js', """// Webpack bundled output — auto-generated
!function(e,t){"use strict";var n=function(){return React.createElement("div",null,"SalesView Dashboard")};ReactDOM.createRoot(document.getElementById("root")).render(React.createElement(n))}();
//# sourceMappingURL=bundle.js.map
""")

    create_file(f'{PROJECT_DIR}/dist/bundle.js.map', '{"version":3,"file":"bundle.js","sources":["../src/index.js"],"mappings":"AAAA"}')

    create_file(f'{PROJECT_DIR}/dist/index.html', """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>SalesView</title></head>
<body><div id="root"></div><script src="bundle.js"></script></body>
</html>
""")

    create_file(f'{PROJECT_DIR}/dist/styles.css', """*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f4f6f9}
""")

    # --- coverage/ (test coverage reports) ---
    create_file(f'{PROJECT_DIR}/coverage/lcov.info', """TN:
SF:src/App.jsx
FN:8,App
FNDA:3,App
FNF:1
FNH:1
DA:9,3
DA:10,3
DA:11,3
DA:15,3
DA:22,2
LF:5
LH:5
BRF:2
BRH:2
end_of_record
SF:src/components/Dashboard.jsx
FN:4,Dashboard
FNDA:5,Dashboard
FNF:1
FNH:1
DA:5,5
DA:8,5
DA:9,5
LF:3
LH:3
end_of_record
""")

    create_file(f'{PROJECT_DIR}/coverage/coverage-summary.json', """{
  "total": {
    "lines": {"total": 142, "covered": 128, "pct": 90.14},
    "statements": {"total": 156, "covered": 141, "pct": 90.38},
    "functions": {"total": 18, "covered": 16, "pct": 88.89},
    "branches": {"total": 24, "covered": 20, "pct": 83.33}
  }
}
""")

    create_file(f'{PROJECT_DIR}/coverage/lcov-report/index.html', """<!DOCTYPE html>
<html><head><title>Code Coverage Report</title></head>
<body><h1>Coverage Report — webapp</h1><p>Generated: 2025-11-20T14:30:00Z</p>
<table><tr><th>File</th><th>Lines</th><th>Branches</th></tr>
<tr><td>src/App.jsx</td><td>100%</td><td>100%</td></tr>
<tr><td>src/components/Dashboard.jsx</td><td>92%</td><td>85%</td></tr>
</table></body></html>
""")

    # --- src/generated/ (auto-generated files) ---
    create_file(f'{PROJECT_DIR}/src/generated/apiTypes.js', """// AUTO-GENERATED — DO NOT EDIT
// Generated from OpenAPI spec on 2025-11-15

/**
 * @typedef {Object} SalesRecord
 * @property {string} id
 * @property {string} name
 * @property {string} region
 * @property {number} revenue
 * @property {number} orderCount
 * @property {string} lastUpdated
 */

/**
 * @typedef {Object} RegionSummary
 * @property {string} region
 * @property {number} totalRevenue
 * @property {number} totalOrders
 * @property {number} avgOrderValue
 */

export const API_VERSION = '2.1.0';
export const ENDPOINTS = {
  sales: '/sales',
  summary: '/sales/summary',
  regions: '/regions',
};
""")

    create_file(f'{PROJECT_DIR}/src/generated/routeMap.js', """// AUTO-GENERATED from router config — DO NOT EDIT
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  SALES_DETAIL: '/sales/:id',
  REGION_VIEW: '/region/:regionName',
  SETTINGS: '/settings',
  EXPORT: '/export',
};
""")

    # --- node_modules/ (simulated, a few marker files) ---
    create_file(f'{PROJECT_DIR}/node_modules/.package-lock.json', '{"lockfileVersion": 3}')
    create_file(f'{PROJECT_DIR}/node_modules/react/index.js', "'use strict'; module.exports = require('./cjs/react.production.min.js');")
    create_file(f'{PROJECT_DIR}/node_modules/prettier/index.js', "'use strict'; module.exports = require('./src/index.js');")

    # --- Other project files ---
    create_file(f'{PROJECT_DIR}/webpack.config.js', """const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\\.jsx?$/,
        exclude: /node_modules/,
        use: { loader: 'babel-loader' },
      },
      {
        test: /\\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
""")

    create_file(f'{PROJECT_DIR}/README.md', """# SalesView Web App

Internal dashboard for tracking sales analytics across regions.

## Getting Started

```bash
npm install
npm run dev
```

## Scripts

- `npm run build` — Production build
- `npm run dev` — Development server
- `npm run lint` — Run ESLint
- `npm run format` — Run Prettier
- `npm run test` — Run tests with coverage
""")

    create_file(f'{PROJECT_DIR}/.gitignore', """node_modules/
dist/
coverage/
.env
""")

    # DO NOT create .prettierignore or .eslintignore — the task is to create them
    print(f'Initial project structure created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the webapp folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
