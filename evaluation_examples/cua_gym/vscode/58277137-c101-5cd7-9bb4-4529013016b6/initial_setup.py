"""
Initial Setup: Configure Emmet className and self-closing tags in VSCode
Task ID: vscode_web_049
Domain: vs_code

Creates a React/TSX project with VSCode open. Emmet is NOT configured for
className or self-closing tags -- those are the task the agent must complete.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_049'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
COMPONENTS_DIR = os.path.join(SRC_DIR, 'components')


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
    # Create directory structure
    for d in [VSCODE_DIR, SRC_DIR, COMPONENTS_DIR]:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.3.3",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

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
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # .vscode/settings.json -- basic workspace settings, NO emmet config
    vscode_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "typescript.tsdk": "node_modules/typescript/lib",
        "files.associations": {
            "*.tsx": "typescriptreact",
            "*.ts": "typescript"
        }
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # src/App.tsx
    app_tsx = '''import React from 'react';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';

function App() {
  return (
    <div className="app-wrapper">
      <Header title="Inventory Manager" />
      <main className="main-content">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
'''
    with open(os.path.join(SRC_DIR, 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # src/index.tsx
    index_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(os.path.join(SRC_DIR, 'index.tsx'), 'w') as f:
        f.write(index_tsx)

    # src/components/Header.tsx
    header_tsx = '''import React from 'react';

interface HeaderProps {
  title: string;
}

export const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <header className="site-header">
      <nav className="nav-bar">
        <h1>{title}</h1>
        <ul className="nav-links">
          <li><a href="/dashboard">Dashboard</a></li>
          <li><a href="/products">Products</a></li>
          <li><a href="/orders">Orders</a></li>
          <li><a href="/settings">Settings</a></li>
        </ul>
      </nav>
      <img src="/logo.png" alt="Company Logo" />
    </header>
  );
};
'''
    with open(os.path.join(COMPONENTS_DIR, 'Header.tsx'), 'w') as f:
        f.write(header_tsx)

    # src/components/Dashboard.tsx
    dashboard_tsx = '''import React, { useState, useEffect } from 'react';

interface Product {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  price: number;
  category: string;
}

const SAMPLE_PRODUCTS: Product[] = [
  { id: 1, name: "Wireless Bluetooth Headphones", sku: "WBH-2024", quantity: 145, price: 79.99, category: "Electronics" },
  { id: 2, name: "Organic Green Tea (50 bags)", sku: "OGT-1050", quantity: 320, price: 14.50, category: "Beverages" },
  { id: 3, name: "Ergonomic Office Chair", sku: "EOC-4400", quantity: 28, price: 349.00, category: "Furniture" },
  { id: 4, name: "Stainless Steel Water Bottle", sku: "SSW-0750", quantity: 512, price: 24.95, category: "Kitchen" },
  { id: 5, name: "LED Desk Lamp", sku: "LDL-3300", quantity: 87, price: 42.00, category: "Electronics" },
  { id: 6, name: "Bamboo Cutting Board Set", sku: "BCS-2200", quantity: 193, price: 32.50, category: "Kitchen" },
  { id: 7, name: "Yoga Mat Premium", sku: "YMP-6600", quantity: 64, price: 55.00, category: "Fitness" },
  { id: 8, name: "Noise Cancelling Earbuds", sku: "NCE-8800", quantity: 210, price: 129.99, category: "Electronics" },
];

export const Dashboard: React.FC = () => {
  const [products] = useState<Product[]>(SAMPLE_PRODUCTS);
  const [filter, setFilter] = useState<string>("");

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(filter.toLowerCase()) ||
    p.category.toLowerCase().includes(filter.toLowerCase())
  );

  const totalValue = filtered.reduce((sum, p) => sum + p.quantity * p.price, 0);

  return (
    <section className="dashboard-container">
      <div className="dashboard-header">
        <h2>Product Inventory</h2>
        <input
          type="text"
          placeholder="Filter by name or category..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="filter-input"
        />
      </div>
      <div className="stats-bar">
        <span>Items: {filtered.length}</span>
        <span>Total Value: ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
      </div>
      <table className="product-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>SKU</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(product => (
            <tr key={product.id}>
              <td>{product.name}</td>
              <td>{product.sku}</td>
              <td>{product.quantity}</td>
              <td>${product.price.toFixed(2)}</td>
              <td>{product.category}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
'''
    with open(os.path.join(COMPONENTS_DIR, 'Dashboard.tsx'), 'w') as f:
        f.write(dashboard_tsx)

    # src/types.ts
    types_ts = '''export interface User {
  id: string;
  email: string;
  displayName: string;
  role: 'admin' | 'manager' | 'viewer';
  lastLogin: Date;
}

export interface OrderItem {
  productId: number;
  quantity: number;
  unitPrice: number;
}

export interface Order {
  orderId: string;
  customer: string;
  items: OrderItem[];
  status: 'pending' | 'processing' | 'shipped' | 'delivered';
  createdAt: Date;
}
'''
    with open(os.path.join(SRC_DIR, 'types.ts'), 'w') as f:
        f.write(types_ts)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Workspace settings at: {os.path.join(VSCODE_DIR, "settings.json")}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
