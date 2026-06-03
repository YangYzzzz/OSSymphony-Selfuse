"""
Initial Setup: Create legacy-app project with 10 JS files, 4 with 'use strict' and 6 without.
Task ID: vscode_gs_079
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_079'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'legacy-app')


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


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- 4 files WITH 'use strict'; ---

    create_file(os.path.join(PROJECT_DIR, 'app.js'), """\
'use strict';

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', function(req, res) {
    res.send('Welcome to Legacy App');
});

app.get('/api/status', function(req, res) {
    res.json({ status: 'running', uptime: process.uptime() });
});

app.listen(PORT, function() {
    console.log('Server started on port ' + PORT);
});
""")

    create_file(os.path.join(PROJECT_DIR, 'config.js'), """\
'use strict';

var config = {
    database: {
        host: 'localhost',
        port: 5432,
        name: 'legacy_app_db',
        user: 'admin',
        password: process.env.DB_PASSWORD || 'changeme'
    },
    redis: {
        host: '127.0.0.1',
        port: 6379
    },
    logging: {
        level: 'info',
        format: 'combined'
    }
};

module.exports = config;
""")

    create_file(os.path.join(PROJECT_DIR, 'middleware.js'), """\
'use strict';

const jwt = require('jsonwebtoken');
const SECRET_KEY = process.env.JWT_SECRET || 'dev-secret-key';

function authMiddleware(req, res, next) {
    var token = req.headers['authorization'];
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    try {
        var decoded = jwt.verify(token.replace('Bearer ', ''), SECRET_KEY);
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Invalid token' });
    }
}

function logRequest(req, res, next) {
    console.log('[' + new Date().toISOString() + '] ' + req.method + ' ' + req.url);
    next();
}

module.exports = { authMiddleware, logRequest };
""")

    create_file(os.path.join(PROJECT_DIR, 'validators.js'), """\
'use strict';

function validateEmail(email) {
    var re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

function validatePassword(password) {
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[0-9]/.test(password)) return false;
    return true;
}

function validateUsername(username) {
    var re = /^[a-zA-Z0-9_]{3,20}$/;
    return re.test(username);
}

module.exports = { validateEmail, validatePassword, validateUsername };
""")

    # --- 6 files WITHOUT 'use strict'; ---

    create_file(os.path.join(PROJECT_DIR, 'routes.js'), """\
const express = require('express');
const router = express.Router();
const userController = require('./controllers/userController');

router.get('/users', function(req, res) {
    var users = userController.getAllUsers();
    res.json(users);
});

router.post('/users', function(req, res) {
    var newUser = userController.createUser(req.body);
    res.status(201).json(newUser);
});

router.get('/users/:id', function(req, res) {
    var user = userController.getUserById(req.params.id);
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

router.delete('/users/:id', function(req, res) {
    userController.deleteUser(req.params.id);
    res.status(204).send();
});

module.exports = router;
""")

    create_file(os.path.join(PROJECT_DIR, 'database.js'), """\
var mysql = require('mysql2');
var config = require('./config');

var pool = mysql.createPool({
    host: config.database.host,
    port: config.database.port,
    database: config.database.name,
    user: config.database.user,
    password: config.database.password,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

function query(sql, params) {
    return new Promise(function(resolve, reject) {
        pool.execute(sql, params, function(err, results) {
            if (err) reject(err);
            else resolve(results);
        });
    });
}

function getConnection() {
    return new Promise(function(resolve, reject) {
        pool.getConnection(function(err, connection) {
            if (err) reject(err);
            else resolve(connection);
        });
    });
}

module.exports = { query, getConnection, pool };
""")

    create_file(os.path.join(PROJECT_DIR, 'helpers.js'), """\
function formatCurrency(amount, currency) {
    currency = currency || 'USD';
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    });
    return formatter.format(amount);
}

function debounce(func, wait) {
    let timeout;
    return function() {
        var context = this;
        var args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}

function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function generateId() {
    return Math.random().toString(36).substring(2, 15) +
           Math.random().toString(36).substring(2, 15);
}

module.exports = { formatCurrency, debounce, deepClone, generateId };
""")

    create_file(os.path.join(PROJECT_DIR, 'logger.js'), """\
let winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple()
    }));
}

function logError(message, meta) {
    logger.error(message, meta || {});
}

function logInfo(message, meta) {
    logger.info(message, meta || {});
}

module.exports = { logger, logError, logInfo };
""")

    create_file(os.path.join(PROJECT_DIR, 'cache.js'), """\
var NodeCache = require('node-cache');
var cacheInstance = new NodeCache({ stdTTL: 600, checkperiod: 120 });

function get(key) {
    return cacheInstance.get(key);
}

function set(key, value, ttl) {
    ttl = ttl || 600;
    return cacheInstance.set(key, value, ttl);
}

function del(key) {
    return cacheInstance.del(key);
}

function flush() {
    cacheInstance.flushAll();
}

function getStats() {
    return cacheInstance.getStats();
}

module.exports = { get, set, del, flush, getStats };
""")

    create_file(os.path.join(PROJECT_DIR, 'events.js'), """\
function EventEmitter() {
    this.listeners = {};
}

EventEmitter.prototype.on = function(event, callback) {
    if (!this.listeners[event]) {
        this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
    return this;
};

EventEmitter.prototype.emit = function(event) {
    var args = Array.prototype.slice.call(arguments, 1);
    var handlers = this.listeners[event] || [];
    handlers.forEach(function(handler) {
        handler.apply(null, args);
    });
    return this;
};

EventEmitter.prototype.off = function(event, callback) {
    if (!this.listeners[event]) return this;
    this.listeners[event] = this.listeners[event].filter(function(cb) {
        return cb !== callback;
    });
    return this;
};

module.exports = EventEmitter;
""")

    # Create a package.json for realism
    create_file(os.path.join(PROJECT_DIR, 'package.json'), """\
{
  "name": "legacy-app",
  "version": "1.2.4",
  "description": "Legacy application server for internal tools",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.0",
    "mysql2": "^3.6.0",
    "node-cache": "^5.1.2",
    "winston": "^3.10.0"
  },
  "devDependencies": {
    "jest": "^29.6.0",
    "nodemon": "^3.0.0"
  },
  "author": "DevOps Team",
  "license": "MIT"
}
""")

    print(f'Initial project created at: {PROJECT_DIR}')
    print('Files with use strict: app.js, config.js, middleware.js, validators.js')
    print('Files without use strict: routes.js, database.js, helpers.js, logger.js, cache.js, events.js')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
