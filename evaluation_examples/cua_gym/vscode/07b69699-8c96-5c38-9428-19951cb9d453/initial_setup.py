"""
Initial Setup: Create a React TypeScript project with 5 components that are used
but not imported in Dashboard.tsx, causing TypeScript errors.
Task ID: vscode_web_088
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_088'
PROJECT_DIR = f'{WORKDIR}/projects/react-ts-app'

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

def create_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def create_initial():
    # --- package.json ---
    package_json = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.3.3"
        },
        "devDependencies": {
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build"
        }
    }
    create_file(f'{PROJECT_DIR}/package.json', json.dumps(package_json, indent=2))

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
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
            "jsx": "react-jsx",
            "baseUrl": "src"
        },
        "include": ["src"]
    }
    create_file(f'{PROJECT_DIR}/tsconfig.json', json.dumps(tsconfig, indent=2))

    # --- src/components/Header.tsx ---
    create_file(f'{PROJECT_DIR}/src/components/Header.tsx', '''import React from 'react';

interface HeaderProps {
  title?: string;
  showNavigation?: boolean;
}

const Header: React.FC<HeaderProps> = ({ title = 'Dashboard', showNavigation = true }) => {
  return (
    <header className="app-header">
      <h1>{title}</h1>
      {showNavigation && (
        <nav>
          <a href="/home">Home</a>
          <a href="/reports">Reports</a>
          <a href="/settings">Settings</a>
        </nav>
      )}
    </header>
  );
};

export default Header;
''')

    # --- src/components/Sidebar.tsx ---
    create_file(f'{PROJECT_DIR}/src/components/Sidebar.tsx', '''import React from 'react';

interface SidebarProps {
  collapsed?: boolean;
  activeItem?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed = false, activeItem = 'dashboard' }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: 'grid' },
    { id: 'analytics', label: 'Analytics', icon: 'chart' },
    { id: 'users', label: 'Users', icon: 'people' },
    { id: 'settings', label: 'Settings', icon: 'gear' },
  ];

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <ul>
        {menuItems.map(item => (
          <li key={item.id} className={item.id === activeItem ? 'active' : ''}>
            <span className={`icon-${item.icon}`} />
            {!collapsed && <span>{item.label}</span>}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
''')

    # --- src/components/Card.tsx ---
    create_file(f'{PROJECT_DIR}/src/components/Card.tsx', '''import React from 'react';

interface CardProps {
  title: string;
  value: string | number;
  trend?: 'up' | 'down' | 'flat';
  description?: string;
}

const Card: React.FC<CardProps> = ({ title, value, trend = 'flat', description }) => {
  const trendColors = { up: '#22c55e', down: '#ef4444', flat: '#6b7280' };

  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <div className="card-value" style={{ color: trendColors[trend] }}>
        {value}
      </div>
      {description && <p className="card-description">{description}</p>}
    </div>
  );
};

export default Card;
''')

    # --- src/components/Chart.tsx ---
    create_file(f'{PROJECT_DIR}/src/components/Chart.tsx', '''import React from 'react';

interface DataPoint {
  label: string;
  value: number;
}

interface ChartProps {
  data: DataPoint[];
  type?: 'bar' | 'line' | 'pie';
  title?: string;
}

const Chart: React.FC<ChartProps> = ({ data, type = 'bar', title }) => {
  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <div className="chart-container">
      {title && <h3 className="chart-title">{title}</h3>}
      <div className={`chart chart-${type}`}>
        {data.map((point, index) => (
          <div key={index} className="chart-bar">
            <div
              className="bar-fill"
              style={{ height: `${(point.value / maxValue) * 100}%` }}
            />
            <span className="bar-label">{point.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chart;
''')

    # --- src/components/Footer.tsx ---
    create_file(f'{PROJECT_DIR}/src/components/Footer.tsx', '''import React from 'react';

interface FooterProps {
  companyName?: string;
  year?: number;
}

const Footer: React.FC<FooterProps> = ({ companyName = 'Acme Corp', year = 2025 }) => {
  return (
    <footer className="app-footer">
      <p>&copy; {year} {companyName}. All rights reserved.</p>
      <div className="footer-links">
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
        <a href="/contact">Contact Us</a>
      </div>
    </footer>
  );
};

export default Footer;
''')

    # --- src/pages/Dashboard.tsx --- (NO imports for the 5 components)
    create_file(f'{PROJECT_DIR}/src/pages/Dashboard.tsx', '''import React from 'react';

// Dashboard page for Acme Corp internal analytics portal
// TODO: Add missing imports for components

const revenueData = [
  { label: 'Jan', value: 42000 },
  { label: 'Feb', value: 38500 },
  { label: 'Mar', value: 51200 },
  { label: 'Apr', value: 47800 },
  { label: 'May', value: 53400 },
  { label: 'Jun', value: 49100 },
];

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-layout">
      <Header title="Analytics Dashboard" showNavigation={true} />
      <div className="main-content">
        <Sidebar activeItem="dashboard" />
        <div className="content-area">
          <div className="metrics-row">
            <Card title="Total Revenue" value="$282,000" trend="up" description="Q1-Q2 2025" />
            <Card title="Active Users" value="12,847" trend="up" description="Monthly active" />
            <Card title="Conversion Rate" value="3.2%" trend="down" description="vs last month" />
            <Card title="Avg Order Value" value="$67.50" trend="flat" description="Last 30 days" />
          </div>
          <Chart data={revenueData} type="bar" title="Monthly Revenue Trend" />
        </div>
      </div>
      <Footer companyName="Acme Corp" year={2025} />
    </div>
  );
};

export default Dashboard;
''')

    # --- src/App.tsx ---
    create_file(f'{PROJECT_DIR}/src/App.tsx', '''import React from 'react';
import Dashboard from './pages/Dashboard';

const App: React.FC = () => {
  return (
    <div className="app">
      <Dashboard />
    </div>
  );
};

export default App;
''')

    # --- src/index.tsx ---
    create_file(f'{PROJECT_DIR}/src/index.tsx', '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Dashboard.tsx at: {PROJECT_DIR}/src/pages/Dashboard.tsx')
    print('Components created: Header, Sidebar, Card, Chart, Footer')
    print('Dashboard.tsx uses all 5 components WITHOUT importing them')

    # GUI-ready: open VSCode with the project folder and the Dashboard.tsx file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{PROJECT_DIR}/src/pages/Dashboard.tsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
