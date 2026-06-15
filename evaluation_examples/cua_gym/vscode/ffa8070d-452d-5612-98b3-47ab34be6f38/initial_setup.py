"""
Initial Setup: Add search exclude patterns for node_modules, dist, and .cache
Task ID: vscode_we_016
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_016'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'

# VSCode config paths
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    """Create a realistic JavaScript project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "analytics-dashboard",
        "version": "2.1.0",
        "description": "Real-time analytics dashboard for monitoring sales metrics",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "build": "webpack --mode production",
            "dev": "webpack serve --mode development",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "chart.js": "^4.4.1",
            "lodash": "^4.17.21",
            "axios": "^1.6.2",
            "moment": "^2.30.1"
        },
        "devDependencies": {
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4",
            "webpack-dev-server": "^4.15.1",
            "jest": "^29.7.0",
            "eslint": "^8.56.0"
        },
        "author": "Elena Rodriguez",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/ directory with realistic files
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    index_js = '''const express = require('express');
const { fetchMetrics } = require('./services/metricsService');
const { formatCurrency } = require('./utils/formatters');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/api/dashboard', async (req, res) => {
    try {
        const metrics = await fetchMetrics();
        const formatted = metrics.map(m => ({
            ...m,
            revenue: formatCurrency(m.revenue),
            timestamp: new Date(m.timestamp).toISOString()
        }));
        res.json({ success: true, data: formatted });
    } catch (error) {
        console.error('Dashboard fetch failed:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Analytics dashboard running on port ${PORT}`);
});
'''
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # services directory
    services_dir = os.path.join(src_dir, 'services')
    os.makedirs(services_dir, exist_ok=True)

    metrics_service = '''const axios = require('axios');
const _ = require('lodash');

const API_BASE = process.env.METRICS_API || 'https://api.internal.analytics.io';

async function fetchMetrics(dateRange = 'last_30_days') {
    const response = await axios.get(`${API_BASE}/v2/metrics`, {
        params: { range: dateRange, granularity: 'daily' }
    });
    return _.sortBy(response.data.metrics, 'timestamp');
}

async function aggregateByRegion(metrics) {
    return _.chain(metrics)
        .groupBy('region')
        .mapValues(group => ({
            totalRevenue: _.sumBy(group, 'revenue'),
            avgConversion: _.meanBy(group, 'conversionRate'),
            count: group.length
        }))
        .value();
}

module.exports = { fetchMetrics, aggregateByRegion };
'''
    with open(os.path.join(services_dir, 'metricsService.js'), 'w') as f:
        f.write(metrics_service)

    # utils directory
    utils_dir = os.path.join(src_dir, 'utils')
    os.makedirs(utils_dir, exist_ok=True)

    formatters = '''function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

function formatPercentage(value, decimals = 1) {
    return `${(value * 100).toFixed(decimals)}%`;
}

function formatDate(dateStr, locale = 'en-US') {
    const date = new Date(dateStr);
    return date.toLocaleDateString(locale, {
        year: 'numeric', month: 'short', day: 'numeric'
    });
}

module.exports = { formatCurrency, formatPercentage, formatDate };
'''
    with open(os.path.join(utils_dir, 'formatters.js'), 'w') as f:
        f.write(formatters)

    # config directory
    config_dir = os.path.join(src_dir, 'config')
    os.makedirs(config_dir, exist_ok=True)

    config_js = '''module.exports = {
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: parseInt(process.env.DB_PORT) || 5432,
        name: 'analytics_prod'
    },
    redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: 6379,
        ttl: 300
    },
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        format: 'json'
    }
};
'''
    with open(os.path.join(config_dir, 'config.js'), 'w') as f:
        f.write(config_js)

    # Create node_modules/ with realistic subdirs (large directory)
    nm_dir = os.path.join(PROJECT_DIR, 'node_modules')
    for pkg in ['express', 'lodash', 'axios', 'chart.js', 'moment',
                'webpack', 'jest', 'eslint', 'chalk', 'debug',
                'body-parser', 'mime-types', 'qs', 'raw-body',
                'safe-buffer', 'statuses', 'unpipe', 'ee-first']:
        pkg_dir = os.path.join(nm_dir, pkg)
        os.makedirs(pkg_dir, exist_ok=True)
        with open(os.path.join(pkg_dir, 'package.json'), 'w') as f:
            json.dump({"name": pkg, "version": "1.0.0", "main": "index.js"}, f)
        with open(os.path.join(pkg_dir, 'index.js'), 'w') as f:
            f.write(f'// {pkg} module entry point\nmodule.exports = {{}};\n')

    # Create dist/ directory with build output
    dist_dir = os.path.join(PROJECT_DIR, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, 'bundle.js'), 'w') as f:
        f.write('// Webpack bundle output - minified\n!function(e,t){"use strict";' +
                'var n=require("express");' * 20 + '}(this,function(){});\n')
    with open(os.path.join(dist_dir, 'bundle.js.map'), 'w') as f:
        f.write('{"version":3,"sources":["src/index.js"],"mappings":"AAAA"}\n')
    with open(os.path.join(dist_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html><html><head><title>Analytics Dashboard</title></head>'
                '<body><div id="root"></div><script src="bundle.js"></script></body></html>\n')

    # Create .cache/ directory
    cache_dir = os.path.join(PROJECT_DIR, '.cache')
    os.makedirs(cache_dir, exist_ok=True)
    with open(os.path.join(cache_dir, 'webpack-cache.json'), 'w') as f:
        json.dump({"version": "5.89.0", "entries": {}, "hash": "a1b2c3d4e5"}, f)
    os.makedirs(os.path.join(cache_dir, 'babel'), exist_ok=True)
    with open(os.path.join(cache_dir, 'babel', 'cache.json'), 'w') as f:
        json.dump({"cacheKey": "babel-loader-7.23.6"}, f)

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('node_modules/\ndist/\n.cache/\n.env\ncoverage/\n')

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Analytics Dashboard\n\n'
                'Real-time analytics dashboard for monitoring sales metrics.\n\n'
                '## Getting Started\n\n'
                '```bash\nnpm install\nnpm run dev\n```\n\n'
                '## Architecture\n\n'
                '- Express.js backend serving REST APIs\n'
                '- Chart.js for data visualization\n'
                '- Webpack for build pipeline\n')

    print(f'Project created: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set VSCode settings to empty (no search.exclude)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings initialized (empty): {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_settings()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
