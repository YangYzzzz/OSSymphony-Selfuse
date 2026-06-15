"""
Initial Setup: Add a watch task to tasks.json (pre-task state)
Task ID: vscode_td_006
Domain: vscode

Creates a webpack-app project with:
- .vscode/tasks.json containing ONE build task only
- package.json with build and watch scripts
- webpack.config.js
- src/index.js
Then opens VSCode with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webpack-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(SRC_DIR, exist_ok=True)

    # --- .vscode/tasks.json with ONE build task only ---
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Build",
                "type": "shell",
                "command": "npm run build",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": ["$tsc"]
            }
        ]
    }
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    with open(tasks_path, 'w') as f:
        json.dump(tasks_json, f, indent=4)
    print(f'Created: {tasks_path}')

    # --- package.json with build and watch scripts ---
    package_json = {
        "name": "webpack-app",
        "version": "1.0.0",
        "description": "A sample webpack application for data visualization",
        "main": "src/index.js",
        "scripts": {
            "build": "webpack --mode production",
            "watch": "webpack --watch",
            "dev": "webpack serve --open",
            "test": "jest",
            "lint": "eslint src/"
        },
        "dependencies": {
            "chart.js": "^4.4.1",
            "lodash": "^4.17.21"
        },
        "devDependencies": {
            "webpack": "^5.90.0",
            "webpack-cli": "^5.1.4",
            "webpack-dev-server": "^4.15.1",
            "html-webpack-plugin": "^5.6.0",
            "css-loader": "^6.9.1",
            "style-loader": "^3.3.4",
            "babel-loader": "^9.1.3",
            "@babel/core": "^7.23.9",
            "@babel/preset-env": "^7.23.9"
        },
        "author": "Elena Rodriguez",
        "license": "MIT"
    }
    package_path = os.path.join(PROJECT_DIR, 'package.json')
    with open(package_path, 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {package_path}')

    # --- webpack.config.js ---
    webpack_config = """const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
    },
    module: {
        rules: [
            {
                test: /\\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /\\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'Data Visualization Dashboard',
            template: './src/index.html',
        }),
    ],
    devServer: {
        static: './dist',
        port: 3000,
        hot: true,
    },
};
"""
    webpack_path = os.path.join(PROJECT_DIR, 'webpack.config.js')
    with open(webpack_path, 'w') as f:
        f.write(webpack_config)
    print(f'Created: {webpack_path}')

    # --- src/index.js ---
    index_js = """import { debounce } from 'lodash';

const API_ENDPOINT = 'https://api.example.com/dashboard/metrics';

class DashboardApp {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.charts = {};
        this.refreshInterval = 30000;
    }

    async fetchMetrics() {
        try {
            const response = await fetch(API_ENDPOINT);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to fetch metrics:', error);
            return null;
        }
    }

    renderSummaryCard(title, value, trend) {
        const card = document.createElement('div');
        card.className = 'metric-card';
        card.innerHTML = `
            <h3>${title}</h3>
            <span class="value">${value}</span>
            <span class="trend ${trend > 0 ? 'up' : 'down'}">${trend}%</span>
        `;
        return card;
    }

    init() {
        console.log('Dashboard initialized');
        this.fetchMetrics().then(data => {
            if (data) {
                this.renderSummaryCard('Revenue', data.revenue, data.revenueTrend);
            }
        });
    }
}

const app = new DashboardApp('app-root');
const debouncedResize = debounce(() => app.init(), 250);
window.addEventListener('resize', debouncedResize);
document.addEventListener('DOMContentLoaded', () => app.init());
"""
    index_path = os.path.join(SRC_DIR, 'index.js')
    with open(index_path, 'w') as f:
        f.write(index_js)
    print(f'Created: {index_path}')

    # --- src/index.html ---
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Visualization Dashboard</title>
</head>
<body>
    <div id="app-root"></div>
</body>
</html>
"""
    html_path = os.path.join(SRC_DIR, 'index.html')
    with open(html_path, 'w') as f:
        f.write(index_html)
    print(f'Created: {html_path}')

    # --- Open VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
