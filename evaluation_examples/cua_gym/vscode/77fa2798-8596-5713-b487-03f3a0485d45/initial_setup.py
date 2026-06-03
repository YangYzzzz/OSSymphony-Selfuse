"""
Initial Setup: Create a JavaScript monorepo directory structure for workspace generation task.
Task ID: vscode_gf3_015
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_015'
MONOREPO = f'{WORKDIR}/projects/monorepo'

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
    # --- Root monorepo ---
    os.makedirs(MONOREPO, exist_ok=True)

    # Root package.json (Yarn Workspaces style)
    root_pkg = {
        "name": "acme-monorepo",
        "version": "1.0.0",
        "private": True,
        "workspaces": [
            "packages/*"
        ],
        "scripts": {
            "build": "echo 'Building all packages...'",
            "test": "echo 'Running tests across packages...'"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "eslint": "^8.56.0",
            "prettier": "^3.2.4"
        }
    }
    with open(f'{MONOREPO}/package.json', 'w') as f:
        json.dump(root_pkg, f, indent=2)

    # --- packages/frontend ---
    frontend_dir = f'{MONOREPO}/packages/frontend'
    os.makedirs(f'{frontend_dir}/src/components', exist_ok=True)

    frontend_pkg = {
        "name": "@acme/frontend",
        "version": "0.4.2",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@acme/shared": "workspace:*"
        },
        "devDependencies": {
            "@types/react": "^18.2.48",
            "vite": "^5.0.12"
        },
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        }
    }
    with open(f'{frontend_dir}/package.json', 'w') as f:
        json.dump(frontend_pkg, f, indent=2)

    with open(f'{frontend_dir}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import { formatCurrency, validateEmail } from '@acme/shared';
import App from './components/App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

console.log('Frontend loaded successfully');
console.log('Sample format:', formatCurrency(1299.99));
""")

    with open(f'{frontend_dir}/src/components/App.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        setProducts(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load products:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="app-container">
      <header>
        <h1>Acme Store</h1>
        <nav>
          <a href="/products">Products</a>
          <a href="/cart">Cart</a>
          <a href="/account">Account</a>
        </nav>
      </header>
      <main>
        {products.map(p => (
          <div key={p.id} className="product-card">
            <h3>{p.name}</h3>
            <p>{p.price}</p>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;
""")

    # --- packages/backend ---
    backend_dir = f'{MONOREPO}/packages/backend'
    os.makedirs(f'{backend_dir}/src/routes', exist_ok=True)

    backend_pkg = {
        "name": "@acme/backend",
        "version": "0.4.2",
        "private": True,
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "@acme/shared": "workspace:*"
        },
        "devDependencies": {
            "nodemon": "^3.0.3",
            "@types/express": "^4.17.21"
        },
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest"
        }
    }
    with open(f'{backend_dir}/package.json', 'w') as f:
        json.dump(backend_pkg, f, indent=2)

    with open(f'{backend_dir}/src/server.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const { validateEmail, sanitizeInput } = require('@acme/shared');
const productRoutes = require('./routes/products');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.use('/api/products', productRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});
""")

    with open(f'{backend_dir}/src/routes/products.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();

const products = [
  { id: 1, name: 'Wireless Keyboard', price: 79.99, category: 'Electronics' },
  { id: 2, name: 'Ergonomic Mouse', price: 45.50, category: 'Electronics' },
  { id: 3, name: 'USB-C Hub', price: 34.99, category: 'Accessories' },
  { id: 4, name: 'Monitor Stand', price: 129.00, category: 'Furniture' },
  { id: 5, name: 'Desk Lamp', price: 52.75, category: 'Furniture' },
];

router.get('/', (req, res) => {
  const { category } = req.query;
  if (category) {
    return res.json(products.filter(p => p.category === category));
  }
  res.json(products);
});

router.get('/:id', (req, res) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  if (!product) return res.status(404).json({ error: 'Product not found' });
  res.json(product);
});

module.exports = router;
""")

    # --- packages/shared ---
    shared_dir = f'{MONOREPO}/packages/shared'
    os.makedirs(f'{shared_dir}/src', exist_ok=True)

    shared_pkg = {
        "name": "@acme/shared",
        "version": "0.4.2",
        "main": "src/utils.js",
        "dependencies": {},
        "devDependencies": {
            "jest": "^29.7.0"
        },
        "scripts": {
            "test": "jest"
        }
    }
    with open(f'{shared_dir}/package.json', 'w') as f:
        json.dump(shared_pkg, f, indent=2)

    with open(f'{shared_dir}/src/utils.js', 'w') as f:
        f.write("""/**
 * Shared utilities for the Acme monorepo.
 * Used by both frontend and backend packages.
 */

function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

function validateEmail(email) {
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
  return re.test(String(email).toLowerCase());
}

function sanitizeInput(str) {
  return str.replace(/[<>&"']/g, (char) => {
    const map = { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' };
    return map[char];
  });
}

function generateId(prefix = '') {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return prefix ? `${prefix}_${timestamp}${random}` : `${timestamp}${random}`;
}

module.exports = { formatCurrency, validateEmail, sanitizeInput, generateId };
""")

    # --- .gitignore ---
    with open(f'{MONOREPO}/.gitignore', 'w') as f:
        f.write("""node_modules/
dist/
.env
*.log
.DS_Store
""")

    # --- README.md ---
    with open(f'{MONOREPO}/README.md', 'w') as f:
        f.write("""# Acme Monorepo

A JavaScript monorepo managed with Yarn Workspaces.

## Packages

- **@acme/frontend** - React-based storefront UI
- **@acme/backend** - Express API server
- **@acme/shared** - Shared utilities and helpers

## Getting Started

```bash
yarn install
yarn build
```
""")

    # MUST NOT create monorepo.code-workspace (that is the task goal)

    print(f'Monorepo structure created at: {MONOREPO}')

    # GUI-ready: open VSCode on the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
