"""
Initial Setup: Set up a comprehensive .gitignore file for the workspace using VSCode
Task ID: vscode_lp_092
Domain: libreoffice_calc (VSCode task)

Creates a full-stack project with Python backend, Node.js frontend,
and a minimal .gitignore that only has a few entries.
Many unneeded files (caches, build artifacts, IDE configs) are present
and visible in source control.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_092'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    """Create a realistic full-stack project with minimal .gitignore."""

    # --- Project root ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    subprocess.run(['git', 'init', PROJECT_DIR], check=True)
    subprocess.run(['git', '-C', PROJECT_DIR, 'config', 'user.email', 'dev@example.com'], check=True)
    subprocess.run(['git', '-C', PROJECT_DIR, 'config', 'user.name', 'Developer'], check=True)

    # --- Minimal .gitignore (only a few entries - task is to make it comprehensive) ---
    gitignore_content = """# Temporary files
*.log
tmp/
"""
    write_file(f'{PROJECT_DIR}/.gitignore', gitignore_content)

    # --- Python backend ---
    backend_dir = f'{PROJECT_DIR}/backend'
    os.makedirs(backend_dir, exist_ok=True)

    write_file(f'{backend_dir}/app.py', '''"""Flask API for inventory management system."""
from flask import Flask, jsonify, request
from models import db, Product, Category
import logging

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
db.init_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/api/products", methods=["GET"])
def get_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    products = Product.query.paginate(page=page, per_page=per_page)
    return jsonify({
        "products": [p.to_dict() for p in products.items],
        "total": products.total,
        "pages": products.pages
    })


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Product(
        name=data["name"],
        sku=data["sku"],
        price=data["price"],
        category_id=data.get("category_id")
    )
    db.session.add(product)
    db.session.commit()
    logger.info(f"Created product: {product.name}")
    return jsonify(product.to_dict()), 201


@app.route("/api/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
''')

    write_file(f'{backend_dir}/models.py', '''"""Database models for inventory system."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship("Product", backref="category", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "sku": self.sku,
            "price": self.price, "quantity": self.quantity,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat(),
        }
''')

    write_file(f'{backend_dir}/requirements.txt', '''flask==3.0.2
flask-sqlalchemy==3.1.1
gunicorn==21.2.0
python-dotenv==1.0.1
pytest==8.0.2
requests==2.31.0
''')

    write_file(f'{backend_dir}/test_app.py', '''"""Tests for the inventory API."""
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_get_products_empty(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.get_json()
    assert data["products"] == []
    assert data["total"] == 0


def test_create_product(client):
    response = client.post("/api/products", json={
        "name": "Wireless Mouse", "sku": "WM-001", "price": 29.99
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Wireless Mouse"
    assert data["sku"] == "WM-001"
''')

    # Python cache/artifact files (should be gitignored)
    pycache_dir = f'{backend_dir}/__pycache__'
    os.makedirs(pycache_dir, exist_ok=True)
    write_file(f'{pycache_dir}/app.cpython-311.pyc', 'compiled bytecode placeholder')
    write_file(f'{pycache_dir}/models.cpython-311.pyc', 'compiled bytecode placeholder')

    # .env file with secrets (should be gitignored)
    write_file(f'{backend_dir}/.env', '''DATABASE_URL=postgresql://admin:s3cretPass@db.internal:5432/inventory
SECRET_KEY=a7f2e9c1d84b3067f5e2a9d1c8b74e30
REDIS_URL=redis://cache.internal:6379/0
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
''')

    # venv directory (should be gitignored)
    venv_dir = f'{backend_dir}/venv'
    os.makedirs(f'{venv_dir}/lib/python3.11/site-packages', exist_ok=True)
    write_file(f'{venv_dir}/pyvenv.cfg', '''home = /usr/bin
include-system-site-packages = false
version = 3.11.7
''')
    write_file(f'{venv_dir}/lib/python3.11/site-packages/flask/__init__.py', '# flask package')

    # .pytest_cache (should be gitignored)
    pytest_cache = f'{backend_dir}/.pytest_cache'
    os.makedirs(f'{pytest_cache}/v/cache', exist_ok=True)
    write_file(f'{pytest_cache}/README.md', 'This directory contains pytest cache data.')
    write_file(f'{pytest_cache}/v/cache/lastfailed', '{}')
    write_file(f'{pytest_cache}/.gitignore', '# pytest cache\n*\n')

    # .pyc and .pyo files at backend level
    write_file(f'{backend_dir}/utils.pyc', 'compiled')
    write_file(f'{backend_dir}/helpers.pyo', 'optimized compiled')

    # --- Node.js frontend ---
    frontend_dir = f'{PROJECT_DIR}/frontend'
    os.makedirs(frontend_dir, exist_ok=True)

    write_file(f'{frontend_dir}/package.json', '''{
  "name": "inventory-dashboard",
  "version": "1.2.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src/",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "axios": "^1.6.7",
    "@tanstack/react-query": "^5.20.0",
    "chart.js": "^4.4.1",
    "react-chartjs-2": "^5.2.0"
  },
  "devDependencies": {
    "vite": "^5.1.0",
    "vitest": "^1.3.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.56.0",
    "typescript": "^5.3.3"
  }
}
''')

    write_file(f'{frontend_dir}/src/App.tsx', '''import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Categories from "./pages/Categories";
import Navbar from "./components/Navbar";

function App() {
    return (
        <BrowserRouter>
            <Navbar />
            <main className="container mx-auto px-4 py-8">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/products" element={<Products />} />
                    <Route path="/categories" element={<Categories />} />
                </Routes>
            </main>
        </BrowserRouter>
    );
}

export default App;
''')

    os.makedirs(f'{frontend_dir}/src/pages', exist_ok=True)
    write_file(f'{frontend_dir}/src/pages/Dashboard.tsx', '''import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Bar } from "react-chartjs-2";
import { fetchProducts } from "../api/products";

export default function Dashboard() {
    const { data, isLoading } = useQuery({ queryKey: ["products"], queryFn: fetchProducts });

    if (isLoading) return <div>Loading dashboard...</div>;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Inventory Dashboard</h1>
            <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="bg-white p-4 rounded shadow">
                    <h3>Total Products</h3>
                    <p className="text-3xl font-bold">{data?.total || 0}</p>
                </div>
            </div>
        </div>
    );
}
''')

    os.makedirs(f'{frontend_dir}/src/api', exist_ok=True)
    write_file(f'{frontend_dir}/src/api/products.ts', '''import axios from "axios";

const API_BASE = "/api";

export async function fetchProducts(page = 1) {
    const response = await axios.get(`${API_BASE}/products`, { params: { page } });
    return response.data;
}

export async function createProduct(product: {
    name: string; sku: string; price: number; category_id?: number
}) {
    const response = await axios.post(`${API_BASE}/products`, product);
    return response.data;
}
''')

    os.makedirs(f'{frontend_dir}/src/components', exist_ok=True)
    write_file(f'{frontend_dir}/src/components/Navbar.tsx', '''import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="bg-indigo-600 text-white p-4">
            <div className="container mx-auto flex gap-6">
                <Link to="/" className="font-bold text-lg">Inventory</Link>
                <Link to="/products">Products</Link>
                <Link to="/categories">Categories</Link>
            </div>
        </nav>
    );
}
''')

    # node_modules (should be gitignored)
    nm_dir = f'{frontend_dir}/node_modules'
    os.makedirs(f'{nm_dir}/react/lib', exist_ok=True)
    os.makedirs(f'{nm_dir}/vite/dist', exist_ok=True)
    os.makedirs(f'{nm_dir}/.package-lock.json', exist_ok=True)
    write_file(f'{nm_dir}/react/package.json', '{"name":"react","version":"18.2.0"}')
    write_file(f'{nm_dir}/react/lib/index.js', 'module.exports = require("./react");')
    write_file(f'{nm_dir}/vite/package.json', '{"name":"vite","version":"5.1.0"}')

    # dist/ build output (should be gitignored)
    dist_dir = f'{frontend_dir}/dist'
    os.makedirs(f'{dist_dir}/assets', exist_ok=True)
    write_file(f'{dist_dir}/index.html', '<!DOCTYPE html><html><body><div id="root"></div><script src="assets/main.js"></script></body></html>')
    write_file(f'{dist_dir}/assets/main.js', '// bundled output')
    write_file(f'{dist_dir}/assets/style.css', '/* bundled styles */')

    # build/ directory (should be gitignored)
    build_dir = f'{frontend_dir}/build'
    os.makedirs(build_dir, exist_ok=True)
    write_file(f'{build_dir}/bundle.js', '// old CRA build output')

    # .npm cache (should be gitignored)
    npm_dir = f'{frontend_dir}/.npm'
    os.makedirs(npm_dir, exist_ok=True)
    write_file(f'{npm_dir}/_cacache.json', '{"cache": "data"}')

    # --- IDE configuration files (should be gitignored) ---
    # .vscode directory
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    os.makedirs(vscode_dir, exist_ok=True)
    write_file(f'{vscode_dir}/settings.json', '''{
    "editor.formatOnSave": true,
    "python.defaultInterpreterPath": "./backend/venv/bin/python",
    "typescript.preferences.importModuleSpecifier": "relative"
}
''')
    write_file(f'{vscode_dir}/launch.json', '''{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {"FLASK_APP": "backend/app.py"},
            "args": ["run", "--debug"]
        }
    ]
}
''')

    # .idea directory (JetBrains)
    idea_dir = f'{PROJECT_DIR}/.idea'
    os.makedirs(idea_dir, exist_ok=True)
    write_file(f'{idea_dir}/workspace.xml', '<?xml version="1.0" encoding="UTF-8"?><project version="4"></project>')
    write_file(f'{idea_dir}/modules.xml', '<?xml version="1.0" encoding="UTF-8"?><project version="4"></project>')

    # .swp files (vim swap files, should be gitignored)
    write_file(f'{PROJECT_DIR}/.app.py.swp', 'vim swap file data')
    write_file(f'{PROJECT_DIR}/.models.py.swp', 'vim swap file data')

    # --- OS-specific files (should be gitignored) ---
    write_file(f'{PROJECT_DIR}/.DS_Store', '\x00\x00\x00\x01Bud1')
    write_file(f'{frontend_dir}/.DS_Store', '\x00\x00\x00\x01Bud1')
    write_file(f'{PROJECT_DIR}/Thumbs.db', 'thumbnail cache data')

    # --- Root project files ---
    write_file(f'{PROJECT_DIR}/README.md', '''# Inventory Management System

A full-stack inventory management application with a Flask backend and React frontend.

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture
- **Backend**: Flask REST API with SQLAlchemy ORM
- **Frontend**: React 18 + TypeScript + Vite
- **Database**: SQLite (dev) / PostgreSQL (prod)
''')

    write_file(f'{PROJECT_DIR}/docker-compose.yml', '''version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "5001:5001"
    environment:
      - DATABASE_URL=postgresql://admin:password@db:5432/inventory
    depends_on:
      - db
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: inventory
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
''')

    # Git add and initial commit
    subprocess.run(['git', '-C', PROJECT_DIR, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', PROJECT_DIR, 'commit', '-m', 'Initial project setup'], check=True)

    print(f'Project created: {PROJECT_DIR}')
    print(f'Initial .gitignore has minimal entries (only *.log and tmp/)')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


def write_file(path, content):
    """Write content to a file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


create_project()
