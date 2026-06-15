"""
Initial Setup: Create a fullstack project directory structure for Docker debugging task.
Task ID: vscode_gf3_027
Domain: vscode

Creates a realistic fullstack project with backend (Node.js) and frontend directories.
Does NOT create .vscode/launch.json — that is the agent's task.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_027'
PROJECT_DIR = f'{WORKDIR}/projects/fullstack'
BACKEND_SRC = f'{PROJECT_DIR}/backend/src'
FRONTEND_SRC = f'{PROJECT_DIR}/frontend/src'


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
    # Create directory structure
    os.makedirs(BACKEND_SRC, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/backend/tests', exist_ok=True)
    os.makedirs(FRONTEND_SRC, exist_ok=True)
    os.makedirs(f'{FRONTEND_SRC}/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/docker', exist_ok=True)

    # --- Backend package.json ---
    with open(f'{PROJECT_DIR}/backend/package.json', 'w') as f:
        f.write('''{
  "name": "fullstack-backend",
  "version": "1.2.0",
  "description": "REST API for inventory management system",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "debug": "node --inspect=0.0.0.0:9229 src/server.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.6.3",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}
''')

    # --- Backend server.js ---
    with open(f'{BACKEND_SRC}/server.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Routes
const productRoutes = require('./routes/products');
const authRoutes = require('./routes/auth');

app.use('/api/products', productRoutes);
app.use('/api/auth', authRoutes);

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

mongoose.connect(process.env.MONGO_URI || 'mongodb://mongo:27017/inventory')
    .then(() => {
        console.log('Connected to MongoDB');
        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    })
    .catch(err => console.error('MongoDB connection error:', err));
""")

    # --- Backend routes/products.js ---
    os.makedirs(f'{BACKEND_SRC}/routes', exist_ok=True)
    with open(f'{BACKEND_SRC}/routes/products.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

router.get('/', async (req, res) => {
    try {
        const products = await Product.find().sort({ createdAt: -1 });
        res.json(products);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const product = new Product(req.body);
        await product.save();
        res.status(201).json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.put('/:id', async (req, res) => {
    try {
        const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
        res.json(product);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await Product.findByIdAndDelete(req.params.id);
        res.status(204).send();
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
""")

    # --- Backend routes/auth.js ---
    with open(f'{BACKEND_SRC}/routes/auth.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

router.post('/register', async (req, res) => {
    try {
        const { email, password, name } = req.body;
        const hashedPassword = await bcrypt.hash(password, 12);
        const user = new User({ email, password: hashedPassword, name });
        await user.save();
        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '24h' });
        res.status(201).json({ token, user: { id: user._id, email, name } });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user || !(await bcrypt.compare(password, user.password))) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '24h' });
        res.json({ token, user: { id: user._id, email: user.email, name: user.name } });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
""")

    # --- Backend models ---
    os.makedirs(f'{BACKEND_SRC}/models', exist_ok=True)
    with open(f'{BACKEND_SRC}/models/Product.js', 'w') as f:
        f.write("""const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: { type: String, required: true },
    sku: { type: String, required: true, unique: true },
    category: { type: String, required: true },
    price: { type: Number, required: true },
    quantity: { type: Number, default: 0 },
    supplier: { type: String },
    description: { type: String },
}, { timestamps: true });

module.exports = mongoose.model('Product', productSchema);
""")

    with open(f'{BACKEND_SRC}/models/User.js', 'w') as f:
        f.write("""const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    name: { type: String, required: true },
    role: { type: String, enum: ['admin', 'manager', 'viewer'], default: 'viewer' },
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema);
""")

    # --- Backend .env ---
    with open(f'{PROJECT_DIR}/backend/.env', 'w') as f:
        f.write("""PORT=3001
MONGO_URI=mongodb://mongo:27017/inventory
JWT_SECRET=dev-secret-key-change-in-production
""")

    # --- Frontend package.json ---
    with open(f'{PROJECT_DIR}/frontend/package.json', 'w') as f:
        f.write('''{
  "name": "fullstack-frontend",
  "version": "1.2.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
''')

    # --- Frontend App.js ---
    with open(f'{FRONTEND_SRC}/App.js', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ProductList from './components/ProductList';
import Login from './components/Login';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/products" element={<ProductList />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
""")

    # --- Frontend components ---
    with open(f'{FRONTEND_SRC}/components/Dashboard.js', 'w') as f:
        f.write("""import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
    const [stats, setStats] = useState({ total: 0, lowStock: 0 });

    useEffect(() => {
        axios.get('/api/products')
            .then(res => {
                const products = res.data;
                setStats({
                    total: products.length,
                    lowStock: products.filter(p => p.quantity < 10).length
                });
            })
            .catch(console.error);
    }, []);

    return (
        <div className="dashboard">
            <h1>Inventory Dashboard</h1>
            <div className="stats">
                <div className="stat-card">
                    <h3>Total Products</h3>
                    <p>{stats.total}</p>
                </div>
                <div className="stat-card">
                    <h3>Low Stock Alerts</h3>
                    <p>{stats.lowStock}</p>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
""")

    # --- Dockerfile ---
    with open(f'{PROJECT_DIR}/docker/Dockerfile.backend', 'w') as f:
        f.write("""FROM node:18-alpine

WORKDIR /app

COPY backend/package*.json ./
RUN npm ci --only=production

COPY backend/src ./src

EXPOSE 3001 9229

CMD ["node", "--inspect=0.0.0.0:9229", "src/server.js"]
""")

    # --- docker-compose.yml ---
    with open(f'{PROJECT_DIR}/docker-compose.yml', 'w') as f:
        f.write("""version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "3001:3001"
      - "9229:9229"
    volumes:
      - ./backend/src:/app/src
    environment:
      - NODE_ENV=development
      - MONGO_URI=mongodb://mongo:27017/inventory
    depends_on:
      - mongo

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
""")

    # --- Root README ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Fullstack Inventory Management System

A containerized inventory management application with a Node.js/Express backend
and React frontend, using MongoDB for data storage.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)

### Running with Docker
```bash
docker-compose up --build
```

### Development
Backend: `cd backend && npm run dev`
Frontend: `cd frontend && npm start`

## Architecture
- **Backend**: Express.js REST API with JWT authentication
- **Frontend**: React SPA with React Router
- **Database**: MongoDB 7
- **Container**: Docker with hot-reload volumes
""")

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
.env
dist/
build/
*.log
.DS_Store
""")

    print(f'Initial project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
