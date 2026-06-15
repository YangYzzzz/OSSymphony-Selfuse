"""
Initial Setup: Multi-root workspace with per-folder linter settings
Task ID: vscode_web_041
Domain: vscode

Creates ~/projects/fullstack-app/ with client/ (React) and server/ (Express)
directories containing realistic project files. No .code-workspace file.
Opens VSCode to the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_ROOT = f'{WORKDIR}/projects/fullstack-app'
CLIENT_DIR = f'{PROJECT_ROOT}/client'
SERVER_DIR = f'{PROJECT_ROOT}/server'


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
    os.makedirs(f'{CLIENT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{CLIENT_DIR}/public', exist_ok=True)
    os.makedirs(f'{SERVER_DIR}/routes', exist_ok=True)
    os.makedirs(f'{SERVER_DIR}/middleware', exist_ok=True)
    os.makedirs(f'{SERVER_DIR}/models', exist_ok=True)

    # --- Client (React) files ---

    # client/package.json
    client_pkg = {
        "name": "fullstack-client",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "eslint-plugin-react": "^7.33.2",
            "eslint-plugin-react-hooks": "^4.6.0",
            "@vitejs/plugin-react": "^4.2.1",
            "vite": "^5.0.8"
        },
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "lint": "eslint src/"
        }
    }
    with open(f'{CLIENT_DIR}/package.json', 'w') as f:
        json.dump(client_pkg, f, indent=2)

    # client/.eslintrc.json
    client_eslint = {
        "env": {"browser": True, "es2021": True},
        "extends": ["eslint:recommended", "plugin:react/recommended", "plugin:react-hooks/recommended"],
        "parserOptions": {"ecmaFeatures": {"jsx": True}, "ecmaVersion": "latest", "sourceType": "module"},
        "plugins": ["react", "react-hooks"],
        "rules": {
            "react/react-in-jsx-scope": "off",
            "react-hooks/exhaustive-deps": "warn"
        },
        "settings": {"react": {"version": "detect"}}
    }
    with open(f'{CLIENT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(client_eslint, f, indent=2)

    # client/src/App.jsx
    with open(f'{CLIENT_DIR}/src/App.jsx', 'w') as f:
        f.write("""import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile/:userId" element={<UserProfile />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # client/src/components/Dashboard.jsx
    with open(f'{CLIENT_DIR}/src/components/Dashboard.jsx', 'w') as f:
        f.write("""import { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/metrics')
      .then(res => {
        setMetrics(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load metrics:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="spinner">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Analytics Dashboard</h1>
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Revenue</h3>
          <p>${metrics?.totalRevenue?.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Active Users</h3>
          <p>{metrics?.activeUsers?.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Conversion Rate</h3>
          <p>{metrics?.conversionRate}%</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
""")

    # client/src/components/Navbar.jsx
    with open(f'{CLIENT_DIR}/src/components/Navbar.jsx', 'w') as f:
        f.write("""import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="main-nav">
      <div className="nav-brand">
        <Link to="/">FullStack App</Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/">Dashboard</Link></li>
        <li><Link to="/profile/me">Profile</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
""")

    # client/src/components/UserProfile.jsx
    with open(f'{CLIENT_DIR}/src/components/UserProfile.jsx', 'w') as f:
        f.write("""import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function UserProfile() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get(`/api/users/${userId}`)
      .then(res => setUser(res.data))
      .catch(err => console.error('Failed to load user:', err));
  }, [userId]);

  if (!user) return <div>Loading profile...</div>;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>Email: {user.email}</p>
      <p>Role: {user.role}</p>
      <p>Joined: {new Date(user.createdAt).toLocaleDateString()}</p>
    </div>
  );
}

export default UserProfile;
""")

    # --- Server (Express) files ---

    # server/package.json
    server_pkg = {
        "name": "fullstack-server",
        "version": "1.0.0",
        "main": "index.js",
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^8.0.3",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "eslint-config-airbnb-base": "^15.0.0",
            "eslint-plugin-import": "^2.29.1",
            "nodemon": "^3.0.2"
        },
        "scripts": {
            "start": "node index.js",
            "dev": "nodemon index.js",
            "lint": "eslint ."
        }
    }
    with open(f'{SERVER_DIR}/package.json', 'w') as f:
        json.dump(server_pkg, f, indent=2)

    # server/.eslintrc.json
    server_eslint = {
        "env": {"node": True, "es2021": True},
        "extends": ["eslint:recommended", "airbnb-base"],
        "parserOptions": {"ecmaVersion": "latest", "sourceType": "module"},
        "plugins": ["import"],
        "rules": {
            "no-console": "off",
            "import/extensions": "off",
            "consistent-return": "warn"
        }
    }
    with open(f'{SERVER_DIR}/.eslintrc.json', 'w') as f:
        json.dump(server_eslint, f, indent=2)

    # server/index.js
    with open(f'{SERVER_DIR}/index.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config();

const userRoutes = require('./routes/users');
const metricsRoutes = require('./routes/metrics');
const authMiddleware = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Public routes
app.use('/api/metrics', metricsRoutes);

// Protected routes
app.use('/api/users', authMiddleware, userRoutes);

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/fullstack-app')
  .then(() => {
    console.log('Connected to MongoDB');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
    process.exit(1);
  });
""")

    # server/routes/users.js
    with open(f'{SERVER_DIR}/routes/users.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const User = require('../models/User');

router.get('/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id).select('-password');
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    console.error('Error fetching user:', err);
    res.status(500).json({ message: 'Server error' });
  }
});

router.put('/:id', async (req, res) => {
  try {
    const { name, email, role } = req.body;
    const user = await User.findByIdAndUpdate(
      req.params.id,
      { name, email, role },
      { new: true, runValidators: true }
    ).select('-password');
    res.json(user);
  } catch (err) {
    console.error('Error updating user:', err);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
""")

    # server/routes/metrics.js
    with open(f'{SERVER_DIR}/routes/metrics.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
  try {
    // In production, this would aggregate from the database
    const metrics = {
      totalRevenue: 1247850,
      activeUsers: 34521,
      conversionRate: 3.7,
      newSignups: 1283,
      avgSessionDuration: 342
    };
    res.json(metrics);
  } catch (err) {
    console.error('Error fetching metrics:', err);
    res.status(500).json({ message: 'Failed to retrieve metrics' });
  }
});

module.exports = router;
""")

    # server/middleware/auth.js
    with open(f'{SERVER_DIR}/middleware/auth.js', 'w') as f:
        f.write("""const jwt = require('jsonwebtoken');

module.exports = function authMiddleware(req, res, next) {
  const token = req.header('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ message: 'Access denied. No token provided.' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'dev-secret-key');
    req.user = decoded;
    next();
  } catch (err) {
    res.status(400).json({ message: 'Invalid token.' });
  }
};
""")

    # server/models/User.js
    with open(f'{SERVER_DIR}/models/User.js', 'w') as f:
        f.write("""const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, minlength: 8 },
  role: { type: String, enum: ['admin', 'editor', 'viewer'], default: 'viewer' },
  createdAt: { type: Date, default: Date.now },
  lastLogin: { type: Date }
});

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
""")

    # server/.env.example
    with open(f'{SERVER_DIR}/.env.example', 'w') as f:
        f.write("""PORT=3001
MONGODB_URI=mongodb://localhost:27017/fullstack-app
JWT_SECRET=your-secret-key-here
""")

    print(f'Initial project structure created at: {PROJECT_ROOT}')

    # NO .code-workspace file -- that's what the agent needs to create

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    print('GUI_READY: VSCode launched with DISPLAY=:0')


create_initial()
