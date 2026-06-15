"""
Initial Setup: Configure VSCode language-specific formatter settings
Task ID: vscode_gf1_050
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_050'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = os.path.join(WORKDIR, "projects", "frontend")


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_project_files():
    """Create a realistic frontend project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "components"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "utils"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "public"), exist_ok=True)

    # package.json
    package_json = {
        "name": "dashboard-app",
        "version": "1.2.0",
        "description": "Internal analytics dashboard for marketing team",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "axios": "^1.3.4",
            "chart.js": "^4.2.1",
            "react-chartjs-2": "^5.2.0",
            "date-fns": "^2.29.3"
        },
        "devDependencies": {
            "eslint": "^8.35.0",
            "prettier": "^2.8.4",
            "@types/react": "^18.0.28"
        }
    }
    with open(os.path.join(PROJECT_DIR, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    with open(os.path.join(PROJECT_DIR, "src", "index.js"), "w") as f:
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

    # src/App.tsx
    with open(os.path.join(PROJECT_DIR, "src", "App.tsx"), "w") as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CampaignList from './components/CampaignList';
import Header from './components/Header';

interface AppProps {
  theme?: 'light' | 'dark';
}

const App: React.FC<AppProps> = ({ theme = 'light' }) => {
  return (
    <BrowserRouter>
      <div className={`app-container ${theme}`}>
        <Header title="Marketing Analytics" />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/campaigns" element={<CampaignList />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
""")

    # src/components/Dashboard.tsx
    with open(os.path.join(PROJECT_DIR, "src", "components", "Dashboard.tsx"), "w") as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchMetrics } from '../utils/api';
import { formatCurrency, formatPercentage } from '../utils/formatters';

interface MetricCard {
  label: string;
  value: number;
  change: number;
  format: 'currency' | 'percentage' | 'number';
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricCard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchMetrics('2025-Q1');
        setMetrics(data);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="dashboard-grid">
      {metrics.map((metric, idx) => (
        <div key={idx} className="metric-card">
          <h3>{metric.label}</h3>
          <span className="value">
            {metric.format === 'currency'
              ? formatCurrency(metric.value)
              : metric.format === 'percentage'
              ? formatPercentage(metric.value)
              : metric.value.toLocaleString()}
          </span>
          <span className={`change ${metric.change >= 0 ? 'positive' : 'negative'}`}>
            {metric.change >= 0 ? '+' : ''}{metric.change}%
          </span>
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
""")

    # src/utils/formatters.ts
    with open(os.path.join(PROJECT_DIR, "src", "utils", "formatters.ts"), "w") as f:
        f.write("""export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
}
""")

    # src/utils/api.ts
    with open(os.path.join(PROJECT_DIR, "src", "utils", "api.ts"), "w") as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.internal.example.com/v2';

export async function fetchMetrics(quarter: string) {
  const response = await axios.get(`${API_BASE}/metrics`, {
    params: { quarter },
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return response.data;
}

export async function fetchCampaigns(status?: string) {
  const response = await axios.get(`${API_BASE}/campaigns`, {
    params: status ? { status } : {},
  });
  return response.data;
}

function getToken(): string {
  return localStorage.getItem('auth_token') || '';
}
""")

    # styles
    os.makedirs(os.path.join(PROJECT_DIR, "src", "styles"), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, "src", "styles", "global.css"), "w") as f:
        f.write(""":root {
  --primary-color: #2563eb;
  --secondary-color: #64748b;
  --background: #f8fafc;
  --surface: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-radius: 8px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--background);
  color: var(--text-primary);
  line-height: 1.6;
}

.app-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.metric-card {
  background: var(--surface);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow);
}

.metric-card h3 {
  font-size: 0.875rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-card .value {
  display: block;
  font-size: 1.875rem;
  font-weight: 700;
  margin: 8px 0;
}

.change.positive { color: #16a34a; }
.change.negative { color: #dc2626; }
""")

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "strict": True,
            "forceConsistentCasingInFileNames": True,
            "noFallthroughCasesInSwitch": True,
            "module": "esnext",
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    with open(os.path.join(PROJECT_DIR, "tsconfig.json"), "w") as f:
        json.dump(tsconfig, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {
            "browser": True,
            "es2021": True,
            "node": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:react/recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaFeatures": {"jsx": True},
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "no-unused-vars": "warn",
            "react/react-in-jsx-scope": "off"
        }
    }
    with open(os.path.join(PROJECT_DIR, ".eslintrc.json"), "w") as f:
        json.dump(eslintrc, f, indent=2)

    print(f"Project files created at: {PROJECT_DIR}")


def setup_vscode_settings():
    """Set up basic VSCode settings WITHOUT language-specific formatter scoped settings."""
    settings = load_settings()
    # Add some basic realistic settings but NO [javascript], [typescript], etc.
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "editor.bracketPairColorization.enabled": True,
        "editor.formatOnSave": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "terminal.integrated.fontSize": 13,
        "explorer.confirmDelete": False,
        "git.enableSmartCommit": True
    })
    save_settings(settings)
    print(f"VSCode settings configured at: {SETTINGS_PATH}")


def main():
    # 1. Create the frontend project files
    create_project_files()

    # 2. Set up basic VSCode settings (no language-scoped formatters)
    setup_vscode_settings()

    # 3. Ensure NO .prettierrc exists in the project
    prettierrc_path = os.path.join(PROJECT_DIR, ".prettierrc")
    if os.path.exists(prettierrc_path):
        os.remove(prettierrc_path)

    # 4. Launch VSCode with the project folder (GUI-ready)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


main()
