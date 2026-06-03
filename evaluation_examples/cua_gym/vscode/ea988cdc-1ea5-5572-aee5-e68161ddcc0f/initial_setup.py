"""
Initial Setup: Configure GitHub Actions workflow for automated code coverage reporting
Task ID: vscode_gf3_056
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_056'
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

def create_initial():
    # Create realistic webapp project structure
    dirs = [
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/utils',
        f'{PROJECT_DIR}/src/services',
        f'{PROJECT_DIR}/tests/unit',
        f'{PROJECT_DIR}/tests/integration',
        f'{PROJECT_DIR}/.github',  # .github exists but NO workflows/coverage.yml
        f'{PROJECT_DIR}/public',
        f'{PROJECT_DIR}/config',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "webapp",
        "version": "2.4.1",
        "description": "Customer portal web application",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "jest --verbose",
            "lint": "eslint src/ --ext .js,.jsx",
            "format": "prettier --write 'src/**/*.{js,jsx,css}'"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.22.0",
            "axios": "^1.6.7",
            "@mui/material": "^5.15.7",
            "@emotion/react": "^11.11.3",
            "@emotion/styled": "^11.11.0"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "@testing-library/react": "^14.2.1",
            "@testing-library/jest-dom": "^6.4.1",
            "eslint": "^8.56.0",
            "prettier": "^3.2.4",
            "react-scripts": "5.0.1"
        },
        "jest": {
            "collectCoverageFrom": [
                "src/**/*.{js,jsx}",
                "!src/index.js",
                "!src/reportWebVitals.js"
            ],
            "coverageReporters": ["lcov", "text", "text-summary"],
            "coverageThreshold": {
                "global": {
                    "branches": 70,
                    "functions": 75,
                    "lines": 80,
                    "statements": 80
                }
            }
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.jsx
    with open(f'{PROJECT_DIR}/src/App.jsx', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import OrderHistory from './components/OrderHistory';
import Navigation from './components/Navigation';

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/orders" element={<OrderHistory />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.jsx
    with open(f'{PROJECT_DIR}/src/components/Dashboard.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchMetrics } from '../services/api';
import { formatCurrency, formatPercentage } from '../utils/formatters';

function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics()
      .then(data => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-spinner">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Customer Portal Dashboard</h1>
      {metrics && (
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Total Revenue</h3>
            <span>{formatCurrency(metrics.totalRevenue)}</span>
          </div>
          <div className="metric-card">
            <h3>Active Users</h3>
            <span>{metrics.activeUsers.toLocaleString()}</span>
          </div>
          <div className="metric-card">
            <h3>Conversion Rate</h3>
            <span>{formatPercentage(metrics.conversionRate)}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
""")

    # src/components/Navigation.jsx
    with open(f'{PROJECT_DIR}/src/components/Navigation.jsx', 'w') as f:
        f.write("""import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navigation() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/profile', label: 'Profile' },
    { path: '/orders', label: 'Orders' },
  ];

  return (
    <nav className="main-nav">
      <div className="nav-brand">CustomerPortal</div>
      <ul className="nav-links">
        {navItems.map(item => (
          <li key={item.path} className={location.pathname === item.path ? 'active' : ''}>
            <Link to={item.path}>{item.label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Navigation;
""")

    # src/components/UserProfile.jsx
    with open(f'{PROJECT_DIR}/src/components/UserProfile.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchUserProfile, updateUserProfile } from '../services/api';

function UserProfile() {
  const [profile, setProfile] = useState(null);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    fetchUserProfile().then(setProfile);
  }, []);

  const handleSave = async (updatedProfile) => {
    const result = await updateUserProfile(updatedProfile);
    setProfile(result);
    setEditing(false);
  };

  if (!profile) return <div>Loading profile...</div>;

  return (
    <div className="user-profile">
      <h2>{profile.name}</h2>
      <p>Email: {profile.email}</p>
      <p>Member since: {profile.memberSince}</p>
      <p>Tier: {profile.tier}</p>
      {editing ? (
        <button onClick={() => handleSave(profile)}>Save Changes</button>
      ) : (
        <button onClick={() => setEditing(true)}>Edit Profile</button>
      )}
    </div>
  );
}

export default UserProfile;
""")

    # src/components/OrderHistory.jsx
    with open(f'{PROJECT_DIR}/src/components/OrderHistory.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchOrders } from '../services/api';
import { formatCurrency } from '../utils/formatters';

function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchOrders().then(setOrders);
  }, []);

  const filteredOrders = orders.filter(order => {
    if (filter === 'all') return true;
    return order.status === filter;
  });

  return (
    <div className="order-history">
      <h2>Order History</h2>
      <div className="filter-bar">
        {['all', 'completed', 'pending', 'cancelled'].map(f => (
          <button
            key={f}
            className={filter === f ? 'active' : ''}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>
      <table className="orders-table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Items</th>
            <th>Total</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredOrders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.date}</td>
              <td>{order.items.length} items</td>
              <td>{formatCurrency(order.total)}</td>
              <td className={`status-${order.status}`}>{order.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default OrderHistory;
""")

    # src/services/api.js
    with open(f'{PROJECT_DIR}/src/services/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.customerportal.example.com/v2';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const fetchMetrics = () => apiClient.get('/metrics').then(r => r.data);
export const fetchUserProfile = () => apiClient.get('/user/profile').then(r => r.data);
export const updateUserProfile = (data) => apiClient.put('/user/profile', data).then(r => r.data);
export const fetchOrders = () => apiClient.get('/orders').then(r => r.data);
""")

    # src/utils/formatters.js
    with open(f'{PROJECT_DIR}/src/utils/formatters.js', 'w') as f:
        f.write("""export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

export function formatPercentage(value) {
  return `${(value * 100).toFixed(1)}%`;
}

export function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function truncateText(text, maxLength = 50) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}
""")

    # tests/unit/formatters.test.js
    with open(f'{PROJECT_DIR}/tests/unit/formatters.test.js', 'w') as f:
        f.write("""import { formatCurrency, formatPercentage, formatDate, truncateText } from '../../src/utils/formatters';

describe('formatCurrency', () => {
  test('formats positive amounts', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  test('formats zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  test('formats negative amounts', () => {
    expect(formatCurrency(-500)).toBe('-$500.00');
  });
});

describe('formatPercentage', () => {
  test('formats decimal to percentage', () => {
    expect(formatPercentage(0.856)).toBe('85.6%');
  });

  test('formats zero', () => {
    expect(formatPercentage(0)).toBe('0.0%');
  });
});

describe('formatDate', () => {
  test('formats ISO date string', () => {
    const result = formatDate('2025-03-15');
    expect(result).toContain('Mar');
    expect(result).toContain('2025');
  });
});

describe('truncateText', () => {
  test('does not truncate short text', () => {
    expect(truncateText('Hello', 10)).toBe('Hello');
  });

  test('truncates long text with ellipsis', () => {
    const long = 'This is a very long text that should be truncated';
    const result = truncateText(long, 20);
    expect(result.length).toBe(23); // 20 + '...'
    expect(result.endsWith('...')).toBe(true);
  });
});
""")

    # tests/unit/Dashboard.test.js
    with open(f'{PROJECT_DIR}/tests/unit/Dashboard.test.js', 'w') as f:
        f.write("""import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '../../src/components/Dashboard';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');

describe('Dashboard', () => {
  test('shows loading state initially', () => {
    api.fetchMetrics.mockReturnValue(new Promise(() => {}));
    render(<Dashboard />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('displays metrics after loading', async () => {
    api.fetchMetrics.mockResolvedValue({
      totalRevenue: 150000,
      activeUsers: 2847,
      conversionRate: 0.124,
    });
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('Total Revenue')).toBeInTheDocument();
    });
  });
});
""")

    # tests/integration/api.test.js
    with open(f'{PROJECT_DIR}/tests/integration/api.test.js', 'w') as f:
        f.write("""import axios from 'axios';
import { fetchMetrics, fetchOrders } from '../../src/services/api';

jest.mock('axios');

describe('API Service', () => {
  test('fetchMetrics calls correct endpoint', async () => {
    const mockData = { totalRevenue: 50000 };
    axios.create.mockReturnValue({
      get: jest.fn().mockResolvedValue({ data: mockData }),
      interceptors: { request: { use: jest.fn() } },
    });
    // Test would verify the API call
  });
});
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
build/
coverage/
.env
.env.local
.DS_Store
*.log
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Customer Portal WebApp

A React-based customer portal providing dashboard analytics, user profile management, and order history tracking.

## Getting Started

```bash
npm install
npm start
```

## Testing

```bash
npm test
npm test -- --coverage
```

## Architecture

- `src/components/` - React components
- `src/services/` - API client and service layer
- `src/utils/` - Shared utility functions
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests

## Team Coverage Policy

All PRs must maintain a minimum of 80% line coverage. Coverage reports are reviewed before merge.
""")

    # jest.config.js
    with open(f'{PROJECT_DIR}/jest.config.js', 'w') as f:
        f.write("""module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterSetup: ['@testing-library/jest-dom'],
  moduleNameMapper: {
    '\\\\.(css|less|scss)$': '<rootDir>/tests/__mocks__/styleMock.js',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/index.js',
    '!src/reportWebVitals.js',
  ],
  coverageReporters: ['lcov', 'text', 'text-summary'],
  coverageDirectory: 'coverage',
};
""")

    # An existing CI workflow (but NOT coverage) to make it realistic
    os.makedirs(f'{PROJECT_DIR}/.github/workflows', exist_ok=True)
    with open(f'{PROJECT_DIR}/.github/workflows/ci.yml', 'w') as f:
        f.write("""name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  build:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
""")

    # config/.env.example
    with open(f'{PROJECT_DIR}/config/.env.example', 'w') as f:
        f.write("""REACT_APP_API_URL=https://api.customerportal.example.com/v2
REACT_APP_CODECOV_TOKEN=your_codecov_token_here
""")

    print(f'Initial project created: {PROJECT_DIR}')

    # NO coverage.yml — that's the agent's task

    # GUI-ready startup: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
