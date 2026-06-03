"""
Initial Setup: Git stash workflow in VSCode
Task ID: vscode_gf2_023
Domain: vscode

Creates a full-stack-app git repository with realistic project structure.
No stashes exist. Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_023'
PROJECT_DIR = f'{WORKDIR}/projects/full-stack-app'


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


def run(cmd, cwd=None):
    """Run a shell command."""
    subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # Clean up if exists
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- Root config files ---
    create_file(f'{PROJECT_DIR}/package.json', """{
  "name": "full-stack-app",
  "version": "1.0.0",
  "private": true,
  "description": "Customer portal with React frontend and Express backend",
  "scripts": {
    "dev": "concurrently \\"npm run dev:frontend\\" \\"npm run dev:backend\\"",
    "dev:frontend": "cd frontend && npm start",
    "dev:backend": "cd backend && npm run dev"
  },
  "devDependencies": {
    "concurrently": "^8.2.0"
  }
}
""")

    create_file(f'{PROJECT_DIR}/README.md', """# Full Stack Customer Portal

A modern customer management portal built with React and Express.

## Architecture

- **Frontend**: React 18 with React Router, Tailwind CSS
- **Backend**: Express.js with PostgreSQL via Prisma ORM
- **Auth**: JWT-based authentication

## Getting Started

```bash
npm install
npm run dev
```

Frontend runs on http://localhost:3000
Backend API runs on http://localhost:4000
""")

    create_file(f'{PROJECT_DIR}/.gitignore', """node_modules/
dist/
build/
.env
.env.local
*.log
.DS_Store
coverage/
""")

    # --- Frontend files ---
    create_file(f'{PROJECT_DIR}/frontend/package.json', """{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "tailwindcss": "^3.4.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
""")

    create_file(f'{PROJECT_DIR}/frontend/src/App.jsx', """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
""")

    create_file(f'{PROJECT_DIR}/frontend/src/index.js', """import React from 'react';
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

    create_file(f'{PROJECT_DIR}/frontend/src/components/Navbar.jsx', """import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard', icon: 'chart-bar' },
  { path: '/customers', label: 'Customers', icon: 'users' },
  { path: '/settings', label: 'Settings', icon: 'cog' },
];

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-xl font-bold">
            CustomerHub
          </Link>
          <div className="flex space-x-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  location.pathname === item.path
                    ? 'bg-indigo-700'
                    : 'hover:bg-indigo-500'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
""")

    create_file(f'{PROJECT_DIR}/frontend/src/pages/Dashboard.jsx', """import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({
    totalCustomers: 0,
    activeSubscriptions: 0,
    monthlyRevenue: 0,
  });

  useEffect(() => {
    axios.get('/api/dashboard/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error('Failed to load stats:', err));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm">Total Customers</h3>
          <p className="text-3xl font-bold">{stats.totalCustomers}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm">Active Subscriptions</h3>
          <p className="text-3xl font-bold">{stats.activeSubscriptions}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm">Monthly Revenue</h3>
          <p className="text-3xl font-bold">${stats.monthlyRevenue.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
""")

    create_file(f'{PROJECT_DIR}/frontend/src/pages/Customers.jsx', """import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    axios.get('/api/customers')
      .then(res => setCustomers(res.data))
      .catch(err => console.error('Failed to load customers:', err));
  }, []);

  const filtered = customers.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Customers</h1>
      <input
        type="text"
        placeholder="Search customers..."
        className="w-full p-3 border rounded-lg mb-4"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">Name</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">Email</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">Plan</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filtered.map((customer) => (
              <tr key={customer.id}>
                <td className="px-6 py-4">{customer.name}</td>
                <td className="px-6 py-4">{customer.email}</td>
                <td className="px-6 py-4">{customer.plan}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    customer.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {customer.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Customers;
""")

    create_file(f'{PROJECT_DIR}/frontend/src/pages/Settings.jsx', """import React, { useState } from 'react';

function Settings() {
  const [notifyEmail, setNotifyEmail] = useState(true);
  const [theme, setTheme] = useState('light');

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <div className="bg-white rounded-lg shadow p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium">Email Notifications</h3>
            <p className="text-sm text-gray-500">Receive alerts for new customers</p>
          </div>
          <button
            onClick={() => setNotifyEmail(!notifyEmail)}
            className={`w-12 h-6 rounded-full ${notifyEmail ? 'bg-indigo-600' : 'bg-gray-300'}`}
          >
            <span className={`block w-5 h-5 bg-white rounded-full transform transition ${
              notifyEmail ? 'translate-x-6' : 'translate-x-0.5'
            }`} />
          </button>
        </div>
        <div>
          <h3 className="font-medium mb-2">Theme</h3>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="border rounded-lg p-2"
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="system">System</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default Settings;
""")

    create_file(f'{PROJECT_DIR}/frontend/src/styles/global.css', """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
""")

    # --- Backend files ---
    create_file(f'{PROJECT_DIR}/backend/package.json', """{
  "name": "backend",
  "version": "1.0.0",
  "main": "src/server.js",
  "scripts": {
    "dev": "nodemon src/server.js",
    "start": "node src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "@prisma/client": "^5.7.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.2",
    "prisma": "^5.7.0"
  }
}
""")

    create_file(f'{PROJECT_DIR}/backend/src/server.js', """const express = require('express');
const cors = require('cors');
require('dotenv').config();

const customerRoutes = require('./routes/customers');
const dashboardRoutes = require('./routes/dashboard');

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

app.use('/api/customers', customerRoutes);
app.use('/api/dashboard', dashboardRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
""")

    create_file(f'{PROJECT_DIR}/backend/src/routes/customers.js', """const express = require('express');
const router = express.Router();

// In-memory store for demo
const customers = [
  { id: 1, name: 'Acme Corp', email: 'billing@acme.com', plan: 'Enterprise', status: 'active' },
  { id: 2, name: 'TechStart Inc', email: 'admin@techstart.io', plan: 'Pro', status: 'active' },
  { id: 3, name: 'Design Studio', email: 'hello@designstudio.co', plan: 'Basic', status: 'inactive' },
  { id: 4, name: 'CloudNine Solutions', email: 'ops@cloudnine.dev', plan: 'Enterprise', status: 'active' },
  { id: 5, name: 'Fresh Eats', email: 'contact@fresheats.com', plan: 'Pro', status: 'active' },
];

router.get('/', (req, res) => {
  res.json(customers);
});

router.get('/:id', (req, res) => {
  const customer = customers.find(c => c.id === parseInt(req.params.id));
  if (!customer) return res.status(404).json({ error: 'Customer not found' });
  res.json(customer);
});

module.exports = router;
""")

    create_file(f'{PROJECT_DIR}/backend/src/routes/dashboard.js', """const express = require('express');
const router = express.Router();

router.get('/stats', (req, res) => {
  res.json({
    totalCustomers: 247,
    activeSubscriptions: 189,
    monthlyRevenue: 34750,
    churnRate: 2.4,
  });
});

module.exports = router;
""")

    # --- Initialize Git repository ---
    run('git init', cwd=PROJECT_DIR)
    run('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Developer"', cwd=PROJECT_DIR)
    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Initial commit: full-stack customer portal with React frontend and Express backend"', cwd=PROJECT_DIR)

    # Add a few more commits for realistic history
    create_file(f'{PROJECT_DIR}/frontend/src/utils/api.js', """import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
""")
    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add API utility with axios interceptors"', cwd=PROJECT_DIR)

    create_file(f'{PROJECT_DIR}/backend/src/middleware/auth.js', """const jwt = require('jsonwebtoken');

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'dev-secret');
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}

module.exports = authMiddleware;
""")
    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Add JWT authentication middleware"', cwd=PROJECT_DIR)

    # Verify no stashes
    run('git stash clear', cwd=PROJECT_DIR)

    print(f'Project created at: {PROJECT_DIR}')
    print('Git repository initialized with 3 commits, no stashes.')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
