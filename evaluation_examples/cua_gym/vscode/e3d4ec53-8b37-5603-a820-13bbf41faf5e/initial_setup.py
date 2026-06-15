"""
Initial Setup: Configure absolute imports in a Next.js project
Task ID: vscode_gf5_021
Domain: vscode

Creates a Next.js 13 project at ~/projects/next-app with:
- jsconfig.json (no path aliases)
- next.config.js (basic config)
- Three source files using deep relative imports
- Opens VSCode with the project
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_021'
PROJECT_DIR = f'{WORKDIR}/projects/next-app'
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


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f'  Created: {path}')


def create_initial():
    # ========================================
    # Project root config files
    # ========================================

    # package.json
    create_file(f'{PROJECT_DIR}/package.json', json.dumps({
        "name": "next-app",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "13.5.6",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "eslint": "^8.50.0",
            "eslint-config-next": "13.5.6"
        }
    }, indent=2))

    # jsconfig.json — exists but NO path aliases (task requires adding them)
    create_file(f'{PROJECT_DIR}/jsconfig.json', json.dumps({
        "compilerOptions": {
            "target": "es2020",
            "module": "esnext",
            "moduleResolution": "node",
            "jsx": "preserve",
            "strict": False
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules"]
    }, indent=2))

    # next.config.js — basic config
    create_file(f'{PROJECT_DIR}/next.config.js', """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
""")

    # .eslintrc.json
    create_file(f'{PROJECT_DIR}/.eslintrc.json', json.dumps({
        "extends": "next/core-web-vitals"
    }, indent=2))

    # ========================================
    # Shared components
    # ========================================

    create_file(f'{SRC_DIR}/components/Button.js', """import React from 'react';

export default function Button({ children, variant = 'primary', onClick, disabled = false }) {
  const baseStyles = 'px-4 py-2 rounded-md font-medium transition-colors duration-200';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
""")

    create_file(f'{SRC_DIR}/components/Header.js', """import React from 'react';

export default function Header({ title, subtitle }) {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="mt-2 text-sm text-gray-600">{subtitle}</p>}
      </div>
    </header>
  );
}
""")

    create_file(f'{SRC_DIR}/components/Card.js', """import React from 'react';

export default function Card({ title, description, footer, children }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {description && <p className="mt-1 text-sm text-gray-500">{description}</p>}
        <div className="mt-4">{children}</div>
      </div>
      {footer && (
        <div className="px-6 py-3 bg-gray-50 border-t">
          {footer}
        </div>
      )}
    </div>
  );
}
""")

    # ========================================
    # Shared utils
    # ========================================

    create_file(f'{SRC_DIR}/utils/api.js', """const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.example.com/v1';

export async function fetchData(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function postData(endpoint, data) {
  return fetchData(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function buildQueryString(params) {
  return Object.entries(params)
    .filter(([_, value]) => value !== undefined && value !== null)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
}
""")

    create_file(f'{SRC_DIR}/utils/formatters.js', """export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

export function truncateText(text, maxLength = 100) {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trimEnd() + '...';
}
""")

    # ========================================
    # Pages with DEEP RELATIVE IMPORTS (the 3 files to refactor)
    # ========================================

    # File 1: src/pages/dashboard/analytics/index.js
    # Uses ../../components/... and ../../utils/...
    create_file(f'{SRC_DIR}/pages/dashboard/analytics/index.js', """import React, { useEffect, useState } from 'react';
import Header from '../../../components/Header';
import Card from '../../../components/Card';
import { fetchData } from '../../../utils/api';
import { formatCurrency, formatDate } from '../../../utils/formatters';

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const data = await fetchData('/analytics/metrics');
        setMetrics(data);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    }
    loadMetrics();
  }, []);

  if (loading) return <div className="p-8 text-center">Loading analytics...</div>;

  return (
    <div>
      <Header title="Analytics Dashboard" subtitle="Track your key performance indicators" />
      <div className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Total Revenue" description="Last 30 days">
          <p className="text-3xl font-bold text-green-600">
            {metrics ? formatCurrency(metrics.revenue) : '$0.00'}
          </p>
        </Card>
        <Card title="Active Users" description="Current month">
          <p className="text-3xl font-bold text-blue-600">
            {metrics ? metrics.activeUsers.toLocaleString() : '0'}
          </p>
        </Card>
        <Card title="Last Updated">
          <p className="text-sm text-gray-500">
            {metrics ? formatDate(metrics.lastUpdated) : 'N/A'}
          </p>
        </Card>
      </div>
    </div>
  );
}
""")

    # File 2: src/pages/settings/profile/edit.js
    # Uses ../../components/... and ../../utils/...
    create_file(f'{SRC_DIR}/pages/settings/profile/edit.js', """import React, { useState } from 'react';
import Header from '../../../components/Header';
import Button from '../../../components/Button';
import { postData } from '../../../utils/api';

export default function EditProfilePage() {
  const [formData, setFormData] = useState({
    displayName: '',
    email: '',
    bio: '',
    timezone: 'America/New_York',
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await postData('/users/profile', formData);
      setMessage('Profile updated successfully!');
    } catch (error) {
      setMessage('Failed to update profile. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header title="Edit Profile" subtitle="Update your personal information" />
      <div className="max-w-2xl mx-auto px-4 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Display Name</label>
            <input
              type="text" name="displayName" value={formData.displayName}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email" name="email" value={formData.email}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Bio</label>
            <textarea
              name="bio" value={formData.bio} onChange={handleChange}
              rows={4}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
          </div>
          {message && <p className="text-sm text-green-600">{message}</p>}
          <Button variant="primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </form>
      </div>
    </div>
  );
}
""")

    # File 3: src/pages/products/inventory/overview.js
    # Uses ../../components/... and ../../utils/...
    create_file(f'{SRC_DIR}/pages/products/inventory/overview.js', """import React, { useEffect, useState } from 'react';
import Header from '../../../components/Header';
import Card from '../../../components/Card';
import Button from '../../../components/Button';
import { fetchData } from '../../../utils/api';
import { formatCurrency } from '../../../utils/formatters';

export default function InventoryOverview() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProducts() {
      try {
        const data = await fetchData('/products/inventory');
        setProducts(data.items || []);
      } catch (error) {
        console.error('Failed to load inventory:', error);
      } finally {
        setLoading(false);
      }
    }
    loadProducts();
  }, []);

  const totalValue = products.reduce((sum, p) => sum + p.price * p.quantity, 0);
  const lowStockItems = products.filter((p) => p.quantity < 10);

  if (loading) return <div className="p-8 text-center">Loading inventory...</div>;

  return (
    <div>
      <Header title="Inventory Overview" subtitle="Manage your product stock levels" />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card title="Total Inventory Value">
            <p className="text-2xl font-bold text-green-600">{formatCurrency(totalValue)}</p>
          </Card>
          <Card title="Low Stock Alerts">
            <p className="text-2xl font-bold text-red-600">{lowStockItems.length} items</p>
          </Card>
        </div>
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {products.map((product) => (
                <tr key={product.sku}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{product.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{product.sku}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatCurrency(product.price)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{product.quantity}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Button variant="secondary">Edit</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""")

    # ========================================
    # Additional supporting files for realism
    # ========================================

    # Layout component
    create_file(f'{SRC_DIR}/components/Layout.js', """import React from 'react';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-indigo-600 text-white px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <span className="text-lg font-semibold">Next App</span>
          <div className="space-x-4">
            <a href="/dashboard" className="hover:text-indigo-200">Dashboard</a>
            <a href="/products" className="hover:text-indigo-200">Products</a>
            <a href="/settings" className="hover:text-indigo-200">Settings</a>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
}
""")

    # Index page
    create_file(f'{SRC_DIR}/pages/index.js', """import React from 'react';
import Layout from '../components/Layout';
import Header from '../components/Header';

export default function HomePage() {
  return (
    <Layout>
      <Header title="Welcome to Next App" subtitle="Your business management platform" />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <p className="text-gray-600">Select a section from the navigation above to get started.</p>
      </div>
    </Layout>
  );
}
""")

    # _app.js
    create_file(f'{SRC_DIR}/pages/_app.js', """import '../styles/globals.css';

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
""")

    # Global styles
    create_file(f'{SRC_DIR}/styles/globals.css', """@tailwind base;
@tailwind components;
@tailwind utilities;

html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}

* {
  box-sizing: border-box;
}
""")

    # README
    create_file(f'{PROJECT_DIR}/README.md', """# Next App

A Next.js 13 business management application.

## Getting Started

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
  components/   - Reusable UI components
  pages/        - Next.js page routes
  utils/        - Utility functions and helpers
  styles/       - Global CSS styles
```
""")

    print(f'Initial project created at: {PROJECT_DIR}')

    # ========================================
    # GUI-ready startup: Open VSCode with the project
    # ========================================
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
