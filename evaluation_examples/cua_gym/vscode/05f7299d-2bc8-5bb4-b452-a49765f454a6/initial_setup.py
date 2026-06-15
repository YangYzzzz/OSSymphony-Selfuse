"""
Initial Setup: Fix compound launch configuration typo in VSCode
Task ID: vscode_fix_056
Domain: vscode

Creates a fullstack-app project with .vscode/launch.json containing:
- Two individual debug configs: 'Backend' (Node.js) and 'Frontend' (Chrome)
- A compound 'Full Stack' config with a typo: 'backend' instead of 'Backend'
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_056'
PROJECT_DIR = os.path.join(WORKDIR, 'fullstack-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    # Create project directories
    os.makedirs(os.path.join(PROJECT_DIR, 'backend'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'frontend', 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'frontend', 'public'), exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- Root package.json ---
    root_package = {
        "name": "fullstack-app",
        "version": "1.0.0",
        "description": "Full-stack application with Node.js backend and React frontend",
        "scripts": {
            "start:backend": "cd backend && node server.js",
            "start:frontend": "cd frontend && npm start",
            "dev": "concurrently \"npm run start:backend\" \"npm run start:frontend\""
        },
        "devDependencies": {
            "concurrently": "^8.2.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(root_package, f, indent=2)

    # --- Backend files ---
    backend_package = {
        "name": "fullstack-app-backend",
        "version": "1.0.0",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.2"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'backend', 'package.json'), 'w') as f:
        json.dump(backend_package, f, indent=2)

    server_js = '''\
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// In-memory product catalog
const products = [
    { id: 1, name: 'Wireless Headphones', price: 79.99, category: 'Electronics', stock: 45 },
    { id: 2, name: 'Running Shoes', price: 129.50, category: 'Sports', stock: 23 },
    { id: 3, name: 'Organic Coffee Beans', price: 18.75, category: 'Food', stock: 120 },
    { id: 4, name: 'Desk Lamp', price: 34.99, category: 'Home', stock: 67 },
    { id: 5, name: 'Yoga Mat', price: 25.00, category: 'Sports', stock: 89 },
];

app.get('/api/products', (req, res) => {
    const { category } = req.query;
    if (category) {
        return res.json(products.filter(p => p.category === category));
    }
    res.json(products);
});

app.get('/api/products/:id', (req, res) => {
    const product = products.find(p => p.id === parseInt(req.params.id));
    if (!product) return res.status(404).json({ error: 'Product not found' });
    res.json(product);
});

app.post('/api/orders', (req, res) => {
    const { productId, quantity } = req.body;
    const product = products.find(p => p.id === productId);
    if (!product) return res.status(404).json({ error: 'Product not found' });
    if (product.stock < quantity) return res.status(400).json({ error: 'Insufficient stock' });
    product.stock -= quantity;
    res.status(201).json({ orderId: Date.now(), product: product.name, quantity, total: product.price * quantity });
});

app.listen(PORT, () => {
    console.log(`Backend server running on http://localhost:${PORT}`);
});
'''
    with open(os.path.join(PROJECT_DIR, 'backend', 'server.js'), 'w') as f:
        f.write(server_js)

    # --- Frontend files ---
    frontend_package = {
        "name": "fullstack-app-frontend",
        "version": "1.0.0",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "axios": "^1.6.2"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version"]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'frontend', 'package.json'), 'w') as f:
        json.dump(frontend_package, f, indent=2)

    app_js = '''\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:3001/api';

function App() {
    const [products, setProducts] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProducts();
    }, [selectedCategory]);

    const fetchProducts = async () => {
        setLoading(true);
        try {
            const url = selectedCategory
                ? `${API_BASE}/products?category=${selectedCategory}`
                : `${API_BASE}/products`;
            const response = await axios.get(url);
            setProducts(response.data);
        } catch (error) {
            console.error('Failed to fetch products:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleOrder = async (productId) => {
        try {
            const response = await axios.post(`${API_BASE}/orders`, {
                productId,
                quantity: 1
            });
            alert(`Order placed! Total: $${response.data.total.toFixed(2)}`);
            fetchProducts();
        } catch (error) {
            alert(error.response?.data?.error || 'Order failed');
        }
    };

    return (
        <div className="App">
            <h1>Product Catalog</h1>
            <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}>
                <option value="">All Categories</option>
                <option value="Electronics">Electronics</option>
                <option value="Sports">Sports</option>
                <option value="Food">Food</option>
                <option value="Home">Home</option>
            </select>
            {loading ? (
                <p>Loading products...</p>
            ) : (
                <div className="product-grid">
                    {products.map(product => (
                        <div key={product.id} className="product-card">
                            <h3>{product.name}</h3>
                            <p className="price">${product.price.toFixed(2)}</p>
                            <p className="stock">In stock: {product.stock}</p>
                            <button onClick={() => handleOrder(product.id)}>
                                Add to Cart
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default App;
'''
    with open(os.path.join(PROJECT_DIR, 'frontend', 'src', 'App.js'), 'w') as f:
        f.write(app_js)

    index_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Product Catalog</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
'''
    with open(os.path.join(PROJECT_DIR, 'frontend', 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    # --- .vscode/launch.json (with typo in compound config) ---
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Backend",
                "type": "node",
                "request": "launch",
                "program": "${workspaceFolder}/backend/server.js",
                "cwd": "${workspaceFolder}/backend",
                "env": {
                    "PORT": "3001"
                },
                "console": "integratedTerminal",
                "skipFiles": ["<node_internals>/**"]
            },
            {
                "name": "Frontend",
                "type": "chrome",
                "request": "launch",
                "url": "http://localhost:3000",
                "webRoot": "${workspaceFolder}/frontend/src",
                "sourceMapPathOverrides": {
                    "webpack:///src/*": "${webRoot}/*"
                }
            }
        ],
        "compounds": [
            {
                "name": "Full Stack",
                "configurations": ["backend", "Frontend"],
                "stopAll": True,
                "preLaunchTask": "npm: dev"
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'launch.json'), 'w') as f:
        json.dump(launch_json, f, indent=4)

    # --- .vscode/tasks.json ---
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "npm: dev",
                "type": "shell",
                "command": "npm run dev",
                "isBackground": True,
                "problemMatcher": [],
                "group": "build"
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'tasks.json'), 'w') as f:
        json.dump(tasks_json, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'launch.json has typo: compound "Full Stack" references "backend" instead of "Backend"')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
