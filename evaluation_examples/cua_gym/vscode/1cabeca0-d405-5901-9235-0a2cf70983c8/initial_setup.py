"""
Initial Setup: Create workspace-specific VSCode settings
Task ID: vscode_stu_067
Domain: vscode

Sets up:
- A realistic React project at ~/webdev/react-app/
- Global VSCode user settings with tabSize 4, no formatOnSave, minimap enabled
- NO .vscode/settings.json in the project (agent must create it)
- Opens VSCode with the project folder
"""

import json
import os
import shlex
import subprocess
import time

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "webdev", "react-app")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
GLOBAL_SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
    """Create a realistic React project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "components"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "hooks"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "utils"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "public"), exist_ok=True)

    # package.json
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "prettier": "^3.1.0",
            "@types/react": "^18.2.43"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        }
    }
    with open(os.path.join(PROJECT_DIR, "package.json"), "w") as f:
        json.dump(package_json, f, indent=4)

    # src/App.jsx
    app_jsx = '''import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <div className="app-container">
                <Navbar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/profile/:userId" element={<UserProfile />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

export default App;
'''
    with open(os.path.join(PROJECT_DIR, "src", "App.jsx"), "w") as f:
        f.write(app_jsx)

    # src/components/Navbar.jsx
    navbar = '''import React, { useState } from 'react';

const Navbar = () => {
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <h1>TaskFlow Pro</h1>
            </div>
            <button
                className="menu-toggle"
                onClick={() => setMenuOpen(!menuOpen)}
            >
                ☰
            </button>
            <ul className={`nav-links ${menuOpen ? 'active' : ''}`}>
                <li><a href="/">Dashboard</a></li>
                <li><a href="/projects">Projects</a></li>
                <li><a href="/team">Team</a></li>
                <li><a href="/settings">Settings</a></li>
            </ul>
        </nav>
    );
};

export default Navbar;
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "Navbar.jsx"), "w") as f:
        f.write(navbar)

    # src/components/Dashboard.jsx
    dashboard = '''import React, { useEffect, useState } from 'react';
import { fetchMetrics } from '../utils/api';
import useDebounce from '../hooks/useDebounce';

const Dashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const debouncedSearch = useDebounce(searchTerm, 300);

    useEffect(() => {
        fetchMetrics().then(data => setMetrics(data));
    }, []);

    useEffect(() => {
        if (debouncedSearch) {
            console.log('Searching for:', debouncedSearch);
        }
    }, [debouncedSearch]);

    if (!metrics) return <div className="loading">Loading dashboard...</div>;

    return (
        <div className="dashboard">
            <h2>Project Overview</h2>
            <input
                type="text"
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <div className="metrics-grid">
                <div className="metric-card">
                    <span className="metric-value">{metrics.totalTasks}</span>
                    <span className="metric-label">Total Tasks</span>
                </div>
                <div className="metric-card">
                    <span className="metric-value">{metrics.completedTasks}</span>
                    <span className="metric-label">Completed</span>
                </div>
                <div className="metric-card">
                    <span className="metric-value">{metrics.activeMembers}</span>
                    <span className="metric-label">Active Members</span>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "Dashboard.jsx"), "w") as f:
        f.write(dashboard)

    # src/components/UserProfile.jsx
    user_profile = '''import React from 'react';
import { useParams } from 'react-router-dom';

const UserProfile = () => {
    const { userId } = useParams();

    return (
        <div className="user-profile">
            <h2>User Profile</h2>
            <p>Viewing profile for user: {userId}</p>
        </div>
    );
};

export default UserProfile;
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "UserProfile.jsx"), "w") as f:
        f.write(user_profile)

    # src/hooks/useDebounce.js
    use_debounce = '''import { useState, useEffect } from 'react';

function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
}

export default useDebounce;
'''
    with open(os.path.join(PROJECT_DIR, "src", "hooks", "useDebounce.js"), "w") as f:
        f.write(use_debounce)

    # src/utils/api.js
    api_js = '''import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

export const fetchMetrics = async () => {
    try {
        const response = await axios.get(`${API_BASE}/metrics`);
        return response.data;
    } catch (error) {
        console.error('Failed to fetch metrics:', error);
        return { totalTasks: 0, completedTasks: 0, activeMembers: 0 };
    }
};

export const fetchTasks = async (filters = {}) => {
    try {
        const response = await axios.get(`${API_BASE}/tasks`, { params: filters });
        return response.data;
    } catch (error) {
        console.error('Failed to fetch tasks:', error);
        return [];
    }
};
'''
    with open(os.path.join(PROJECT_DIR, "src", "utils", "api.js"), "w") as f:
        f.write(api_js)

    # src/App.css
    app_css = '''.app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background-color: #1a1a2e;
    color: #eee;
}

.main-content {
    flex: 1;
    padding: 2rem;
    background-color: #f5f5f5;
}

.dashboard {
    max-width: 960px;
    margin: 0 auto;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.metric-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}
'''
    with open(os.path.join(PROJECT_DIR, "src", "App.css"), "w") as f:
        f.write(app_css)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>TaskFlow Pro</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
'''
    with open(os.path.join(PROJECT_DIR, "public", "index.html"), "w") as f:
        f.write(index_html)

    # .eslintrc.json
    eslintrc = {
        "env": {"browser": True, "es2021": True},
        "extends": ["eslint:recommended", "plugin:react/recommended"],
        "parserOptions": {
            "ecmaFeatures": {"jsx": True},
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "react/react-in-jsx-scope": "off",
            "no-unused-vars": "warn"
        }
    }
    with open(os.path.join(PROJECT_DIR, ".eslintrc.json"), "w") as f:
        json.dump(eslintrc, f, indent=4)

    print(f"React project created at: {PROJECT_DIR}")


def setup_global_vscode_settings():
    """Set global VSCode settings: tabSize 4, no formatOnSave, minimap enabled."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings if any, then merge
    settings = {}
    if os.path.exists(GLOBAL_SETTINGS_PATH):
        try:
            with open(GLOBAL_SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    settings.update({
        "editor.tabSize": 4,
        "editor.formatOnSave": False,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "editor.fontSize": 14,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "explorer.confirmDelete": False
    })

    with open(GLOBAL_SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Global settings written to: {GLOBAL_SETTINGS_PATH}")


def ensure_no_workspace_settings():
    """Make sure .vscode/settings.json does NOT exist in the project."""
    vscode_dir = os.path.join(PROJECT_DIR, ".vscode")
    settings_file = os.path.join(vscode_dir, "settings.json")
    if os.path.exists(settings_file):
        os.remove(settings_file)
        print(f"Removed existing workspace settings: {settings_file}")
    else:
        print(f"Confirmed: No .vscode/settings.json exists in project")


def main():
    create_project_files()
    setup_global_vscode_settings()
    ensure_no_workspace_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: VSCode launched with ~/webdev/react-app")


main()
