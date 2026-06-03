"""
Initial Setup: Create a large full-stack project in VSCode without workspace settings
Task ID: vscode_file_076
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_076'
PROJECT_DIR = f'{WORKDIR}/fullstack-app'


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

    # .vscode/ directory (exists but empty — no settings.json)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # client/src/
    client_src = os.path.join(PROJECT_DIR, 'client', 'src')
    os.makedirs(client_src, exist_ok=True)

    # client/node_modules/ (exists as directory)
    node_modules = os.path.join(PROJECT_DIR, 'client', 'node_modules')
    os.makedirs(node_modules, exist_ok=True)
    # Add some fake node module dirs for realism
    os.makedirs(os.path.join(node_modules, 'react'), exist_ok=True)
    os.makedirs(os.path.join(node_modules, 'typescript'), exist_ok=True)

    # server/src/
    server_src = os.path.join(PROJECT_DIR, 'server', 'src')
    os.makedirs(server_src, exist_ok=True)

    # server/__pycache__/ (exists as directory)
    pycache = os.path.join(PROJECT_DIR, 'server', '__pycache__')
    os.makedirs(pycache, exist_ok=True)

    # .git/ directory (exists as directory)
    git_dir = os.path.join(PROJECT_DIR, '.git')
    os.makedirs(os.path.join(git_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(git_dir, 'refs'), exist_ok=True)

    # --- Create project files ---

    # client/src/App.tsx
    app_tsx = """import React, { useState, useEffect } from 'react';
import './App.css';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface Product {
  id: number;
  title: string;
  price: number;
  category: string;
  inStock: boolean;
}

const App: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'users' | 'products'>('users');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersRes = await fetch('/api/users');
        const productsRes = await fetch('/api/products');
        const usersData = await usersRes.json();
        const productsData = await productsRes.json();
        setUsers(usersData);
        setProducts(productsData);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="app">
      <header className="app-header">
        <h1>FullStack Dashboard</h1>
        <nav>
          <button onClick={() => setActiveTab('users')}>Users</button>
          <button onClick={() => setActiveTab('products')}>Products</button>
        </nav>
      </header>
      <main>
        {activeTab === 'users' ? (
          <section>
            <h2>Team Members ({users.length})</h2>
            <table>
              <thead>
                <tr><th>Name</th><th>Email</th><th>Role</th></tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id}>
                    <td>{u.name}</td>
                    <td>{u.email}</td>
                    <td>{u.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        ) : (
          <section>
            <h2>Products ({products.length})</h2>
            <div className="product-grid">
              {products.map(p => (
                <div key={p.id} className="product-card">
                  <h3>{p.title}</h3>
                  <p>Price: ${p.price.toFixed(2)}</p>
                  <p>Category: {p.category}</p>
                  <span className={p.inStock ? 'in-stock' : 'out-of-stock'}>
                    {p.inStock ? 'In Stock' : 'Out of Stock'}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default App;
"""
    with open(os.path.join(client_src, 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # client/package.json
    package_json = {
        "name": "fullstack-app-client",
        "version": "1.0.0",
        "description": "React TypeScript frontend for fullstack application",
        "main": "src/index.tsx",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src --ext .ts,.tsx"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "axios": "^1.3.4"
        },
        "devDependencies": {
            "typescript": "^4.9.5",
            "@types/react": "^18.0.28",
            "@types/react-dom": "^18.0.11",
            "eslint": "^8.35.0",
            "@typescript-eslint/parser": "^5.54.1"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'client', 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # server/src/app.py
    app_py = """#!/usr/bin/env python3
\"\"\"
FullStack Application Backend
Flask REST API serving users and products data
\"\"\"

from flask import Flask, jsonify, request, abort
from dataclasses import dataclass, asdict
from typing import List, Optional
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory data store (replace with database in production)
users_db = [
    {"id": 1, "name": "Sarah Chen", "email": "s.chen@company.com", "role": "Engineering Lead"},
    {"id": 2, "name": "Marcus Johnson", "email": "m.johnson@company.com", "role": "Senior Developer"},
    {"id": 3, "name": "Priya Patel", "email": "p.patel@company.com", "role": "DevOps Engineer"},
    {"id": 4, "name": "Lucas Oliveira", "email": "l.oliveira@company.com", "role": "Frontend Developer"},
    {"id": 5, "name": "Aisha Kamara", "email": "a.kamara@company.com", "role": "QA Engineer"},
]

products_db = [
    {"id": 1, "title": "Analytics Dashboard Pro", "price": 299.99, "category": "Software", "inStock": True},
    {"id": 2, "title": "Cloud Storage Plan - 1TB", "price": 9.99, "category": "Infrastructure", "inStock": True},
    {"id": 3, "title": "CI/CD Pipeline Toolkit", "price": 149.00, "category": "DevTools", "inStock": False},
    {"id": 4, "title": "Security Audit Module", "price": 499.00, "category": "Security", "inStock": True},
    {"id": 5, "title": "Performance Monitor", "price": 79.95, "category": "Monitoring", "inStock": True},
]


@app.route('/api/users', methods=['GET'])
def get_users():
    \"\"\"Return all users.\"\"\"
    logger.info('GET /api/users - returning %d users', len(users_db))
    return jsonify(users_db)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    \"\"\"Return a single user by ID.\"\"\"
    user = next((u for u in users_db if u['id'] == user_id), None)
    if user is None:
        abort(404, description=f'User {user_id} not found')
    return jsonify(user)


@app.route('/api/products', methods=['GET'])
def get_products():
    \"\"\"Return all products, optionally filtered by category.\"\"\"
    category = request.args.get('category')
    if category:
        filtered = [p for p in products_db if p['category'].lower() == category.lower()]
        return jsonify(filtered)
    logger.info('GET /api/products - returning %d products', len(products_db))
    return jsonify(products_db)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    \"\"\"Return a single product by ID.\"\"\"
    product = next((p for p in products_db if p['id'] == product_id), None)
    if product is None:
        abort(404, description=f'Product {product_id} not found')
    return jsonify(product)


@app.route('/api/health', methods=['GET'])
def health_check():
    \"\"\"Health check endpoint.\"\"\"
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    logger.info('Starting server on port %d (debug=%s)', port, debug)
    app.run(host='0.0.0.0', port=port, debug=debug)
"""
    with open(os.path.join(server_src, 'app.py'), 'w') as f:
        f.write(app_py)

    # server/requirements.txt
    requirements_txt = """Flask==2.3.2
Werkzeug==2.3.6
gunicorn==21.2.0
python-dotenv==1.0.0
flask-cors==4.0.0
marshmallow==3.20.1
SQLAlchemy==2.0.19
psycopg2-binary==2.9.7
redis==4.6.0
celery==5.3.1
pytest==7.4.0
pytest-flask==1.2.0
black==23.7.0
flake8==6.1.0
mypy==1.5.1
"""
    with open(os.path.join(PROJECT_DIR, 'server', 'requirements.txt'), 'w') as f:
        f.write(requirements_txt)

    # .env file
    env_content = """# Environment Configuration
# DO NOT commit this file to version control

# Application
NODE_ENV=development
PORT=3000
API_URL=http://localhost:5001

# Database
DATABASE_URL=postgresql://admin:devpassword@localhost:5432/fullstack_dev
REDIS_URL=redis://localhost:6379/0

# Authentication
JWT_SECRET=dev-secret-key-change-in-production
JWT_EXPIRES_IN=7d

# External APIs
STRIPE_API_KEY=sk_test_placeholder
SENDGRID_API_KEY=SG.placeholder

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_NOTIFICATIONS=false
"""
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # Add a fake git config to make .git look realistic
    git_config = """[core]
\trepositoryformatversion = 0
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
[remote "origin"]
\turl = https://github.com/example-org/fullstack-app.git
\tfetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
\tremote = origin
\tmerge = refs/heads/main
[user]
\tname = Dev User
\temail = dev@company.com
"""
    with open(os.path.join(git_dir, 'config'), 'w') as f:
        f.write(git_config)

    # Add a .gitignore
    gitignore = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo

# Build outputs
build/
dist/
*.egg-info/

# Environment
.env
.env.local
.env.production

# IDE
.vscode/settings.json
.idea/

# Logs
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'  .vscode/ directory exists (empty — no settings.json)')
    print(f'  client/src/App.tsx created')
    print(f'  client/package.json created')
    print(f'  server/src/app.py created')
    print(f'  server/requirements.txt created')
    print(f'  .env created')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
