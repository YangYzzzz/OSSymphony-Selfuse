"""
Initial Setup: ESLint validate missing Vue file support
Task ID: vscode_fix_060
Domain: vscode

Creates a Vue project workspace with VSCode settings that have
editor.codeActionsOnSave with ESLint fix enabled, but eslint.validate
only includes javascript and typescript (missing vue).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_060'
PROJECT_DIR = os.path.join(WORKDIR, 'vue-dashboard')

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
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


def create_project():
    """Create a realistic Vue project directory structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "vue-dashboard",
        "version": "1.2.0",
        "description": "Internal analytics dashboard for Meridian Corp",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "lint": "eslint . --ext .vue,.js,.ts",
            "preview": "vite preview"
        },
        "dependencies": {
            "vue": "^3.4.15",
            "vue-router": "^4.2.5",
            "pinia": "^2.1.7",
            "axios": "^1.6.5",
            "chart.js": "^4.4.1",
            "vue-chartjs": "^5.3.0"
        },
        "devDependencies": {
            "@vitejs/plugin-vue": "^5.0.3",
            "eslint": "^8.56.0",
            "eslint-plugin-vue": "^9.20.1",
            "@typescript-eslint/parser": "^6.19.0",
            "typescript": "^5.3.3",
            "vite": "^5.0.12"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "root": True,
        "env": {
            "browser": True,
            "es2021": True,
            "node": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:vue/vue3-recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        "parserOptions": {
            "ecmaVersion": "latest",
            "parser": "@typescript-eslint/parser",
            "sourceType": "module"
        },
        "plugins": ["vue", "@typescript-eslint"],
        "rules": {
            "vue/multi-word-component-names": "off",
            "no-unused-vars": "warn",
            "@typescript-eslint/no-explicit-any": "warn"
        }
    }
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "moduleResolution": "bundler",
            "strict": True,
            "jsx": "preserve",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "esModuleInterop": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "skipLibCheck": True,
            "noEmit": True,
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["src/**/*.ts", "src/**/*.vue"],
        "references": [{"path": "./tsconfig.node.json"}]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Create src directory structure
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(os.path.join(src_dir, 'components'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'views'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'stores'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'router'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'types'), exist_ok=True)

    # main.ts
    with open(os.path.join(src_dir, 'main.ts'), 'w') as f:
        f.write("""import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
""")

    # App.vue
    with open(os.path.join(src_dir, 'App.vue'), 'w') as f:
        f.write("""<template>
  <div id="app">
    <nav class="sidebar">
      <div class="logo">
        <h2>Meridian Analytics</h2>
      </div>
      <ul class="nav-links">
        <li><router-link to="/">Dashboard</router-link></li>
        <li><router-link to="/reports">Reports</router-link></li>
        <li><router-link to="/settings">Settings</router-link></li>
      </ul>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// Root app component - layout wrapper
</script>

<style scoped>
#app {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 240px;
  background-color: #1a1a2e;
  color: #e0e0e0;
  padding: 1rem;
}
.content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
}
</style>
""")

    # src/views/DashboardView.vue
    with open(os.path.join(src_dir, 'views', 'DashboardView.vue'), 'w') as f:
        f.write("""<template>
  <div class="dashboard">
    <h1>Analytics Overview</h1>
    <div class="stats-grid">
      <StatCard
        v-for="stat in summaryStats"
        :key="stat.label"
        :label="stat.label"
        :value="stat.value"
        :trend="stat.trend"
      />
    </div>
    <div class="charts-row">
      <RevenueChart :data="revenueData" />
      <UserActivityChart :data="activityData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import StatCard from '@/components/StatCard.vue'
import RevenueChart from '@/components/RevenueChart.vue'
import UserActivityChart from '@/components/UserActivityChart.vue'

const store = useDashboardStore()

const summaryStats = computed(() => store.summaryStats)
const revenueData = computed(() => store.revenueData)
const activityData = computed(() => store.activityData)
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}
</style>
""")

    # src/components/StatCard.vue
    with open(os.path.join(src_dir, 'components', 'StatCard.vue'), 'w') as f:
        f.write("""<template>
  <div class="stat-card">
    <span class="label">{{ label }}</span>
    <span class="value">{{ formattedValue }}</span>
    <span :class="['trend', trend > 0 ? 'up' : 'down']">
      {{ trend > 0 ? '+' : '' }}{{ trend }}%
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  label: string
  value: number
  trend: number
}

const props = defineProps<Props>()

const formattedValue = computed(() => {
  if (props.value >= 1000000) {
    return `$${(props.value / 1000000).toFixed(1)}M`
  }
  if (props.value >= 1000) {
    return `$${(props.value / 1000).toFixed(1)}K`
  }
  return props.value.toString()
})
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.label { font-size: 0.85rem; color: #666; }
.value { font-size: 1.75rem; font-weight: 600; display: block; }
.trend.up { color: #22c55e; }
.trend.down { color: #ef4444; }
</style>
""")

    # src/stores/dashboard.ts
    with open(os.path.join(src_dir, 'stores', 'dashboard.ts'), 'w') as f:
        f.write("""import { defineStore } from 'pinia'

interface SummaryStat {
  label: string
  value: number
  trend: number
}

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    summaryStats: [
      { label: 'Total Revenue', value: 2450000, trend: 12.5 },
      { label: 'Active Users', value: 18420, trend: 8.3 },
      { label: 'Conversion Rate', value: 3.2, trend: -1.1 },
      { label: 'Avg Order Value', value: 127, trend: 5.7 },
    ] as SummaryStat[],
    revenueData: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      values: [380000, 420000, 395000, 460000, 510000, 485000],
    },
    activityData: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      values: [2400, 2800, 3100, 2950, 3200, 1800, 1200],
    },
  }),
})
""")

    # src/types/index.ts
    with open(os.path.join(src_dir, 'types', 'index.ts'), 'w') as f:
        f.write("""export interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'editor' | 'viewer'
  lastActive: string
}

export interface Report {
  id: number
  title: string
  createdAt: string
  author: string
  status: 'draft' | 'published' | 'archived'
}

export interface ChartData {
  labels: string[]
  values: number[]
}
""")

    # vite.config.ts
    with open(os.path.join(PROJECT_DIR, 'vite.config.ts'), 'w') as f:
        f.write("""import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
  },
})
""")

    print(f'Vue project created: {PROJECT_DIR}')


def setup_vscode_settings():
    """Configure VSCode settings with ESLint but missing Vue validation."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Merge our task-specific settings
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.fixAll.eslint": True
        },
        "eslint.validate": ["javascript", "typescript"],
        "eslint.workingDirectories": [{"mode": "auto"}],
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "[vue]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "typescript.tsdk": "node_modules/typescript/lib",
        "files.associations": {
            "*.vue": "vue"
        }
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written: {SETTINGS_PATH}')
    print(f'  eslint.validate = {settings["eslint.validate"]}')


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
