"""
Initial Setup: Configure ESLint extension settings in VSCode
Task ID: vscode_we_055
Domain: vscode (eslint configuration)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_055'
WORKSPACE = f'{WORKDIR}/workspace'
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


def create_vue_project():
    """Create a realistic Vue.js project structure."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.2.0",
        "private": True,
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "lint": "eslint . --ext .vue,.js,.ts"
        },
        "dependencies": {
            "vue": "^3.4.15",
            "vue-router": "^4.2.5",
            "pinia": "^2.1.7"
        },
        "devDependencies": {
            "vite": "^5.0.11",
            "@vitejs/plugin-vue": "^5.0.3",
            "eslint": "^9.0.0",
            "eslint-plugin-vue": "^9.20.1",
            "typescript": "^5.3.3",
            "@typescript-eslint/parser": "^6.19.0",
            "@typescript-eslint/eslint-plugin": "^6.19.0"
        }
    }
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # eslint.config.js (flat config style)
    eslint_config = """import pluginVue from 'eslint-plugin-vue';
import tseslint from 'typescript-eslint';

export default [
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    rules: {
      'no-unused-vars': 'warn',
      'vue/multi-word-component-names': 'off',
    },
  },
];
"""
    with open(os.path.join(WORKSPACE, 'eslint.config.js'), 'w') as f:
        f.write(eslint_config)

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
            "baseUrl": ".",
            "paths": {
                "@/*": ["src/*"]
            }
        },
        "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.vue"]
    }
    with open(os.path.join(WORKSPACE, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Create src directory structure
    src_dir = os.path.join(WORKSPACE, 'src')
    os.makedirs(os.path.join(src_dir, 'components'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'views'), exist_ok=True)
    os.makedirs(os.path.join(src_dir, 'stores'), exist_ok=True)

    # main.ts
    main_ts = """import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount('#app');
"""
    with open(os.path.join(src_dir, 'main.ts'), 'w') as f:
        f.write(main_ts)

    # App.vue
    app_vue = """<template>
  <div id="app">
    <nav class="sidebar">
      <h2>Inventory Dashboard</h2>
      <router-link to="/">Overview</router-link>
      <router-link to="/products">Products</router-link>
      <router-link to="/reports">Reports</router-link>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// App root component
</script>

<style>
#app {
  display: flex;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}
.sidebar {
  width: 240px;
  background: #1a1a2e;
  color: #e0e0e0;
  padding: 1.5rem;
}
.content {
  flex: 1;
  padding: 2rem;
  background: #f5f5f5;
}
</style>
"""
    with open(os.path.join(src_dir, 'App.vue'), 'w') as f:
        f.write(app_vue)

    # ProductList.vue component
    product_list_vue = """<template>
  <div class="product-list">
    <h3>Product Inventory</h3>
    <table>
      <thead>
        <tr>
          <th>SKU</th>
          <th>Name</th>
          <th>Category</th>
          <th>Stock</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.sku">
          <td>{{ product.sku }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.category }}</td>
          <td :class="{ 'low-stock': product.stock < 10 }">{{ product.stock }}</td>
          <td>${{ product.price.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useInventoryStore } from '../stores/inventory';

const store = useInventoryStore();
const products = computed(() => store.products);
</script>

<style scoped>
.product-list table {
  width: 100%;
  border-collapse: collapse;
}
.low-stock {
  color: #e74c3c;
  font-weight: bold;
}
</style>
"""
    with open(os.path.join(src_dir, 'components', 'ProductList.vue'), 'w') as f:
        f.write(product_list_vue)

    # inventory store (TypeScript)
    inventory_store = """import { defineStore } from 'pinia';

interface Product {
  sku: string;
  name: string;
  category: string;
  stock: number;
  price: number;
}

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    products: [
      { sku: 'WH-2041', name: 'Wireless Headphones', category: 'Electronics', stock: 45, price: 79.99 },
      { sku: 'KB-1023', name: 'Mechanical Keyboard', category: 'Electronics', stock: 8, price: 149.50 },
      { sku: 'MG-3301', name: 'Ceramic Travel Mug', category: 'Kitchen', stock: 120, price: 24.95 },
      { sku: 'CH-4410', name: 'Ergonomic Office Chair', category: 'Furniture', stock: 3, price: 399.00 },
      { sku: 'LP-5502', name: 'LED Desk Lamp', category: 'Office', stock: 67, price: 45.00 },
    ] as Product[],
  }),
  getters: {
    lowStockProducts: (state) => state.products.filter(p => p.stock < 10),
    totalValue: (state) => state.products.reduce((sum, p) => sum + p.stock * p.price, 0),
  },
});
"""
    with open(os.path.join(src_dir, 'stores', 'inventory.ts'), 'w') as f:
        f.write(inventory_store)

    # utils.js (plain JavaScript file)
    utils_js = """/**
 * Format currency values for display.
 * @param {number} amount
 * @returns {string}
 */
export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

/**
 * Calculate percentage change between two values.
 */
export function percentChange(oldVal, newVal) {
  if (oldVal === 0) return newVal > 0 ? 100 : 0;
  return ((newVal - oldVal) / oldVal) * 100;
}
"""
    with open(os.path.join(src_dir, 'utils.js'), 'w') as f:
        f.write(utils_js)

    print(f'Vue.js project created at {WORKSPACE}')


def setup_vscode_settings():
    """Set up empty VSCode user settings."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Start with empty settings - the task is to configure ESLint
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json created at {SETTINGS_PATH}')


def install_eslint_extension():
    """Ensure ESLint extension is installed."""
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    if 'dbaeumer.vscode-eslint' not in result.stdout:
        subprocess.run(
            ['code', '--install-extension', 'dbaeumer.vscode-eslint', '--force'],
            capture_output=True, text=True
        )
        print('ESLint extension installed')
    else:
        print('ESLint extension already installed')


def main():
    create_vue_project()
    setup_vscode_settings()
    install_eslint_extension()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
