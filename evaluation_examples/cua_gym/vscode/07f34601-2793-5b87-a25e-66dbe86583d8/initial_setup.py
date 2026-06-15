"""
Initial Setup: Set up custom color theme override in VSCode settings
Task ID: vscode_web_064
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_064'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')


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


def create_project_files():
    """Create a realistic webapp project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'styles'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # package.json
    pkg = {
        "name": "webapp",
        "version": "1.2.0",
        "description": "Customer portal web application",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "axios": "^1.3.4"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # src/index.js
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
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
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Settings from './components/Settings';
import Profile from './components/Profile';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Dashboard.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    totalUsers: 0,
    activeUsers: 0,
    revenue: 0,
    conversionRate: 0,
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get('/api/metrics');
        setMetrics(response.data);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      }
    };
    fetchMetrics();
  }, []);

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Users</h3>
          <p>{metrics.totalUsers.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Active Users</h3>
          <p>{metrics.activeUsers.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Revenue</h3>
          <p>${metrics.revenue.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Conversion Rate</h3>
          <p>{metrics.conversionRate}%</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
""")

    # src/components/Settings.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Settings.js'), 'w') as f:
        f.write("""import React, { useState } from 'react';

const Settings = () => {
  const [preferences, setPreferences] = useState({
    notifications: true,
    darkMode: false,
    language: 'en',
    timezone: 'UTC',
  });

  const handleToggle = (key) => {
    setPreferences(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="settings-page">
      <h1>Settings</h1>
      <div className="settings-section">
        <h2>Preferences</h2>
        <label>
          <input
            type="checkbox"
            checked={preferences.notifications}
            onChange={() => handleToggle('notifications')}
          />
          Enable Notifications
        </label>
        <label>
          <input
            type="checkbox"
            checked={preferences.darkMode}
            onChange={() => handleToggle('darkMode')}
          />
          Dark Mode
        </label>
      </div>
    </div>
  );
};

export default Settings;
""")

    # src/components/Profile.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Profile.js'), 'w') as f:
        f.write("""import React from 'react';

const Profile = () => {
  const user = {
    name: 'Elena Rodriguez',
    email: 'elena.rodriguez@techcorp.io',
    role: 'Senior Developer',
    team: 'Frontend Platform',
    joinDate: '2023-06-15',
  };

  return (
    <div className="profile-page">
      <h1>Profile</h1>
      <div className="profile-card">
        <h2>{user.name}</h2>
        <p className="email">{user.email}</p>
        <p className="role">{user.role}</p>
        <p className="team">{user.team}</p>
        <p className="join-date">Member since {user.joinDate}</p>
      </div>
    </div>
  );
};

export default Profile;
""")

    # src/styles/global.css
    with open(os.path.join(PROJECT_DIR, 'src', 'styles', 'global.css'), 'w') as f:
        f.write("""* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard {
  padding: 20px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-card h3 {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.metric-card p {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a2e;
}
""")

    # public/index.html
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Customer Portal</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Customer Portal WebApp

A React-based customer portal with dashboard analytics, user settings, and profile management.

## Getting Started

```bash
npm install
npm start
```

## Features

- Real-time dashboard metrics
- User preference management
- Profile editing
- Dark mode support (planned)
""")

    print(f'Project files created at {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up minimal VSCode settings with Dark+ theme, no color customizations."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure Dark+ theme is active, no color customizations
    settings["workbench.colorTheme"] = "Default Dark+"
    settings["editor.fontSize"] = 14
    settings["editor.tabSize"] = 2
    settings["editor.minimap.enabled"] = True
    settings["files.autoSave"] = "afterDelay"

    # Explicitly remove any existing color customizations
    if "workbench.colorCustomizations" in settings:
        del settings["workbench.colorCustomizations"]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to {SETTINGS_PATH}')


def main():
    create_project_files()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
