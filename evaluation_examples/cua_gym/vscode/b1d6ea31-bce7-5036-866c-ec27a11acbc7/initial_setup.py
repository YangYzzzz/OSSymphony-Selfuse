"""
Initial Setup: Set up i18n workflow in ~/project
Task ID: vscode_wf_079
Domain: vscode

Creates a React project with hardcoded translations (no i18n infrastructure).
VSCode opens with ~/project.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')

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
    # Create project structure - a React app with hardcoded translations
    dirs = [
        os.path.join(PROJECT, 'src', 'components'),
        os.path.join(PROJECT, 'src', 'pages'),
        os.path.join(PROJECT, 'public'),
        os.path.join(PROJECT, '.vscode'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-i18next": "^13.5.0",
            "i18next": "^23.7.0",
            "react-scripts": "5.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/App.js - main app with hardcoded English strings
    app_js = '''import React from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <Dashboard />
      </main>
      <Footer />
    </div>
  );
}

export default App;
'''
    with open(os.path.join(PROJECT, 'src', 'App.js'), 'w') as f:
        f.write(app_js)

    # src/components/Header.js - hardcoded English strings
    header_js = '''import React from 'react';

function Header() {
  return (
    <header className="app-header">
      <h1>Inventory Management System</h1>
      <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/products">Products</a>
        <a href="/orders">Orders</a>
        <a href="/reports">Reports</a>
        <a href="/settings">Settings</a>
      </nav>
      <div className="user-menu">
        <span>Welcome back, Admin</span>
        <button>Log Out</button>
      </div>
    </header>
  );
}

export default Header;
'''
    with open(os.path.join(PROJECT, 'src', 'components', 'Header.js'), 'w') as f:
        f.write(header_js)

    # src/components/Footer.js
    footer_js = '''import React from 'react';

function Footer() {
  return (
    <footer className="app-footer">
      <p>Copyright 2025 Meridian Supply Co. All rights reserved.</p>
      <div className="footer-links">
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
        <a href="/contact">Contact Us</a>
      </div>
    </footer>
  );
}

export default Footer;
'''
    with open(os.path.join(PROJECT, 'src', 'components', 'Footer.js'), 'w') as f:
        f.write(footer_js)

    # src/pages/Dashboard.js - hardcoded strings for inventory dashboard
    dashboard_js = '''import React, { useState } from 'react';

function Dashboard() {
  const [searchQuery, setSearchQuery] = useState('');

  const summaryCards = [
    { title: 'Total Products', value: 1247, change: '+12 this week' },
    { title: 'Low Stock Items', value: 23, change: 'Needs attention' },
    { title: 'Pending Orders', value: 58, change: '15 urgent' },
    { title: 'Revenue This Month', value: '$142,580', change: '+8.3% vs last month' },
  ];

  const recentActivity = [
    'Order #4521 shipped to Portland warehouse',
    'Stock alert: Widget A below minimum threshold',
    'New supplier Apex Materials added to system',
    'Monthly inventory audit completed successfully',
  ];

  return (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>
      <p className="subtitle">Here is your inventory summary for today</p>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search products, orders, or suppliers..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button>Search</button>
      </div>

      <div className="summary-cards">
        {summaryCards.map((card, idx) => (
          <div key={idx} className="card">
            <h3>{card.title}</h3>
            <p className="value">{card.value}</p>
            <p className="change">{card.change}</p>
          </div>
        ))}
      </div>

      <div className="recent-activity">
        <h3>Recent Activity</h3>
        {recentActivity.map((item, idx) => (
          <p key={idx}>{item}</p>
        ))}
      </div>

      <div className="actions">
        <button>Add New Product</button>
        <button>Create Order</button>
        <button>Generate Report</button>
        <button>Export Data</button>
      </div>
    </div>
  );
}

export default Dashboard;
'''
    with open(os.path.join(PROJECT, 'src', 'pages', 'Dashboard.js'), 'w') as f:
        f.write(dashboard_js)

    # src/index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(os.path.join(PROJECT, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # public/index.html
    index_html = '''<!DOCTYPE html>
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
'''
    with open(os.path.join(PROJECT, 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    # Minimal .vscode/settings.json (no i18n-ally settings)
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True
    }
    with open(os.path.join(PROJECT, '.vscode', 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial project created: {PROJECT}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
