"""
Initial Setup: Configure ESLint + Prettier in VSCode workspace settings
Task ID: vscode_gf3_054
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_054'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
SETTINGS_PATH = f'{VSCODE_DIR}/settings.json'


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
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/hooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # package.json - realistic React project
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "description": "Internal dashboard for Meridian Analytics",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "recharts": "^2.10.3",
            "@mui/material": "^5.15.1",
            "@emotion/react": "^11.11.1",
            "@emotion/styled": "^11.11.0"
        },
        "devDependencies": {
            "eslint": "^8.56.0",
            "eslint-config-prettier": "^9.1.0",
            "eslint-plugin-react": "^7.33.2",
            "eslint-plugin-react-hooks": "^4.6.0",
            "@typescript-eslint/eslint-plugin": "^6.16.0",
            "@typescript-eslint/parser": "^6.16.0",
            "prettier": "^3.1.1",
            "typescript": "^5.3.3",
            "react-scripts": "5.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/ --ext .js,.jsx,.ts,.tsx",
            "format": "prettier --write src/"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

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
            "plugin:react-hooks/recommended",
            "plugin:@typescript-eslint/recommended",
            "prettier"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaFeatures": {"jsx": True},
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "plugins": ["react", "react-hooks", "@typescript-eslint"],
        "rules": {
            "react/react-in-jsx-scope": "off",
            "react/prop-types": "warn",
            "no-unused-vars": "warn",
            "no-console": ["warn", {"allow": ["warn", "error"]}]
        },
        "settings": {
            "react": {"version": "detect"}
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # .prettierrc
    prettierrc = {
        "semi": True,
        "trailingComma": "es5",
        "singleQuote": True,
        "printWidth": 100,
        "tabWidth": 2,
        "useTabs": False,
        "bracketSpacing": True,
        "arrowParens": "always"
    }
    with open(f'{PROJECT_DIR}/.prettierrc', 'w') as f:
        json.dump(prettierrc, f, indent=2)

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
            "noEmit": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # .vscode/settings.json - minimal, NO task-completed elements
    initial_settings = {
        "editor.tabSize": 2,
        "editor.minimap.enabled": False,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(initial_settings, f, indent=4)

    # src/App.tsx - main app component
    app_tsx = '''import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import AnalyticsPanel from './components/AnalyticsPanel';
import { fetchMetrics } from './utils/api';

interface AppState {
  isLoading: boolean;
  error: string | null;
}

function App() {
  const [state, setState] = useState<AppState>({
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    fetchMetrics()
      .then(() => setState({ isLoading: false, error: null }))
      .catch((err) => setState({ isLoading: false, error: err.message }));
  }, []);

  if (state.isLoading) {
    return <div className="loading-spinner">Loading Meridian Analytics...</div>;
  }

  if (state.error) {
    return <div className="error-banner">Error: {state.error}</div>;
  }

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile/:userId" element={<UserProfile />} />
          <Route path="/analytics" element={<AnalyticsPanel />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx)

    # src/components/Dashboard.tsx
    dashboard_tsx = '''import { useState, useEffect } from 'react';
import { fetchDashboardData } from '../utils/api';

interface MetricCard {
  title: string;
  value: number;
  trend: 'up' | 'down' | 'flat';
  percentChange: number;
}

interface DashboardData {
  metrics: MetricCard[];
  lastUpdated: string;
}

function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetchDashboardData().then(setData);
  }, []);

  const renderTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return '\\u2191';
      case 'down':
        return '\\u2193';
      default:
        return '\\u2192';
    }
  };

  if (!data) return <div>Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h1>Meridian Analytics Dashboard</h1>
      <p className="last-updated">Last updated: {data.lastUpdated}</p>
      <div className="metrics-grid">
        {data.metrics.map((metric, index) => (
          <div key={index} className="metric-card">
            <h3>{metric.title}</h3>
            <span className="metric-value">${metric.value.toLocaleString()}</span>
            <span className={`trend trend-${metric.trend}`}>
              {renderTrendIcon(metric.trend)} {metric.percentChange}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
'''
    with open(f'{PROJECT_DIR}/src/components/Dashboard.tsx', 'w') as f:
        f.write(dashboard_tsx)

    # src/utils/api.ts
    api_ts = '''import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.meridian-analytics.io/v2';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function fetchMetrics() {
  const response = await client.get('/metrics/summary');
  return response.data;
}

export async function fetchDashboardData() {
  const response = await client.get('/dashboard');
  return response.data;
}

export async function fetchUserProfile(userId: string) {
  const response = await client.get(`/users/${userId}/profile`);
  return response.data;
}

export async function updateUserPreferences(userId: string, preferences: Record<string, unknown>) {
  const response = await client.put(`/users/${userId}/preferences`, preferences);
  return response.data;
}
'''
    with open(f'{PROJECT_DIR}/src/utils/api.ts', 'w') as f:
        f.write(api_ts)

    # src/hooks/useDebounce.ts
    use_debounce = '''import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

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
    with open(f'{PROJECT_DIR}/src/hooks/useDebounce.ts', 'w') as f:
        f.write(use_debounce)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Meridian Analytics Dashboard</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'VSCode settings at: {SETTINGS_PATH}')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
