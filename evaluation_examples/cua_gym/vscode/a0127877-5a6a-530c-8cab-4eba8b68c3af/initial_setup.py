"""
Initial Setup: Create project scaffold for Playwright offline-behavior test task
Task ID: vscode_gf3_085
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_085'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
TESTS_DIR = f'{PROJECT_DIR}/tests'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(TESTS_DIR, exist_ok=True)
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{SRC_DIR}/components', exist_ok=True)
    os.makedirs(f'{SRC_DIR}/api', exist_ok=True)

    # package.json with playwright and other realistic dependencies
    package_json = {
        "name": "webapp",
        "version": "1.2.0",
        "description": "Progressive web application with offline support",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "test": "playwright test",
            "test:ui": "playwright test --ui",
            "lint": "eslint src --ext .ts,.tsx"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "@playwright/test": "^1.40.1",
            "@types/react": "^18.2.43",
            "@types/react-dom": "^18.2.17",
            "typescript": "^5.3.3",
            "vite": "^5.0.8",
            "@vitejs/plugin-react": "^4.2.1",
            "eslint": "^8.55.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": True,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": True,
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx",
            "strict": True,
            "noUnusedLocals": True,
            "noUnusedParameters": True,
            "noFallthroughCasesInSwitch": True
        },
        "include": ["src"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # playwright.config.ts
    playwright_config = '''import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
'''
    with open(f'{PROJECT_DIR}/playwright.config.ts', 'w') as f:
        f.write(playwright_config)

    # src/App.tsx - main application component with offline handling
    app_tsx = '''import { useState, useEffect, useCallback } from 'react';
import { fetchDashboardData, DashboardData } from './api/client';
import { OfflineBanner } from './components/OfflineBanner';
import { Dashboard } from './components/Dashboard';

function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isOffline, setIsOffline] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setError(null);
      const result = await fetchDashboardData();
      setData(result);
      setIsOffline(false);
    } catch (err) {
      setIsOffline(true);
      setError('Unable to connect to the server');
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleRetry = () => {
    loadData();
  };

  return (
    <div className="app">
      <header>
        <h1>Analytics Dashboard</h1>
      </header>
      {isOffline && <OfflineBanner onRetry={handleRetry} />}
      {error && !isOffline && <p className="error">{error}</p>}
      {data && <Dashboard data={data} />}
    </div>
  );
}

export default App;
'''
    with open(f'{SRC_DIR}/App.tsx', 'w') as f:
        f.write(app_tsx)

    # src/api/client.ts - API client
    api_client = '''import axios from 'axios';

export interface DashboardData {
  totalUsers: number;
  activeUsers: number;
  revenue: number;
  recentOrders: Array<{
    id: string;
    customer: string;
    amount: number;
    status: string;
  }>;
}

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

export async function fetchDashboardData(): Promise<DashboardData> {
  const response = await api.get<DashboardData>('/dashboard');
  return response.data;
}

export async function fetchUserProfile(userId: string) {
  const response = await api.get(`/users/${userId}`);
  return response.data;
}
'''
    with open(f'{SRC_DIR}/api/client.ts', 'w') as f:
        f.write(api_client)

    # src/components/OfflineBanner.tsx
    offline_banner = '''import React from 'react';

interface OfflineBannerProps {
  onRetry: () => void;
}

export const OfflineBanner: React.FC<OfflineBannerProps> = ({ onRetry }) => {
  return (
    <div className="offline-banner" role="alert" aria-live="assertive">
      <span className="offline-icon">&#9888;</span>
      <p>You are currently offline. Some features may be unavailable.</p>
      <button className="retry-button" onClick={onRetry}>
        Retry Connection
      </button>
    </div>
  );
};
'''
    with open(f'{SRC_DIR}/components/OfflineBanner.tsx', 'w') as f:
        f.write(offline_banner)

    # src/components/Dashboard.tsx
    dashboard = '''import React from 'react';
import { DashboardData } from '../api/client';

interface DashboardProps {
  data: DashboardData;
}

export const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-value">{data.totalUsers.toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <h3>Active Users</h3>
          <p className="stat-value">{data.activeUsers.toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <h3>Revenue</h3>
          <p className="stat-value">${data.revenue.toLocaleString()}</p>
        </div>
      </div>
      <div className="recent-orders">
        <h2>Recent Orders</h2>
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.recentOrders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.customer}</td>
                <td>${order.amount.toFixed(2)}</td>
                <td className={`status-${order.status}`}>{order.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
'''
    with open(f'{SRC_DIR}/components/Dashboard.tsx', 'w') as f:
        f.write(dashboard)

    # Existing test file (navigation test, NOT the target test)
    existing_test = '''import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should navigate to dashboard from home', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Analytics Dashboard');
  });

  test('should display header with correct title', async ({ page }) => {
    await page.goto('/');
    const header = page.locator('header h1');
    await expect(header).toBeVisible();
    await expect(header).toHaveText('Analytics Dashboard');
  });

  test('should show loading state initially', async ({ page }) => {
    await page.goto('/');
    // The dashboard should eventually load or show offline state
    await expect(page.locator('.app')).toBeVisible();
  });
});
'''
    with open(f'{TESTS_DIR}/navigation.spec.ts', 'w') as f:
        f.write(existing_test)

    # .gitignore
    gitignore = '''node_modules/
dist/
test-results/
playwright-report/
.env
.env.local
*.tsbuildinfo
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # vite.config.ts
    vite_config = '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
});
'''
    with open(f'{PROJECT_DIR}/vite.config.ts', 'w') as f:
        f.write(vite_config)

    print(f'Project scaffold created at: {PROJECT_DIR}')
    print(f'Tests directory: {TESTS_DIR}')
    print(f'Existing test: {TESTS_DIR}/navigation.spec.ts')
    print(f'Target file (NOT created): {TESTS_DIR}/offline-behavior.spec.ts')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
