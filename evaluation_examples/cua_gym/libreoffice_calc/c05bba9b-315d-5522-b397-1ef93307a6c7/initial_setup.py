"""
Initial Setup: Set up frontend workspace for Vue.js project
Task ID: osworld_multi_apps_workspace_init_009
Domain: multi_apps (os + chrome + vscode + nautilus)

Creates ~/Projects/vue-dashboard with realistic Vue.js project structure.
Desktop is idle — Chrome and VSCode are closed. Agent must open everything.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_workspace_init_009'
PROJECT_DIR = f'{WORKDIR}/Projects/vue-dashboard'


def run(cmd, check=False):
    """Run a shell command."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)


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


def create_vue_project():
    """Create a realistic Vue.js 3 + Vite project structure."""

    # Create directory structure
    dirs = [
        PROJECT_DIR,
        f'{PROJECT_DIR}/src',
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/views',
        f'{PROJECT_DIR}/src/assets',
        f'{PROJECT_DIR}/src/router',
        f'{PROJECT_DIR}/src/store',
        f'{PROJECT_DIR}/public',
        f'{PROJECT_DIR}/tests',
        f'{PROJECT_DIR}/tests/unit',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    Path(f'{PROJECT_DIR}/package.json').write_text("""{
  "name": "vue-dashboard",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test:unit": "vitest"
  },
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6",
    "axios": "^1.4.0",
    "chart.js": "^4.3.3",
    "vue-chartjs": "^5.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.1",
    "@vue/test-utils": "^2.4.1",
    "vite": "^4.4.9",
    "vitest": "^0.34.3",
    "eslint": "^8.47.0",
    "eslint-plugin-vue": "^9.17.0"
  }
}
""")

    # vite.config.js
    Path(f'{PROJECT_DIR}/vite.config.js').write_text("""import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    host: true
  }
})
""")

    # .gitignore
    Path(f'{PROJECT_DIR}/.gitignore').write_text("""node_modules/
dist/
.env.local
.env.*.local
*.log
.DS_Store
.vite/
coverage/
""")

    # README.md
    Path(f'{PROJECT_DIR}/README.md').write_text("""# Vue Dashboard

A responsive analytics dashboard built with Vue.js 3 and Vite.

## Features

- Real-time data visualization with Chart.js
- Vue Router for SPA navigation
- Pinia state management
- Axios for API integration
- Responsive layout for desktop and mobile

## Getting Started

```bash
npm install
npm run dev
```

The development server will start at http://localhost:5173.

## Project Structure

```
src/
  components/   - Reusable UI components
  views/        - Page-level components
  router/       - Vue Router configuration
  store/        - Pinia state stores
  assets/       - Static assets (CSS, images)
```

## Build for Production

```bash
npm run build
```
""")

    # src/main.js
    Path(f'{PROJECT_DIR}/src/main.js').write_text("""import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
""")

    # src/App.vue
    Path(f'{PROJECT_DIR}/src/App.vue').write_text("""<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.main-content {
  padding: 24px;
  max-width: 1280px;
  margin: 0 auto;
}
</style>
""")

    # src/assets/main.css
    Path(f'{PROJECT_DIR}/src/assets/main.css').write_text(""":root {
  --primary: #4F46E5;
  --primary-dark: #4338CA;
  --secondary: #10B981;
  --danger: #EF4444;
  --warning: #F59E0B;
  --bg-light: #F9FAFB;
  --text-main: #111827;
  --text-muted: #6B7280;
  --border: #E5E7EB;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

body {
  color: var(--text-main);
  background: var(--bg-light);
}

.card {
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
}
""")

    # src/router/index.js
    Path(f'{PROJECT_DIR}/src/router/index.js').write_text("""import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: () => import('@/views/AnalyticsView.vue')
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/views/UsersView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
""")

    # src/store/dashboard.js
    Path(f'{PROJECT_DIR}/src/store/dashboard.js').write_text("""import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDashboardStore = defineStore('dashboard', () => {
  const metrics = ref({
    totalRevenue: 284750,
    activeUsers: 12483,
    newOrders: 847,
    conversionRate: 3.24
  })

  const revenueHistory = ref([
    { month: 'Jan', value: 42300 },
    { month: 'Feb', value: 38900 },
    { month: 'Mar', value: 51200 },
    { month: 'Apr', value: 47600 },
    { month: 'May', value: 55800 },
    { month: 'Jun', value: 48950 }
  ])

  const totalRevenue = computed(() => metrics.value.totalRevenue)

  function updateMetric(key, value) {
    if (key in metrics.value) {
      metrics.value[key] = value
    }
  }

  return { metrics, revenueHistory, totalRevenue, updateMetric }
})
""")

    # src/components/NavBar.vue
    Path(f'{PROJECT_DIR}/src/components/NavBar.vue').write_text("""<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <span class="brand-icon">📊</span>
      <span class="brand-name">Vue Dashboard</span>
    </div>
    <ul class="navbar-links">
      <li><RouterLink to="/">Dashboard</RouterLink></li>
      <li><RouterLink to="/analytics">Analytics</RouterLink></li>
      <li><RouterLink to="/users">Users</RouterLink></li>
      <li><RouterLink to="/settings">Settings</RouterLink></li>
    </ul>
    <div class="navbar-user">
      <img src="@/assets/avatar.png" alt="User avatar" class="avatar" @error="onAvatarError" />
      <span>Alex Rivera</span>
    </div>
  </nav>
</template>

<script setup>
function onAvatarError(e) {
  e.target.style.display = 'none'
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  background: white;
  padding: 0 24px;
  height: 64px;
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary);
  margin-right: 40px;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 24px;
  flex: 1;
}

.navbar-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.navbar-links a:hover,
.navbar-links a.router-link-active {
  color: var(--primary);
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
}
</style>
""")

    # src/components/MetricCard.vue
    Path(f'{PROJECT_DIR}/src/components/MetricCard.vue').write_text("""<template>
  <div class="metric-card">
    <div class="metric-icon">{{ icon }}</div>
    <div class="metric-info">
      <div class="metric-label">{{ label }}</div>
      <div class="metric-value">{{ formattedValue }}</div>
      <div :class="['metric-change', trend > 0 ? 'positive' : 'negative']">
        {{ trend > 0 ? '+' : '' }}{{ trend }}%
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [Number, String],
  icon: String,
  trend: Number,
  prefix: { type: String, default: '' },
  suffix: { type: String, default: '' }
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return `${props.prefix}${props.value.toLocaleString()}${props.suffix}`
  }
  return props.value
})
</script>

<style scoped>
.metric-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
}

.metric-icon {
  font-size: 2rem;
}

.metric-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.metric-change {
  font-size: 0.8rem;
  font-weight: 600;
}

.positive { color: var(--secondary); }
.negative { color: var(--danger); }
</style>
""")

    # src/views/DashboardView.vue
    Path(f'{PROJECT_DIR}/src/views/DashboardView.vue').write_text("""<template>
  <div class="dashboard">
    <h1 class="page-title">Dashboard Overview</h1>

    <div class="metrics-grid">
      <MetricCard
        label="Total Revenue"
        :value="store.metrics.totalRevenue"
        icon="💰"
        :trend="12.5"
        prefix="$"
      />
      <MetricCard
        label="Active Users"
        :value="store.metrics.activeUsers"
        icon="👥"
        :trend="8.3"
      />
      <MetricCard
        label="New Orders"
        :value="store.metrics.newOrders"
        icon="🛒"
        :trend="-2.1"
      />
      <MetricCard
        label="Conversion Rate"
        :value="store.metrics.conversionRate"
        icon="📈"
        :trend="0.7"
        suffix="%"
      />
    </div>

    <div class="charts-row">
      <div class="card chart-card">
        <h2>Revenue Trend</h2>
        <Bar :data="revenueChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import MetricCard from '@/components/MetricCard.vue'
import { useDashboardStore } from '@/store/dashboard'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useDashboardStore()

const revenueChartData = computed(() => ({
  labels: store.revenueHistory.map(d => d.month),
  datasets: [{
    label: 'Monthly Revenue ($)',
    data: store.revenueHistory.map(d => d.value),
    backgroundColor: '#4F46E5',
    borderRadius: 4
  }]
}))

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: false }
  },
  scales: {
    y: { beginAtZero: true }
  }
}
</script>

<style scoped>
.dashboard { }

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-main);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.charts-row {
  display: grid;
  gap: 16px;
}

.chart-card h2 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
""")

    # src/views/AnalyticsView.vue
    Path(f'{PROJECT_DIR}/src/views/AnalyticsView.vue').write_text("""<template>
  <div class="analytics">
    <h1 class="page-title">Analytics</h1>
    <p class="placeholder">Detailed analytics coming soon...</p>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-title { font-size: 1.75rem; font-weight: 700; margin-bottom: 16px; }
.placeholder { color: var(--text-muted); }
</style>
""")

    # src/views/UsersView.vue
    Path(f'{PROJECT_DIR}/src/views/UsersView.vue').write_text("""<template>
  <div class="users">
    <h1 class="page-title">Users</h1>
    <div class="card">
      <table class="users-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Last Active</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td><span :class="['badge', user.role]">{{ user.role }}</span></td>
            <td><span :class="['status', user.status]">{{ user.status }}</span></td>
            <td>{{ user.lastActive }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const users = ref([
  { id: 1, name: 'Sarah Chen', email: 'sarah.chen@company.io', role: 'admin', status: 'active', lastActive: '2 min ago' },
  { id: 2, name: 'Marcus Johnson', email: 'marcus.j@company.io', role: 'editor', status: 'active', lastActive: '1 hr ago' },
  { id: 3, name: 'Priya Patel', email: 'priya.p@company.io', role: 'viewer', status: 'inactive', lastActive: '3 days ago' },
  { id: 4, name: 'Tom Eriksson', email: 'tom.e@company.io', role: 'editor', status: 'active', lastActive: '15 min ago' },
  { id: 5, name: 'Aiko Tanaka', email: 'aiko.t@company.io', role: 'admin', status: 'active', lastActive: 'just now' },
])
</script>

<style scoped>
.page-title { font-size: 1.75rem; font-weight: 700; margin-bottom: 16px; }
.users-table { width: 100%; border-collapse: collapse; }
.users-table th { text-align: left; padding: 10px; color: var(--text-muted); border-bottom: 1px solid var(--border); font-size: 0.85rem; text-transform: uppercase; }
.users-table td { padding: 12px 10px; border-bottom: 1px solid var(--border); }
.badge { padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.badge.admin { background: #EDE9FE; color: #6D28D9; }
.badge.editor { background: #D1FAE5; color: #065F46; }
.badge.viewer { background: #E5E7EB; color: #374151; }
.status { font-size: 0.85rem; }
.status.active { color: var(--secondary); }
.status.inactive { color: var(--text-muted); }
</style>
""")

    # src/views/SettingsView.vue
    Path(f'{PROJECT_DIR}/src/views/SettingsView.vue').write_text("""<template>
  <div class="settings">
    <h1 class="page-title">Settings</h1>
    <div class="card settings-form">
      <h2>Profile Settings</h2>
      <div class="form-group">
        <label>Display Name</label>
        <input type="text" v-model="profile.name" placeholder="Your name" />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" v-model="profile.email" placeholder="your@email.com" />
      </div>
      <div class="form-group">
        <label>Theme</label>
        <select v-model="profile.theme">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System Default</option>
        </select>
      </div>
      <button class="btn btn-primary" @click="saveSettings">Save Changes</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const profile = ref({
  name: 'Alex Rivera',
  email: 'alex.rivera@company.io',
  theme: 'light'
})

function saveSettings() {
  alert('Settings saved!')
}
</script>

<style scoped>
.page-title { font-size: 1.75rem; font-weight: 700; margin-bottom: 16px; }
.settings-form h2 { margin-bottom: 20px; font-size: 1.1rem; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 6px; }
.form-group input,
.form-group select { width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius); font-size: 0.95rem; }
</style>
""")

    # tests/unit/dashboard.test.js
    Path(f'{PROJECT_DIR}/tests/unit/dashboard.test.js').write_text("""import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useDashboardStore } from '@/store/dashboard'

describe('Dashboard Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with correct metrics', () => {
    const store = useDashboardStore()
    expect(store.metrics.totalRevenue).toBe(284750)
    expect(store.metrics.activeUsers).toBe(12483)
    expect(store.metrics.newOrders).toBe(847)
  })

  it('updates metric values correctly', () => {
    const store = useDashboardStore()
    store.updateMetric('newOrders', 900)
    expect(store.metrics.newOrders).toBe(900)
  })

  it('computes totalRevenue correctly', () => {
    const store = useDashboardStore()
    expect(store.totalRevenue).toBe(284750)
  })

  it('has revenue history with 6 months', () => {
    const store = useDashboardStore()
    expect(store.revenueHistory).toHaveLength(6)
  })
})
""")

    # public/index.html
    Path(f'{PROJECT_DIR}/public/favicon.ico').write_bytes(b'')  # placeholder

    # index.html (Vite root)
    Path(f'{PROJECT_DIR}/index.html').write_text("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
""")

    # .env.example
    Path(f'{PROJECT_DIR}/.env.example').write_text("""# Copy to .env.local and fill in your values
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_TITLE=Vue Dashboard
VITE_ENABLE_ANALYTICS=false
""")

    print(f'Vue.js project created at: {PROJECT_DIR}')


def close_existing_apps():
    """Ensure Chrome, VSCode, Nautilus, and terminal are not running."""
    # Use -x for exact process name match to avoid killing the running Python script
    apps_to_kill = [
        'google-chrome',
        'chromium',
        'chromium-browser',
        'code',
        'nautilus',
        'gnome-terminal',
        'xterm',
    ]
    for app in apps_to_kill:
        subprocess.run(['pkill', '-x', app], capture_output=True)
    time.sleep(1.5)


def setup_initial():
    # 1. Ensure apps are closed
    close_existing_apps()

    # 2. Create the Vue.js project
    create_vue_project()

    # NOTE: Desktop is intentionally idle — the task requires the agent to open:
    #   - Nautilus to ~/Projects/vue-dashboard
    #   - Terminal with cwd ~/Projects/vue-dashboard
    #   - VSCode with ~/Projects/vue-dashboard
    #   - Chrome with vuejs.org/guide and vitejs.dev/guide/
    print('Initial state ready: ~/Projects/vue-dashboard exists, desktop is idle.')
    print('Agent must open Nautilus, Terminal, VSCode, and Chrome.')


setup_initial()
