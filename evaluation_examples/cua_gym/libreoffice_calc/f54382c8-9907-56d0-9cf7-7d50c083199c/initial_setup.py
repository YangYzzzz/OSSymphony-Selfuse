"""
Initial Setup: Create a webapp project with Cypress scaffolding (without the login command)
Task ID: vscode_gf3_050
Domain: vscode (libreoffice_calc label)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_050'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
CYPRESS_DIR = f'{PROJECT_DIR}/cypress'
SUPPORT_DIR = f'{CYPRESS_DIR}/support'

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
    # --- Create project directory structure ---
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/pages', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)
    os.makedirs(f'{CYPRESS_DIR}/e2e', exist_ok=True)
    os.makedirs(f'{CYPRESS_DIR}/fixtures', exist_ok=True)
    os.makedirs(SUPPORT_DIR, exist_ok=True)

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "webapp",
  "version": "2.1.0",
  "private": true,
  "description": "Internal dashboard for Meridian Analytics",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts,.tsx",
    "test": "vitest",
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.12.0",
    "zustand": "^4.4.7",
    "tailwindcss": "^3.3.6"
  },
  "devDependencies": {
    "typescript": "^5.3.2",
    "vite": "^5.0.5",
    "@types/react": "^18.2.41",
    "@types/react-dom": "^18.2.17",
    "cypress": "^13.6.1",
    "eslint": "^8.55.0",
    "vitest": "^1.0.4"
  }
}
""")

    # --- tsconfig.json ---
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

    # --- cypress.config.ts ---
    with open(f'{PROJECT_DIR}/cypress.config.ts', 'w') as f:
        f.write("""import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
  },
})
""")

    # --- cypress/support/e2e.ts (exists but does NOT import commands) ---
    with open(f'{SUPPORT_DIR}/e2e.ts', 'w') as f:
        f.write("""// ***********************************************************
// This file is processed and loaded automatically before
// your test files.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import global styles or utilities if needed
""")

    # --- cypress/support/commands.ts (empty placeholder - no login command) ---
    # Intentionally NOT creating commands.ts - the task asks the agent to create it

    # --- cypress/fixtures/example.json ---
    with open(f'{CYPRESS_DIR}/fixtures/example.json', 'w') as f:
        f.write("""{
  "users": [
    {
      "id": 1,
      "email": "sarah.chen@meridian.io",
      "name": "Sarah Chen",
      "role": "admin"
    },
    {
      "id": 2,
      "email": "marcus.johnson@meridian.io",
      "name": "Marcus Johnson",
      "role": "analyst"
    },
    {
      "id": 3,
      "email": "priya.patel@meridian.io",
      "name": "Priya Patel",
      "role": "viewer"
    }
  ],
  "dashboards": [
    {
      "id": "dash-001",
      "title": "Revenue Overview",
      "owner": "sarah.chen@meridian.io"
    },
    {
      "id": "dash-002",
      "title": "User Engagement Metrics",
      "owner": "marcus.johnson@meridian.io"
    }
  ]
}
""")

    # --- cypress/e2e/dashboard.cy.ts (existing test without cy.login) ---
    with open(f'{CYPRESS_DIR}/e2e/dashboard.cy.ts', 'w') as f:
        f.write("""describe('Dashboard Page', () => {
  beforeEach(() => {
    // TODO: Replace with cy.login() once the custom command is ready
    cy.visit('/login')
    cy.get('[data-testid="email-input"]').type('sarah.chen@meridian.io')
    cy.get('[data-testid="password-input"]').type('SecurePass123!')
    cy.get('[data-testid="login-button"]').click()
    cy.url().should('include', '/dashboard')
  })

  it('should display the revenue overview widget', () => {
    cy.get('[data-testid="revenue-widget"]').should('be.visible')
    cy.get('[data-testid="revenue-total"]').should('contain', '$')
  })

  it('should allow filtering by date range', () => {
    cy.get('[data-testid="date-range-picker"]').click()
    cy.get('[data-testid="preset-last-30"]').click()
    cy.get('[data-testid="revenue-widget"]').should('be.visible')
  })

  it('should navigate to detailed report', () => {
    cy.get('[data-testid="view-details-btn"]').first().click()
    cy.url().should('include', '/reports/')
  })
})
""")

    # --- src/App.tsx ---
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write("""import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import DashboardPage from './pages/DashboardPage'
import LoginPage from './pages/LoginPage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'
import { useAuthStore } from './store/authStore'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 2,
    },
  },
})

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/reports/:id"
            element={
              <ProtectedRoute>
                <ReportsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
""")

    # --- src/api/auth.ts ---
    with open(f'{PROJECT_DIR}/src/api/auth.ts', 'w') as f:
        f.write("""import axios from 'axios'

interface LoginPayload {
  email: string
  password: string
}

interface LoginResponse {
  token: string
  user: {
    id: number
    email: string
    name: string
    role: string
  }
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001'

export async function loginUser(payload: LoginPayload): Promise<LoginResponse> {
  const response = await axios.post<LoginResponse>(`${API_BASE}/api/auth/login`, payload)
  return response.data
}

export async function logoutUser(): Promise<void> {
  const token = localStorage.getItem('auth_token')
  await axios.post(`${API_BASE}/api/auth/logout`, null, {
    headers: { Authorization: `Bearer ${token}` },
  })
  localStorage.removeItem('auth_token')
}

export async function getCurrentUser() {
  const token = localStorage.getItem('auth_token')
  const response = await axios.get(`${API_BASE}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
""")

    # --- src/pages/LoginPage.tsx ---
    os.makedirs(f'{PROJECT_DIR}/src/pages', exist_ok=True)
    with open(f'{PROJECT_DIR}/src/pages/LoginPage.tsx', 'w') as f:
        f.write("""import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../api/auth'
import { useAuthStore } from '../store/authStore'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const { token, user } = await loginUser({ email, password })
      localStorage.setItem('auth_token', token)
      document.cookie = `session=${token}; path=/; max-age=86400`
      setAuth(user, token)
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid email or password. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">Meridian Analytics</h1>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <input
          data-testid="email-input"
          type="email"
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 border rounded mb-4"
        />
        <input
          data-testid="password-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 border rounded mb-4"
        />
        <button
          data-testid="login-button"
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
    </div>
  )
}
""")

    # --- src/store/authStore.ts ---
    os.makedirs(f'{PROJECT_DIR}/src/store', exist_ok=True)
    with open(f'{PROJECT_DIR}/src/store/authStore.ts', 'w') as f:
        f.write("""import { create } from 'zustand'

interface User {
  id: number
  email: string
  name: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setAuth: (user: User, token: string) => void
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  setAuth: (user, token) => set({ user, token, isAuthenticated: true }),
  clearAuth: () => set({ user: null, token: null, isAuthenticated: false }),
}))
""")

    # --- Create placeholder pages ---
    for page in ['DashboardPage', 'ReportsPage', 'SettingsPage']:
        with open(f'{PROJECT_DIR}/src/pages/{page}.tsx', 'w') as f:
            f.write(f"""export default function {page}() {{
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">{page.replace('Page', '')}</h1>
      <p className="mt-4 text-gray-600">Content loading...</p>
    </div>
  )
}}
""")

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
dist/
.env
.env.local
*.log
cypress/videos/
cypress/screenshots/
coverage/
""")

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
