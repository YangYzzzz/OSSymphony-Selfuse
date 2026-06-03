"""
Initial Setup: Configure VSCode file watcher exclusion patterns
Task ID: vscode_lp_069
Domain: vs_code

Creates a realistic JavaScript project workspace and opens VSCode.
No files.watcherExclude configuration exists in settings.json.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_069'
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


def create_project_structure():
    """Create a realistic large JavaScript project."""
    # Main project directories
    dirs = [
        f'{WORKSPACE}/src/components',
        f'{WORKSPACE}/src/utils',
        f'{WORKSPACE}/src/services',
        f'{WORKSPACE}/src/styles',
        f'{WORKSPACE}/src/hooks',
        f'{WORKSPACE}/node_modules/react/lib',
        f'{WORKSPACE}/node_modules/lodash',
        f'{WORKSPACE}/node_modules/axios/dist',
        f'{WORKSPACE}/node_modules/webpack/lib',
        f'{WORKSPACE}/.git/objects',
        f'{WORKSPACE}/.git/refs/heads',
        f'{WORKSPACE}/build/static/js',
        f'{WORKSPACE}/build/static/css',
        f'{WORKSPACE}/public',
        f'{WORKSPACE}/tests',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "crm-dashboard",
        "version": "2.4.1",
        "description": "Customer Relationship Management Dashboard for Meridian Corp",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "jest --coverage",
            "lint": "eslint src/ --ext .js,.jsx"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "axios": "^1.3.4",
            "lodash": "^4.17.21",
            "chart.js": "^4.2.1",
            "date-fns": "^2.29.3"
        },
        "devDependencies": {
            "jest": "^29.4.3",
            "eslint": "^8.35.0",
            "webpack": "^5.75.0",
            "prettier": "^2.8.4"
        }
    }
    with open(f'{WORKSPACE}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    with open(f'{WORKSPACE}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.js
    with open(f'{WORKSPACE}/src/App.js', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CustomerList from './components/CustomerList';
import Analytics from './components/Analytics';
import Navigation from './components/Navigation';

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/customers" element={<CustomerList />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.jsx
    with open(f'{WORKSPACE}/src/components/Dashboard.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchMetrics } from '../services/api';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import MetricCard from './MetricCard';
import RevenueChart from './RevenueChart';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('30d');

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        setLoading(true);
        const data = await fetchMetrics(dateRange);
        setMetrics(data);
      } catch (error) {
        console.error('Failed to load dashboard metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMetrics();
  }, [dateRange]);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Meridian Corp - CRM Dashboard</h1>
      <div className="metrics-grid">
        <MetricCard title="Total Revenue" value={formatCurrency(metrics.revenue)} />
        <MetricCard title="Active Customers" value={metrics.activeCustomers} />
        <MetricCard title="Conversion Rate" value={formatPercentage(metrics.conversionRate)} />
        <MetricCard title="Avg Deal Size" value={formatCurrency(metrics.avgDealSize)} />
      </div>
      <RevenueChart data={metrics.revenueHistory} />
    </div>
  );
};

export default Dashboard;
""")

    # src/components/CustomerList.jsx
    with open(f'{WORKSPACE}/src/components/CustomerList.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchCustomers } from '../services/api';
import { debounce } from 'lodash';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('name');

  useEffect(() => {
    fetchCustomers().then(setCustomers);
  }, []);

  const debouncedSearch = debounce((term) => setSearchTerm(term), 300);

  const filtered = customers
    .filter(c => c.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => a[sortField] > b[sortField] ? 1 : -1);

  return (
    <div className="customer-list">
      <h2>Customer Directory</h2>
      <input placeholder="Search customers..." onChange={e => debouncedSearch(e.target.value)} />
      <table>
        <thead>
          <tr>
            <th onClick={() => setSortField('name')}>Name</th>
            <th onClick={() => setSortField('company')}>Company</th>
            <th onClick={() => setSortField('revenue')}>Revenue</th>
            <th onClick={() => setSortField('status')}>Status</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(customer => (
            <tr key={customer.id}>
              <td>{customer.name}</td>
              <td>{customer.company}</td>
              <td>${customer.revenue.toLocaleString()}</td>
              <td><span className={`badge ${customer.status}`}>{customer.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerList;
""")

    # src/services/api.js
    with open(f'{WORKSPACE}/src/services/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.meridian-crm.internal';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

client.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const fetchMetrics = (range) => client.get(`/metrics?range=${range}`).then(r => r.data);
export const fetchCustomers = () => client.get('/customers').then(r => r.data);
export const updateCustomer = (id, data) => client.put(`/customers/${id}`, data).then(r => r.data);
export const fetchAnalytics = (params) => client.get('/analytics', { params }).then(r => r.data);
""")

    # src/utils/formatters.js
    with open(f'{WORKSPACE}/src/utils/formatters.js', 'w') as f:
        f.write("""export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

export const formatPercentage = (value) => {
  return `${(value * 100).toFixed(1)}%`;
};

export const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

export const truncateText = (text, maxLength = 50) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};
""")

    # src/hooks/useAuth.js
    with open(f'{WORKSPACE}/src/hooks/useAuth.js', 'w') as f:
        f.write("""import { useState, useEffect, createContext, useContext } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Validate token and fetch user profile
      fetch('/api/me', { headers: { Authorization: `Bearer ${token}` } })
        .then(r => r.json())
        .then(setUser)
        .catch(() => localStorage.removeItem('auth_token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    localStorage.setItem('auth_token', data.token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""")

    # src/styles/global.css
    with open(f'{WORKSPACE}/src/styles/global.css', 'w') as f:
        f.write("""* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f7fa;
  color: #2d3748;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard { padding: 20px; }
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 24px 0;
}

.customer-list table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.customer-list th, .customer-list td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85em;
}

.badge.active { background: #c6f6d5; color: #22543d; }
.badge.churned { background: #fed7d7; color: #742a2a; }
.badge.prospect { background: #bee3f8; color: #2a4365; }
""")

    # Fake node_modules content (a few representative files)
    with open(f'{WORKSPACE}/node_modules/react/lib/index.js', 'w') as f:
        f.write('// React library core\nmodule.exports = require("./react.production.min.js");\n')
    with open(f'{WORKSPACE}/node_modules/lodash/index.js', 'w') as f:
        f.write('// Lodash utility library\nmodule.exports = require("./lodash.js");\n')
    with open(f'{WORKSPACE}/node_modules/axios/dist/axios.min.js', 'w') as f:
        f.write('// Axios HTTP client - minified\n')

    # Fake .git content
    with open(f'{WORKSPACE}/.git/HEAD', 'w') as f:
        f.write('ref: refs/heads/main\n')
    with open(f'{WORKSPACE}/.git/config', 'w') as f:
        f.write('[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n')
    with open(f'{WORKSPACE}/.git/refs/heads/main', 'w') as f:
        f.write('a3f5c8d2e1b4f6a7c9d0e2f3a5b7c8d1e4f6a8b0\n')

    # Build output files
    with open(f'{WORKSPACE}/build/static/js/main.chunk.js', 'w') as f:
        f.write('// Compiled JavaScript bundle\n(function(){/* minified */})();\n')
    with open(f'{WORKSPACE}/build/static/css/main.css', 'w') as f:
        f.write('/* Compiled CSS */\nbody{font-family:Inter,sans-serif}\n')
    with open(f'{WORKSPACE}/build/index.html', 'w') as f:
        f.write('<!DOCTYPE html><html><head><title>CRM Dashboard</title></head><body><div id="root"></div></body></html>\n')

    # tests/
    with open(f'{WORKSPACE}/tests/Dashboard.test.js', 'w') as f:
        f.write("""import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '../src/components/Dashboard';
import { fetchMetrics } from '../src/services/api';

jest.mock('../src/services/api');

describe('Dashboard', () => {
  it('renders metric cards after loading', async () => {
    fetchMetrics.mockResolvedValue({
      revenue: 1250000,
      activeCustomers: 847,
      conversionRate: 0.234,
      avgDealSize: 15600,
      revenueHistory: []
    });

    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('Total Revenue')).toBeInTheDocument();
      expect(screen.getByText('$1,250,000')).toBeInTheDocument();
    });
  });
});
""")

    # .eslintrc.json
    with open(f'{WORKSPACE}/.eslintrc.json', 'w') as f:
        json.dump({
            "env": {"browser": True, "es2021": True, "jest": True},
            "extends": ["eslint:recommended", "plugin:react/recommended"],
            "parserOptions": {"ecmaVersion": "latest", "sourceType": "module"},
            "rules": {"no-unused-vars": "warn", "react/prop-types": "off"}
        }, f, indent=2)

    # README.md
    with open(f'{WORKSPACE}/README.md', 'w') as f:
        f.write("""# Meridian Corp CRM Dashboard

Internal customer relationship management tool for the sales and marketing teams.

## Getting Started

```bash
npm install
npm start
```

## Architecture

- `src/components/` - React UI components
- `src/services/` - API client layer
- `src/utils/` - Shared utility functions
- `src/hooks/` - Custom React hooks
- `tests/` - Jest test suites

## Team

- Lead: Elena Rodriguez (elena.r@meridian.com)
- Frontend: James Park, Aisha Patel
- Backend API: Carlos Mendez, Priya Singh
""")

    print(f'Project structure created at {WORKSPACE}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT files.watcherExclude."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Merge in baseline settings (no files.watcherExclude!)
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "editor.formatOnSave": True,
        "workbench.colorTheme": "Default Dark Modern",
        "terminal.integrated.fontSize": 13,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    # Ensure files.watcherExclude is NOT present
    settings.pop("files.watcherExclude", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings created at {SETTINGS_PATH} (no watcherExclude)')


def main():
    create_project_structure()
    setup_vscode_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
