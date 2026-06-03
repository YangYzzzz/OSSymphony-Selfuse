"""
Initial Setup: Configure performance profiling task for a Node.js application in VSCode
Task ID: vscode_gf3_048
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_048'
PROJECT_DIR = f'{WORKDIR}/projects/node-service'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # package.json — realistic Node.js service
    package_json = {
        "name": "node-service",
        "version": "2.4.1",
        "description": "Backend API service for inventory management",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "winston": "^3.11.0",
            "jsonwebtoken": "^9.0.2",
            "bcryptjs": "^2.4.3"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "nodemon": "^3.0.2",
            "eslint": "^8.54.0",
            "supertest": "^6.3.3"
        },
        "engines": {
            "node": ">=18.0.0"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/server.js — main entry point
    server_js = '''\
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const mongoose = require('mongoose');
const winston = require('winston');
require('dotenv').config();

const inventoryRoutes = require('./routes/inventory');
const authRoutes = require('./routes/auth');
const authMiddleware = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 3000;

// Logger setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/inventory', authMiddleware, inventoryRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// Database connection
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/inventory';

mongoose.connect(MONGO_URI)
  .then(() => {
    logger.info('Connected to MongoDB');
    app.listen(PORT, () => {
      logger.info(`Server running on port ${PORT}`);
      console.log(`Inventory service listening on port ${PORT}`);
    });
  })
  .catch(err => {
    logger.error('Database connection failed', { error: err.message });
    process.exit(1);
  });

module.exports = app;
'''
    with open(f'{PROJECT_DIR}/src/server.js', 'w') as f:
        f.write(server_js)

    # src/routes/inventory.js
    inventory_js = '''\
const express = require('express');
const router = express.Router();

// In-memory cache for hot path optimization
let inventoryCache = new Map();
const CACHE_TTL = 60000; // 1 minute

function computeStockMetrics(items) {
  let totalValue = 0;
  let lowStockCount = 0;
  for (const item of items) {
    totalValue += item.quantity * item.unitPrice;
    if (item.quantity < item.reorderThreshold) {
      lowStockCount++;
    }
  }
  return { totalValue, lowStockCount, itemCount: items.length };
}

router.get('/', async (req, res) => {
  try {
    const { category, warehouse, page = 1, limit = 50 } = req.query;
    const filter = {};
    if (category) filter.category = category;
    if (warehouse) filter.warehouse = warehouse;

    const items = await Item.find(filter)
      .skip((page - 1) * limit)
      .limit(parseInt(limit))
      .sort({ updatedAt: -1 });

    const metrics = computeStockMetrics(items);
    res.json({ items, metrics, page: parseInt(page) });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch inventory' });
  }
});

router.post('/bulk-update', async (req, res) => {
  const { updates } = req.body;
  const results = [];
  for (const update of updates) {
    try {
      const item = await Item.findByIdAndUpdate(update.id, update.changes, { new: true });
      results.push({ id: update.id, status: 'success', item });
    } catch (err) {
      results.push({ id: update.id, status: 'error', message: err.message });
    }
  }
  inventoryCache.clear();
  res.json({ results });
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/inventory.js', 'w') as f:
        f.write(inventory_js)

    # src/routes/auth.js
    auth_js = '''\
const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const router = express.Router();

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const user = await User.findOne({ email });
    if (!user || !await bcrypt.compare(password, user.passwordHash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ userId: user._id, role: user.role }, JWT_SECRET, { expiresIn: '8h' });
    res.json({ token, user: { email: user.email, role: user.role } });
  } catch (err) {
    res.status(500).json({ error: 'Authentication failed' });
  }
});

module.exports = router;
'''
    with open(f'{PROJECT_DIR}/src/routes/auth.js', 'w') as f:
        f.write(auth_js)

    # src/middleware/auth.js
    auth_middleware = '''\
const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';

module.exports = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Access denied' });
  }
  try {
    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(403).json({ error: 'Invalid token' });
  }
};
'''
    with open(f'{PROJECT_DIR}/src/middleware/auth.js', 'w') as f:
        f.write(auth_middleware)

    # .env file
    env_content = '''\
PORT=3000
MONGO_URI=mongodb://localhost:27017/inventory
JWT_SECRET=a7f2c9e1d4b8f3a6e5c2d1b9a8f7e6d5
NODE_ENV=development
LOG_LEVEL=info
'''
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write(env_content)

    # .gitignore
    gitignore = '''\
node_modules/
.env
logs/
coverage/
*.log
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # VSCode settings.json (workspace-level, but NO launch.json or tasks.json)
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "files.exclude": {
            "node_modules": True,
            "coverage": True
        }
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # tests/inventory.test.js
    test_js = '''\
const request = require('supertest');
const app = require('../src/server');

describe('Inventory API', () => {
  let authToken;

  beforeAll(async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@warehouse.com', password: 'admin123' });
    authToken = res.body.token;
  });

  test('GET /api/inventory returns paginated results', async () => {
    const res = await request(app)
      .get('/api/inventory?page=1&limit=10')
      .set('Authorization', `Bearer ${authToken}`);
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('items');
    expect(res.body).toHaveProperty('metrics');
  });

  test('GET /health returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/inventory.test.js', 'w') as f:
        f.write(test_js)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  .vscode/settings.json present (NO launch.json, NO tasks.json)')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
