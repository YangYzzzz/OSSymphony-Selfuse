"""
Initial Setup: Configure VSCode path aliases for React project
Task ID: vscode_gf2_026
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_026'
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
    dirs = [
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/utils',
        f'{PROJECT_DIR}/src/pages',
        f'{PROJECT_DIR}/src/hooks',
        f'{PROJECT_DIR}/src/assets',
        f'{PROJECT_DIR}/public',
        f'{PROJECT_DIR}/node_modules/.cache',
        f'{PROJECT_DIR}/.vscode',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "description": "Customer analytics dashboard for Meridian Corp",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "recharts": "^2.10.3",
            "date-fns": "^3.0.6"
        },
        "devDependencies": {
            "@testing-library/react": "^14.1.2",
            "@testing-library/jest-dom": "^6.1.4",
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
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # .vscode/settings.json — basic settings, NO importModuleSpecifier
    vscode_settings = {
        "editor.formatOnSave": True,
        "editor.tabSize": 2,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # src/index.js
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

    # src/App.js — uses long relative imports (this is the pain point)
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CustomerList from './pages/CustomerList';
import { formatCurrency, calculateGrowth } from './utils/formatters';
import { useAuth } from './hooks/useAuth';
import './App.css';

function App() {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <div className="login-prompt">Please log in to continue</div>;
  }

  return (
    <BrowserRouter>
      <div className="app-container">
        <Header user={user} />
        <div className="main-layout">
          <Sidebar />
          <main className="content-area">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/customers" element={<CustomerList />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Header.js
    with open(f'{PROJECT_DIR}/src/components/Header.js', 'w') as f:
        f.write("""import React from 'react';
import { formatDate } from '../utils/formatters';

function Header({ user }) {
  return (
    <header className="app-header">
      <div className="logo">
        <h1>Meridian Analytics</h1>
      </div>
      <div className="header-right">
        <span className="current-date">{formatDate(new Date())}</span>
        <div className="user-info">
          <span>{user?.name || 'Guest'}</span>
          <img src={user?.avatar} alt="avatar" className="avatar" />
        </div>
      </div>
    </header>
  );
}

export default Header;
""")

    # src/components/Sidebar.js
    with open(f'{PROJECT_DIR}/src/components/Sidebar.js', 'w') as f:
        f.write("""import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard', icon: 'chart-bar' },
  { path: '/customers', label: 'Customers', icon: 'users' },
  { path: '/reports', label: 'Reports', icon: 'file-text' },
  { path: '/settings', label: 'Settings', icon: 'cog' },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav>
        <ul className="nav-list">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink to={item.path} className="nav-link">
                <i className={`icon-${item.icon}`} />
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
""")

    # src/components/MetricCard.js
    with open(f'{PROJECT_DIR}/src/components/MetricCard.js', 'w') as f:
        f.write("""import React from 'react';
import { formatCurrency, formatPercent } from '../utils/formatters';

function MetricCard({ title, value, change, isCurrency }) {
  const formattedValue = isCurrency ? formatCurrency(value) : value;
  const changeClass = change >= 0 ? 'positive' : 'negative';

  return (
    <div className="metric-card">
      <h3 className="metric-title">{title}</h3>
      <p className="metric-value">{formattedValue}</p>
      <span className={`metric-change ${changeClass}`}>
        {change >= 0 ? '+' : ''}{formatPercent(change)}
      </span>
    </div>
  );
}

export default MetricCard;
""")

    # src/components/DataTable.js
    with open(f'{PROJECT_DIR}/src/components/DataTable.js', 'w') as f:
        f.write("""import React, { useState } from 'react';

function DataTable({ columns, data, onSort }) {
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');

  const handleSort = (column) => {
    const newDirection = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
    setSortColumn(column);
    setSortDirection(newDirection);
    onSort?.(column, newDirection);
  };

  return (
    <table className="data-table">
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} onClick={() => handleSort(col.key)}>
              {col.label}
              {sortColumn === col.key && (
                <span className="sort-indicator">
                  {sortDirection === 'asc' ? ' ▲' : ' ▼'}
                </span>
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {columns.map((col) => (
              <td key={col.key}>{row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DataTable;
""")

    # src/utils/formatters.js
    with open(f'{PROJECT_DIR}/src/utils/formatters.js', 'w') as f:
        f.write("""import { format, parseISO, differenceInDays } from 'date-fns';

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
  }).format(amount);
}

export function formatPercent(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value / 100);
}

export function formatDate(date) {
  if (typeof date === 'string') {
    date = parseISO(date);
  }
  return format(date, 'MMM dd, yyyy');
}

export function formatRelativeDate(dateStr) {
  const date = parseISO(dateStr);
  const days = differenceInDays(new Date(), date);
  if (days === 0) return 'Today';
  if (days === 1) return 'Yesterday';
  if (days < 7) return `${days} days ago`;
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`;
  return formatDate(dateStr);
}
""")

    # src/utils/api.js
    with open(f'{PROJECT_DIR}/src/utils/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.meridian-corp.com/v2';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const fetchCustomers = (params) => client.get('/customers', { params });
export const fetchDashboardMetrics = () => client.get('/dashboard/metrics');
export const fetchRevenueChart = (period) => client.get(`/analytics/revenue?period=${period}`);
export const updateCustomer = (id, data) => client.put(`/customers/${id}`, data);
""")

    # src/hooks/useAuth.js
    with open(f'{PROJECT_DIR}/src/hooks/useAuth.js', 'w') as f:
        f.write("""import { useState, useEffect } from 'react';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setUser({
        name: 'Sarah Chen',
        email: 'sarah.chen@meridian-corp.com',
        role: 'analyst',
        avatar: '/avatars/sarah.png',
      });
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    // Authentication logic would go here
    localStorage.setItem('auth_token', 'mock-jwt-token');
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    setIsAuthenticated(false);
  };

  return { user, isAuthenticated, loading, login, logout };
}
""")

    # src/pages/Dashboard.js
    with open(f'{PROJECT_DIR}/src/pages/Dashboard.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import MetricCard from '../components/MetricCard';
import { fetchDashboardMetrics } from '../utils/api';
import { formatCurrency } from '../utils/formatters';

function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-spinner">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h2>Analytics Overview</h2>
      <div className="metrics-grid">
        <MetricCard title="Total Revenue" value={metrics?.revenue || 0} change={12.5} isCurrency />
        <MetricCard title="Active Customers" value={metrics?.activeCustomers || 0} change={8.3} />
        <MetricCard title="Avg. Order Value" value={metrics?.avgOrderValue || 0} change={-2.1} isCurrency />
        <MetricCard title="Conversion Rate" value={`${metrics?.conversionRate || 0}%`} change={3.7} />
      </div>
    </div>
  );
}

export default Dashboard;
""")

    # src/pages/CustomerList.js
    with open(f'{PROJECT_DIR}/src/pages/CustomerList.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import DataTable from '../components/DataTable';
import { fetchCustomers } from '../utils/api';
import { formatCurrency, formatRelativeDate } from '../utils/formatters';

const columns = [
  { key: 'name', label: 'Customer Name' },
  { key: 'email', label: 'Email' },
  { key: 'totalSpent', label: 'Total Spent' },
  { key: 'lastOrder', label: 'Last Order' },
  { key: 'status', label: 'Status' },
];

function CustomerList() {
  const [customers, setCustomers] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchCustomers({ page, limit: 25 })
      .then(setCustomers)
      .catch(console.error);
  }, [page]);

  return (
    <div className="customer-list">
      <h2>Customer Management</h2>
      <DataTable columns={columns} data={customers} />
      <div className="pagination">
        <button onClick={() => setPage(p => Math.max(1, p - 1))}>Previous</button>
        <span>Page {page}</span>
        <button onClick={() => setPage(p => p + 1)}>Next</button>
      </div>
    </div>
  );
}

export default CustomerList;
""")

    # src/App.css
    with open(f'{PROJECT_DIR}/src/App.css', 'w') as f:
        f.write(""".app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-layout {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 240px;
  background: #1a1a2e;
  color: #e0e0e0;
}

.content-area {
  flex: 1;
  padding: 24px;
  background: #f5f5f5;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
""")

    # src/index.css
    with open(f'{PROJECT_DIR}/src/index.css', 'w') as f:
        f.write("""body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}
""")

    # public/index.html
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Meridian Analytics</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
build/
.env
.env.local
.DS_Store
*.log
""")

    # NO jsconfig.json — this is what the task asks to create
    # NO importModuleSpecifier settings in .vscode/settings.json

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files created:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip node_modules
        if 'node_modules' in root:
            continue
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    # Also open the .vscode/settings.json for easier access
    launch_gui(f'code "{PROJECT_DIR}/.vscode/settings.json"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
