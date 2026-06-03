"""
Initial Setup: Configure a tasks.json background watch task for webpack dev server
Task ID: vscode_td_035
Domain: vscode

Creates a Next.js project with package.json containing a "dev" script using webpack dev server.
No .vscode/tasks.json exists yet — the agent must create it.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_035'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'next-app')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'pages'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # package.json with dev script using webpack dev server
    package_json = {
        "name": "next-app",
        "version": "1.2.0",
        "private": True,
        "description": "Internal dashboard for Meridian Analytics",
        "scripts": {
            "dev": "webpack serve --mode development --config webpack.config.js",
            "build": "webpack --mode production --config webpack.config.js",
            "lint": "eslint src/ --ext .js,.jsx,.ts,.tsx",
            "test": "jest --coverage",
            "start": "node dist/server.js"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "chart.js": "^4.4.1",
            "dayjs": "^1.11.10"
        },
        "devDependencies": {
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4",
            "webpack-dev-server": "^4.15.1",
            "babel-loader": "^9.1.3",
            "@babel/core": "^7.23.6",
            "@babel/preset-env": "^7.23.6",
            "@babel/preset-react": "^7.23.3",
            "@babel/preset-typescript": "^7.23.3",
            "typescript": "^5.3.3",
            "ts-loader": "^9.5.1",
            "css-loader": "^6.8.1",
            "style-loader": "^3.3.3",
            "html-webpack-plugin": "^5.6.0",
            "eslint": "^8.56.0",
            "jest": "^29.7.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # webpack.config.js
    webpack_config = """const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.[contenthash].js',
    clean: true,
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true,
  },
};
"""
    with open(os.path.join(PROJECT_DIR, 'webpack.config.js'), 'w') as f:
        f.write(webpack_config)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "moduleResolution": "node",
            "jsx": "react-jsx",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "outDir": "./dist",
            "rootDir": "./src",
            "baseUrl": ".",
            "paths": {
                "@components/*": ["src/components/*"],
                "@pages/*": ["src/pages/*"]
            }
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # src/index.tsx
    index_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.tsx'), 'w') as f:
        f.write(index_tsx)

    # src/App.tsx
    app_tsx = """import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # src/pages/Dashboard.tsx
    dashboard = """import React, { useEffect, useState } from 'react';
import axios from 'axios';
import MetricCard from '../components/MetricCard';

interface DashboardMetrics {
  totalRevenue: number;
  activeUsers: number;
  conversionRate: number;
  avgSessionDuration: string;
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);

  useEffect(() => {
    axios.get('/api/metrics')
      .then(res => setMetrics(res.data))
      .catch(err => console.error('Failed to load metrics:', err));
  }, []);

  if (!metrics) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h1>Meridian Analytics Dashboard</h1>
      <div className="metrics-grid">
        <MetricCard title="Total Revenue" value={`$${metrics.totalRevenue.toLocaleString()}`} />
        <MetricCard title="Active Users" value={metrics.activeUsers.toString()} />
        <MetricCard title="Conversion Rate" value={`${metrics.conversionRate}%`} />
        <MetricCard title="Avg Session" value={metrics.avgSessionDuration} />
      </div>
    </div>
  );
};

export default Dashboard;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'pages', 'Dashboard.tsx'), 'w') as f:
        f.write(dashboard)

    # src/pages/Reports.tsx
    reports = """import React from 'react';

const Reports: React.FC = () => {
  return (
    <div className="reports">
      <h1>Monthly Reports</h1>
      <p>Select a date range to generate analytics reports.</p>
    </div>
  );
};

export default Reports;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'pages', 'Reports.tsx'), 'w') as f:
        f.write(reports)

    # src/components/MetricCard.tsx
    metric_card = """import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value }) => {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <span className="metric-value">{value}</span>
    </div>
  );
};

export default MetricCard;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'MetricCard.tsx'), 'w') as f:
        f.write(metric_card)

    # src/styles/global.css
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'styles'), exist_ok=True)
    css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f7fa;
  color: #2d3748;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}

.metric-card h3 {
  font-size: 0.875rem;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  margin-top: 0.5rem;
  color: #1a202c;
}

.loading {
  text-align: center;
  padding: 4rem;
  color: #a0aec0;
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'styles', 'global.css'), 'w') as f:
        f.write(css)

    # public/index.html
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Meridian Analytics</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write(html)

    # .gitignore
    gitignore = """node_modules/
dist/
.env
.env.local
coverage/
*.log
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # Ensure NO .vscode directory exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'No .vscode/tasks.json exists (confirmed)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
