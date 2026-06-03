"""
Initial Setup: Multi-cursor Find and Replace to rename 'callback' to 'handler' in registerEvent
Task ID: vscode_gs_081
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_081'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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

    # Create a realistic events.js file
    # Lines are carefully structured so registerEvent spans lines 30-50,
    # onLoad spans lines 55-70, fetchData spans lines 75-95
    events_js = """\
// events.js - Event Management Module
// Part of the WebApp framework
// Author: Sarah Chen
// Last modified: 2025-11-20

'use strict';

const EventEmitter = require('events');
const logger = require('./utils/logger');

// Configuration constants
const MAX_LISTENERS = 25;
const EVENT_TIMEOUT = 5000;
const RETRY_ATTEMPTS = 3;

// Supported event types
const EVENT_TYPES = {
    USER_ACTION: 'user_action',
    SYSTEM: 'system',
    NETWORK: 'network',
    LIFECYCLE: 'lifecycle'
};

// Internal event registry
const _registry = new Map();
let _nextId = 1000;

// Register a new event listener with validation and retry logic
function registerEvent(eventName, callback, options = {}) {
    if (!eventName || typeof eventName !== 'string') {
        throw new TypeError('Event name must be a non-empty string');
    }
    if (typeof callback !== 'function') {
        throw new TypeError('Second argument must be a function');
    }
    const priority = options.priority || 'normal';
    const timeout = options.timeout || EVENT_TIMEOUT;
    const wrappedFn = function (...args) {
        const timer = setTimeout(() => {
            logger.warn(`Listener timed out for: ${eventName}`);
        }, timeout);
        try {
            const result = callback(...args);
            clearTimeout(timer);
            return result;
        } catch (err) {
            clearTimeout(timer);
            logger.error(`Error in listener for event ${eventName}:`, err);
            throw err;
        }
    };
    _registry.set(_nextId++, { eventName, callback, priority });
    logger.info(`Registered event: ${eventName}`);
    return wrappedFn;
}

// Initialize page load handlers and DOM-ready events
function onLoad(callback, options = {}) {
    const defer = options.defer || false;
    const once = options.once || true;
    if (typeof callback !== 'function') {
        throw new TypeError('onLoad requires a valid function argument');
    }
    const eventName = defer ? 'DOMContentLoaded' : 'load';
    const ready = !defer && document.readyState === 'complete';
    if (ready) {
        callback();
    } else {
        window.addEventListener(eventName, function () {
            logger.info(`${eventName} event fired`);
        }, { once: once });
    }
    logger.info('Page load listener registered');
}

// Fetch data from API endpoint with retry logic
function fetchData(url, callback, retryCount = RETRY_ATTEMPTS) {
    if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided to fetchData');
    }
    if (typeof callback !== 'function') {
        throw new TypeError('fetchData requires a function argument');
    }
    let attempts = 0;
    function attemptFetch() {
        attempts++;
        logger.info(`Fetch attempt ${attempts}/${retryCount} for: ${url}`);
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                logger.info(`Data fetched successfully from: ${url}`);
                callback(data);
            })
            .catch(error => {
                if (attempts < retryCount) {
                    logger.warn(`Fetch failed, retrying... (${attempts}/${retryCount})`);
                    setTimeout(attemptFetch, 1000 * attempts);
                } else {
                    logger.error(`All ${retryCount} attempts failed for: ${url}`);
                }
            });
    }
    attemptFetch();
}

// Module exports
module.exports = {
    registerEvent,
    onLoad,
    fetchData,
    EVENT_TYPES,
    MAX_LISTENERS
};
"""

    events_path = os.path.join(PROJECT_DIR, 'events.js')
    with open(events_path, 'w') as f:
        f.write(events_js)

    # Create some supporting files for a realistic project
    # package.json
    package_json = """{
  "name": "webapp",
  "version": "2.4.1",
  "description": "Enterprise web application framework",
  "main": "index.js",
  "scripts": {
    "start": "node server.js",
    "test": "jest --coverage",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "events": "^3.3.0"
  }
}
"""
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write(package_json)

    # index.js
    index_js = """'use strict';

const { registerEvent, onLoad, fetchData, EVENT_TYPES } = require('./events');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/api/status', (req, res) => {
    res.json({ status: 'running', version: '2.4.1' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
"""
    with open(os.path.join(PROJECT_DIR, 'index.js'), 'w') as f:
        f.write(index_js)

    # utils/logger.js
    os.makedirs(os.path.join(PROJECT_DIR, 'utils'), exist_ok=True)
    logger_js = """'use strict';

const LOG_LEVELS = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
let currentLevel = LOG_LEVELS.INFO;

module.exports = {
    info: (msg) => currentLevel <= LOG_LEVELS.INFO && console.log(`[INFO] ${msg}`),
    warn: (msg) => currentLevel <= LOG_LEVELS.WARN && console.warn(`[WARN] ${msg}`),
    error: (msg, err) => console.error(`[ERROR] ${msg}`, err || ''),
    setLevel: (level) => { currentLevel = LOG_LEVELS[level] || LOG_LEVELS.INFO; }
};
"""
    with open(os.path.join(PROJECT_DIR, 'utils', 'logger.js'), 'w') as f:
        f.write(logger_js)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Events file: {os.path.join(PROJECT_DIR, "events.js")}')

    # Count callback occurrences for verification
    with open(events_path, 'r') as f:
        content = f.read()

    # Count in registerEvent function
    lines = content.split('\n')
    register_callbacks = 0
    onload_callbacks = 0
    fetchdata_callbacks = 0
    current_func = None

    for line in lines:
        if 'function registerEvent' in line:
            current_func = 'registerEvent'
        elif 'function onLoad' in line:
            current_func = 'onLoad'
        elif 'function fetchData' in line:
            current_func = 'fetchData'

        if current_func == 'registerEvent':
            register_callbacks += line.count('callback')
        elif current_func == 'onLoad':
            onload_callbacks += line.count('callback')
        elif current_func == 'fetchData':
            fetchdata_callbacks += line.count('callback')

    total = register_callbacks + onload_callbacks + fetchdata_callbacks
    print(f'callback in registerEvent: {register_callbacks}')
    print(f'callback in onLoad: {onload_callbacks}')
    print(f'callback in fetchData: {fetchdata_callbacks}')
    print(f'Total callback occurrences: {total}')

    # Launch VSCode with the project folder, opening events.js
    launch_gui(f'code {PROJECT_DIR}', delay_sec=2.0)
    launch_gui(f'code {os.path.join(PROJECT_DIR, "events.js")}', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
