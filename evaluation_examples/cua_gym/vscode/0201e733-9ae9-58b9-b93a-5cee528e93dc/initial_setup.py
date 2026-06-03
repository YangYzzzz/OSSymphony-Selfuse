"""
Initial Setup: Fix Prettier configuration resolution in VSCode
Task ID: vscode_fix_053
Domain: vscode

Creates a monorepo with .prettierrc in root, a frontend package with JS files,
and sets prettier.configPath to a non-existent path in VSCode settings so
Prettier falls back to defaults (double quotes instead of single quotes).
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
WORKDIR = HOME
TASK_ID = 'vscode_fix_053'

# Directory structure
MONOREPO = os.path.join(HOME, 'monorepo')
FRONTEND = os.path.join(MONOREPO, 'packages', 'frontend')
SRC_DIR = os.path.join(FRONTEND, 'src')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
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


def create_monorepo():
    """Create the monorepo directory structure with frontend package."""
    # Create directories
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(os.path.join(FRONTEND, 'public'), exist_ok=True)

    # Root .prettierrc with singleQuote: true
    prettierrc = {
        "singleQuote": True,
        "trailingComma": "es5",
        "tabWidth": 2,
        "semi": True,
        "printWidth": 80
    }
    with open(os.path.join(MONOREPO, '.prettierrc'), 'w') as f:
        json.dump(prettierrc, f, indent=2)
    print(f'Created .prettierrc at {MONOREPO}/.prettierrc')

    # Root package.json (monorepo root)
    root_pkg = {
        "name": "acme-monorepo",
        "version": "1.0.0",
        "private": True,
        "workspaces": ["packages/*"],
        "devDependencies": {
            "prettier": "^3.2.0"
        }
    }
    with open(os.path.join(MONOREPO, 'package.json'), 'w') as f:
        json.dump(root_pkg, f, indent=2)

    # Frontend package.json
    frontend_pkg = {
        "name": "@acme/frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(os.path.join(FRONTEND, 'package.json'), 'w') as f:
        json.dump(frontend_pkg, f, indent=2)

    # Source files using double quotes (what Prettier defaults produce)
    app_js = '''import React from "react";
import { Header } from "./components/Header";
import { Dashboard } from "./components/Dashboard";
import { Footer } from "./components/Footer";

function App() {
  const [theme, setTheme] = React.useState("light");
  const [locale, setLocale] = React.useState("en-US");

  const handleThemeToggle = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <div className="app-container" data-theme={theme}>
      <Header
        title="Acme Dashboard"
        onThemeToggle={handleThemeToggle}
        currentTheme={theme}
      />
      <Dashboard locale={locale} theme={theme} />
      <Footer companyName="Acme Corp" year={2025} />
    </div>
  );
}

export default App;
'''
    with open(os.path.join(SRC_DIR, 'App.js'), 'w') as f:
        f.write(app_js)

    # Header component
    header_js = '''import React from "react";

export function Header({ title, onThemeToggle, currentTheme }) {
  return (
    <header className="main-header">
      <h1>{title}</h1>
      <nav className="header-nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/reports">Reports</a>
        <a href="/settings">Settings</a>
      </nav>
      <button onClick={onThemeToggle} className="theme-toggle">
        {currentTheme === "light" ? "Switch to Dark" : "Switch to Light"}
      </button>
    </header>
  );
}
'''
    os.makedirs(os.path.join(SRC_DIR, 'components'), exist_ok=True)
    with open(os.path.join(SRC_DIR, 'components', 'Header.js'), 'w') as f:
        f.write(header_js)

    # Dashboard component
    dashboard_js = '''import React from "react";

const METRIC_LABELS = {
  revenue: "Total Revenue",
  users: "Active Users",
  orders: "Pending Orders",
  satisfaction: "Customer Satisfaction",
};

export function Dashboard({ locale, theme }) {
  const [metrics, setMetrics] = React.useState({
    revenue: 245830,
    users: 1847,
    orders: 56,
    satisfaction: 94.2,
  });

  const formatCurrency = (value) => {
    return new Intl.NumberFormat(locale, {
      style: "currency",
      currency: "USD",
    }).format(value);
  };

  return (
    <main className="dashboard" data-theme={theme}>
      <h2>Performance Overview</h2>
      <div className="metrics-grid">
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key} className="metric-card">
            <span className="metric-label">{METRIC_LABELS[key]}</span>
            <span className="metric-value">
              {key === "revenue" ? formatCurrency(value) : value}
            </span>
          </div>
        ))}
      </div>
    </main>
  );
}
'''
    with open(os.path.join(SRC_DIR, 'components', 'Dashboard.js'), 'w') as f:
        f.write(dashboard_js)

    # Footer component
    footer_js = '''import React from "react";

export function Footer({ companyName, year }) {
  return (
    <footer className="main-footer">
      <p>
        &copy; {year} {companyName}. All rights reserved.
      </p>
      <div className="footer-links">
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
        <a href="/contact">Contact Us</a>
      </div>
    </footer>
  );
}
'''
    with open(os.path.join(SRC_DIR, 'components', 'Footer.js'), 'w') as f:
        f.write(footer_js)

    # utils.js
    utils_js = '''export function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

export function formatDate(date, locale = "en-US") {
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date(date));
}

export function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}
'''
    with open(os.path.join(SRC_DIR, 'utils.js'), 'w') as f:
        f.write(utils_js)

    # index.js
    index_js = '''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(os.path.join(SRC_DIR, 'index.js'), 'w') as f:
        f.write(index_js)

    # index.css
    index_css = '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
    "Oxygen", "Ubuntu", sans-serif;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-container[data-theme="dark"] {
  background-color: #1a1a2e;
  color: #e0e0e0;
}

.main-header {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
}

.dashboard {
  flex: 1;
  padding: 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.metric-card {
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: white;
}

.main-footer {
  padding: 1rem 2rem;
  background-color: #34495e;
  color: white;
  text-align: center;
}
'''
    with open(os.path.join(SRC_DIR, 'index.css'), 'w') as f:
        f.write(index_css)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Acme Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
'''
    with open(os.path.join(FRONTEND, 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    print('Monorepo structure created successfully')


def setup_vscode_settings():
    """Configure VSCode settings with incorrect prettier.configPath."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set prettier.configPath to a non-existent path (THE BUG)
    settings.update({
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": True,
        "editor.tabSize": 2,
        "prettier.configPath": "/home/user/monorepo/configs/.prettierrc",
        "[javascript]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[javascriptreact]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written to {SETTINGS_PATH}')
    print(f'  prettier.configPath set to NON-EXISTENT path: /home/user/monorepo/configs/.prettierrc')


def main():
    create_monorepo()
    setup_vscode_settings()

    # Launch VSCode with the frontend folder
    launch_gui(f'code "{FRONTEND}"', delay_sec=2.0)
    print(f'GUI_READY: launched VSCode with {FRONTEND}')


main()
