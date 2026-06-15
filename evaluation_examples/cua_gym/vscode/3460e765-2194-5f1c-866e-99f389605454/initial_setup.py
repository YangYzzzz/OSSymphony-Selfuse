"""
Initial Setup: Set up multi-root workspace directories for VSCode
Task ID: vscode_lp_062
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECTS = os.path.join(WORKDIR, 'projects')

# --- Project directory structures ---

def create_api_project():
    """Create a realistic Node.js API project."""
    api_dir = os.path.join(PROJECTS, 'api')
    src_dir = os.path.join(api_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # package.json
    with open(os.path.join(api_dir, 'package.json'), 'w') as f:
        json.dump({
            "name": "fullstack-api",
            "version": "2.1.0",
            "description": "REST API service for the fullstack application",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest --coverage"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "mongoose": "^7.6.3",
                "jsonwebtoken": "^9.0.2",
                "bcryptjs": "^2.4.3",
                "dotenv": "^16.3.1"
            },
            "devDependencies": {
                "jest": "^29.7.0",
                "nodemon": "^3.0.1",
                "supertest": "^6.3.3"
            }
        }, f, indent=2)

    # src/index.js
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/users', require('./routes/users'));
app.use('/api/products', require('./routes/products'));

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/fullstack')
    .then(() => {
        app.listen(PORT, () => {
            console.log(`API server running on port ${PORT}`);
        });
    })
    .catch(err => console.error('Database connection failed:', err));
""")

    # src/routes directory
    routes_dir = os.path.join(src_dir, 'routes')
    os.makedirs(routes_dir, exist_ok=True)

    with open(os.path.join(routes_dir, 'auth.js'), 'w') as f:
        f.write("""const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
        // Authentication logic
        const token = jwt.sign({ email }, process.env.JWT_SECRET, { expiresIn: '24h' });
        res.json({ token, user: { email } });
    } catch (err) {
        res.status(401).json({ error: 'Invalid credentials' });
    }
});

router.post('/register', async (req, res) => {
    const { email, password, name } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 12);
        res.status(201).json({ message: 'User registered successfully' });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

module.exports = router;
""")

    # .env.example
    with open(os.path.join(api_dir, '.env.example'), 'w') as f:
        f.write("""PORT=3001
MONGODB_URI=mongodb://localhost:27017/fullstack
JWT_SECRET=your-secret-key-here
NODE_ENV=development
""")


def create_web_project():
    """Create a realistic React web frontend project."""
    web_dir = os.path.join(PROJECTS, 'web')
    src_dir = os.path.join(web_dir, 'src')
    components_dir = os.path.join(src_dir, 'components')
    os.makedirs(components_dir, exist_ok=True)

    # package.json
    with open(os.path.join(web_dir, 'package.json'), 'w') as f:
        json.dump({
            "name": "fullstack-web",
            "version": "1.4.0",
            "description": "React frontend for the fullstack application",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "lint": "eslint src/"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.18.0",
                "axios": "^1.6.0",
                "@mui/material": "^5.14.18",
                "@emotion/react": "^11.11.1",
                "@emotion/styled": "^11.11.0"
            },
            "devDependencies": {
                "react-scripts": "5.0.1",
                "eslint": "^8.53.0",
                "@testing-library/react": "^14.1.0"
            }
        }, f, indent=2)

    # src/App.jsx
    with open(os.path.join(src_dir, 'App.jsx'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import ProductList from './components/ProductList';
import Login from './components/Login';

function App() {
    return (
        <BrowserRouter>
            <Navbar />
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

    # src/components/Dashboard.jsx
    with open(os.path.join(components_dir, 'Dashboard.jsx'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

export default function Dashboard() {
    const [stats, setStats] = useState({ users: 0, products: 0, revenue: 0 });

    useEffect(() => {
        axios.get(`${API_BASE}/stats`)
            .then(res => setStats(res.data))
            .catch(err => console.error('Failed to load stats:', err));
    }, []);

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="stats-grid">
                <div className="stat-card">
                    <h3>Total Users</h3>
                    <p>{stats.users}</p>
                </div>
                <div className="stat-card">
                    <h3>Products</h3>
                    <p>{stats.products}</p>
                </div>
                <div className="stat-card">
                    <h3>Revenue</h3>
                    <p>${stats.revenue.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
}
""")

    # src/components/Navbar.jsx
    with open(os.path.join(components_dir, 'Navbar.jsx'), 'w') as f:
        f.write("""import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-brand">
                <Link to="/">Fullstack App</Link>
            </div>
            <ul className="nav-links">
                <li><Link to="/">Dashboard</Link></li>
                <li><Link to="/products">Products</Link></li>
                <li><Link to="/login">Login</Link></li>
            </ul>
        </nav>
    );
}
""")


def create_shared_project():
    """Create a realistic shared utilities library."""
    shared_dir = os.path.join(PROJECTS, 'shared')
    src_dir = os.path.join(shared_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # package.json
    with open(os.path.join(shared_dir, 'package.json'), 'w') as f:
        json.dump({
            "name": "@fullstack/shared",
            "version": "1.0.3",
            "description": "Shared utilities, types, and constants for the fullstack monorepo",
            "main": "src/index.js",
            "scripts": {
                "test": "jest",
                "build": "tsc"
            },
            "dependencies": {
                "date-fns": "^2.30.0",
                "zod": "^3.22.4"
            },
            "devDependencies": {
                "typescript": "^5.2.2",
                "jest": "^29.7.0"
            }
        }, f, indent=2)

    # src/index.js
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write("""const { formatCurrency, formatDate } = require('./formatters');
const { validateEmail, validatePassword } = require('./validators');
const { API_ENDPOINTS, STATUS_CODES } = require('./constants');

module.exports = {
    formatCurrency,
    formatDate,
    validateEmail,
    validatePassword,
    API_ENDPOINTS,
    STATUS_CODES,
};
""")

    # src/validators.js
    with open(os.path.join(src_dir, 'validators.js'), 'w') as f:
        f.write("""function validateEmail(email) {
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    if (password.length < 8) return { valid: false, error: 'Password must be at least 8 characters' };
    if (!/[A-Z]/.test(password)) return { valid: false, error: 'Password must contain an uppercase letter' };
    if (!/[0-9]/.test(password)) return { valid: false, error: 'Password must contain a number' };
    return { valid: true };
}

module.exports = { validateEmail, validatePassword };
""")

    # src/formatters.js
    with open(os.path.join(src_dir, 'formatters.js'), 'w') as f:
        f.write("""const { format, parseISO } = require('date-fns');

function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency,
    }).format(amount);
}

function formatDate(dateString, pattern = 'MMM dd, yyyy') {
    const date = typeof dateString === 'string' ? parseISO(dateString) : dateString;
    return format(date, pattern);
}

module.exports = { formatCurrency, formatDate };
""")

    # src/constants.js
    with open(os.path.join(src_dir, 'constants.js'), 'w') as f:
        f.write("""const API_ENDPOINTS = {
    AUTH: '/api/auth',
    USERS: '/api/users',
    PRODUCTS: '/api/products',
    STATS: '/api/stats',
};

const STATUS_CODES = {
    SUCCESS: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    NOT_FOUND: 404,
    SERVER_ERROR: 500,
};

module.exports = { API_ENDPOINTS, STATUS_CODES };
""")


def launch_gui(command, delay_sec=1.0):
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


def main():
    # Create all three project directories with content
    create_api_project()
    print(f'Created: {PROJECTS}/api/')

    create_web_project()
    print(f'Created: {PROJECTS}/web/')

    create_shared_project()
    print(f'Created: {PROJECTS}/shared/')

    # Open VSCode with the api project as workspace (initial state)
    launch_gui(f'code "{PROJECTS}/api"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/projects/api/ as workspace')


main()
