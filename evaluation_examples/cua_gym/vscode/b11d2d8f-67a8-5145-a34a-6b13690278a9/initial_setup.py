"""
Initial Setup: Create a React app project skeleton for Playwright testing task
Task ID: vscode_gf3_062
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_062'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'

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
    os.makedirs(f'{PROJECT_DIR}/src/pages', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json — realistic React app
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "react-app",
  "version": "1.2.0",
  "private": true,
  "description": "Internal dashboard for Meridian Analytics",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts,.tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.12.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "typescript": "^5.3.2",
    "vite": "^5.0.8"
  }
}
""")

    # tsconfig.json
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        f.write("""{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
""")

    # tsconfig.node.json
    with open(f'{PROJECT_DIR}/tsconfig.node.json', 'w') as f:
        f.write("""{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
""")

    # vite.config.ts
    with open(f'{PROJECT_DIR}/vite.config.ts', 'w') as f:
        f.write("""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
})
""")

    # index.html
    with open(f'{PROJECT_DIR}/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Meridian Analytics Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

    # src/main.tsx
    with open(f'{PROJECT_DIR}/src/main.tsx', 'w') as f:
        f.write("""import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 2,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
""")

    # src/App.tsx
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write("""import { Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Settings from './pages/Settings'
import Layout from './components/Layout'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}

export default App
""")

    # src/index.css
    with open(f'{PROJECT_DIR}/src/index.css', 'w') as f:
        f.write("""*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #1a1a2e;
}

#root {
  min-height: 100vh;
}
""")

    # src/pages/Dashboard.tsx
    with open(f'{PROJECT_DIR}/src/pages/Dashboard.tsx', 'w') as f:
        f.write("""import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface MetricCard {
  label: string
  value: number
  change: number
}

function Dashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: async () => {
      const response = await axios.get<MetricCard[]>('/api/metrics')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="loading-spinner">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="metrics-grid">
        {metrics?.map((metric, index) => (
          <div key={index} className="metric-card">
            <span className="metric-label">{metric.label}</span>
            <span className="metric-value">{metric.value.toLocaleString()}</span>
            <span className={`metric-change ${metric.change >= 0 ? 'positive' : 'negative'}`}>
              {metric.change >= 0 ? '+' : ''}{metric.change}%
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard
""")

    # src/pages/Login.tsx
    with open(f'{PROJECT_DIR}/src/pages/Login.tsx', 'w') as f:
        f.write("""import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    try {
      await axios.post('/api/auth/login', { email, password })
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid email or password. Please try again.')
    }
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Sign in to Meridian Analytics</h2>
        {error && <div className="error-message">{error}</div>}
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
          required
        />
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />
        <button type="submit">Sign In</button>
      </form>
    </div>
  )
}

export default Login
""")

    # src/pages/Settings.tsx
    with open(f'{PROJECT_DIR}/src/pages/Settings.tsx', 'w') as f:
        f.write("""function Settings() {
  return (
    <div className="settings-page">
      <h1>Settings</h1>
      <section>
        <h2>Profile</h2>
        <p>Manage your account settings and preferences.</p>
      </section>
      <section>
        <h2>Notifications</h2>
        <p>Configure email and push notification preferences.</p>
      </section>
    </div>
  )
}

export default Settings
""")

    # src/components/Layout.tsx
    with open(f'{PROJECT_DIR}/src/components/Layout.tsx', 'w') as f:
        f.write("""import { Outlet, Link, useLocation } from 'react-router-dom'

function Layout() {
  const location = useLocation()

  return (
    <div className="app-layout">
      <nav className="sidebar">
        <div className="logo">Meridian Analytics</div>
        <ul>
          <li className={location.pathname === '/dashboard' ? 'active' : ''}>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li className={location.pathname === '/settings' ? 'active' : ''}>
            <Link to="/settings">Settings</Link>
          </li>
        </ul>
      </nav>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
""")

    # .eslintrc.cjs
    with open(f'{PROJECT_DIR}/.eslintrc.cjs', 'w') as f:
        f.write("""module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
""")

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
