"""
Initial Setup: Multi-root VSCode workspace with React frontend and Node.js backend
Task ID: vscode_wf_014
Domain: libreoffice_calc (actually vscode)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_014'

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
    # --- Create ~/frontend (React project) ---
    frontend_dir = os.path.join(WORKDIR, 'frontend')
    os.makedirs(os.path.join(frontend_dir, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, 'public'), exist_ok=True)

    # package.json for React project
    frontend_pkg = {
        "name": "inventory-dashboard-frontend",
        "version": "1.2.0",
        "private": True,
        "description": "React frontend for inventory management dashboard",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "axios": "^1.6.2",
            "@mui/material": "^5.14.18",
            "@emotion/react": "^11.11.1",
            "@emotion/styled": "^11.11.0"
        },
        "devDependencies": {
            "react-scripts": "5.0.1",
            "@testing-library/react": "^14.1.2",
            "eslint": "^8.54.0",
            "eslint-config-react-app": "^7.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(os.path.join(frontend_dir, 'package.json'), 'w') as f:
        json.dump(frontend_pkg, f, indent=2)

    # src/App.js
    with open(os.path.join(frontend_dir, 'src', 'App.js'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ProductList from './components/ProductList';
import Header from './components/Header';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/products" element={<ProductList />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.js
    with open(os.path.join(frontend_dir, 'src', 'components', 'Dashboard.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({ totalProducts: 0, lowStock: 0, revenue: 0 });

  useEffect(() => {
    axios.get('/api/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error('Failed to fetch stats:', err));
  }, []);

  return (
    <div className="dashboard-container">
      <h1>Inventory Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Products</h3>
          <span>{stats.totalProducts}</span>
        </div>
        <div className="stat-card">
          <h3>Low Stock Alerts</h3>
          <span>{stats.lowStock}</span>
        </div>
        <div className="stat-card">
          <h3>Monthly Revenue</h3>
          <span>${stats.revenue.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
""")

    # src/components/Header.js
    with open(os.path.join(frontend_dir, 'src', 'components', 'Header.js'), 'w') as f:
        f.write("""import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => (
  <nav className="main-nav">
    <div className="logo">InventoryPro</div>
    <ul>
      <li><Link to="/">Dashboard</Link></li>
      <li><Link to="/products">Products</Link></li>
    </ul>
  </nav>
);

export default Header;
""")

    # src/components/ProductList.js
    with open(os.path.join(frontend_dir, 'src', 'components', 'ProductList.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    axios.get('/api/products')
      .then(res => setProducts(res.data))
      .catch(err => console.error('Failed to load products:', err));
  }, []);

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="product-list">
      <h2>Product Inventory</h2>
      <input
        type="text"
        placeholder="Search products..."
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Category</th>
            <th>Price</th>
            <th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(p => (
            <tr key={p.sku}>
              <td>{p.sku}</td>
              <td>{p.name}</td>
              <td>{p.category}</td>
              <td>${p.price.toFixed(2)}</td>
              <td className={p.stock < 10 ? 'low-stock' : ''}>{p.stock}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductList;
""")

    # public/index.html
    with open(os.path.join(frontend_dir, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>InventoryPro Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # --- Create ~/backend (Node.js API project) ---
    backend_dir = os.path.join(WORKDIR, 'backend')
    os.makedirs(os.path.join(backend_dir, 'src', 'routes'), exist_ok=True)
    os.makedirs(os.path.join(backend_dir, 'src', 'models'), exist_ok=True)
    os.makedirs(os.path.join(backend_dir, 'config'), exist_ok=True)

    # package.json for Node.js API
    backend_pkg = {
        "name": "inventory-api-backend",
        "version": "2.0.1",
        "description": "Node.js REST API for inventory management system",
        "main": "src/server.js",
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "mongoose": "^8.0.2",
            "dotenv": "^16.3.1",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0",
            "supertest": "^6.3.3",
            "eslint": "^8.54.0"
        },
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        }
    }
    with open(os.path.join(backend_dir, 'package.json'), 'w') as f:
        json.dump(backend_pkg, f, indent=4)

    # src/server.js
    with open(os.path.join(backend_dir, 'src', 'server.js'), 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const mongoose = require('mongoose');
require('dotenv').config();

const productRoutes = require('./routes/products');
const statsRoutes = require('./routes/stats');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Routes
app.use('/api/products', productRoutes);
app.use('/api/stats', statsRoutes);

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', uptime: process.uptime() });
});

// Database connection
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/inventory';
mongoose.connect(MONGO_URI)
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

app.listen(PORT, () => {
    console.log(`Inventory API running on port ${PORT}`);
});

module.exports = app;
""")

    # src/routes/products.js
    with open(os.path.join(backend_dir, 'src', 'routes', 'products.js'), 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

// GET all products
router.get('/', async (req, res) => {
    try {
        const { category, minStock } = req.query;
        const filter = {};
        if (category) filter.category = category;
        if (minStock) filter.stock = { $gte: parseInt(minStock) };

        const products = await Product.find(filter).sort({ name: 1 });
        res.json(products);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch products' });
    }
});

// POST new product
router.post('/', async (req, res) => {
    try {
        const product = new Product(req.body);
        await product.save();
        res.status(201).json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// PUT update product
router.put('/:id', async (req, res) => {
    try {
        const product = await Product.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true, runValidators: true }
        );
        if (!product) return res.status(404).json({ error: 'Product not found' });
        res.json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

module.exports = router;
""")

    # src/models/Product.js
    with open(os.path.join(backend_dir, 'src', 'models', 'Product.js'), 'w') as f:
        f.write("""const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    sku: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    category: { type: String, required: true },
    price: { type: Number, required: true, min: 0 },
    stock: { type: Number, required: true, min: 0 },
    supplier: { type: String },
    lastRestocked: { type: Date, default: Date.now }
}, {
    timestamps: true
});

productSchema.index({ category: 1, name: 1 });

module.exports = mongoose.model('Product', productSchema);
""")

    # src/routes/stats.js
    with open(os.path.join(backend_dir, 'src', 'routes', 'stats.js'), 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

router.get('/', async (req, res) => {
    try {
        const totalProducts = await Product.countDocuments();
        const lowStock = await Product.countDocuments({ stock: { $lt: 10 } });
        const revenueAgg = await Product.aggregate([
            { $group: { _id: null, total: { $sum: { $multiply: ['$price', '$stock'] } } } }
        ]);
        const revenue = revenueAgg.length > 0 ? revenueAgg[0].total : 0;

        res.json({ totalProducts, lowStock, revenue });
    } catch (err) {
        res.status(500).json({ error: 'Failed to compute stats' });
    }
});

module.exports = router;
""")

    # config/default.json
    with open(os.path.join(backend_dir, 'config', 'default.json'), 'w') as f:
        json.dump({
            "server": {"port": 3001, "host": "0.0.0.0"},
            "database": {"uri": "mongodb://localhost:27017/inventory"},
            "auth": {"jwtSecret": "change-me-in-production", "tokenExpiry": "24h"},
            "logging": {"level": "info", "format": "combined"}
        }, f, indent=4)

    # .env file for backend
    with open(os.path.join(backend_dir, '.env'), 'w') as f:
        f.write("""PORT=3001
MONGO_URI=mongodb://localhost:27017/inventory
JWT_SECRET=dev-secret-key-12345
NODE_ENV=development
""")

    # Make sure NO .code-workspace file exists
    import glob
    for ws_file in glob.glob(os.path.join(WORKDIR, '*.code-workspace')):
        os.remove(ws_file)

    print(f'Initial project structure created in {WORKDIR}')
    print(f'  - {frontend_dir}/ (React project)')
    print(f'  - {backend_dir}/ (Node.js API project)')

    # Launch VSCode (just open the home directory, no workspace)
    launch_gui('code /home/user', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
