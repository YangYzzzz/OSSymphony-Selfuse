"""
Initial Setup: Create project directory structure without workspace file
Task ID: vscode_file_080
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_080'
PROJECTS_DIR = f'{WORKDIR}/projects'


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
    # --- web-client project (React frontend) ---
    web_src = f'{PROJECTS_DIR}/web-client/src'
    os.makedirs(web_src, exist_ok=True)

    # App.tsx
    with open(f'{web_src}/App.tsx', 'w') as f:
        f.write("""import React from 'react';

interface AppProps {
  title: string;
}

const App: React.FC<AppProps> = ({ title }) => {
  return (
    <div className="app">
      <header>
        <h1>{title}</h1>
      </header>
      <main>
        <p>Welcome to the team project.</p>
      </main>
    </div>
  );
};

export default App;
""")

    # web-client package.json
    with open(f'{PROJECTS_DIR}/web-client/package.json', 'w') as f:
        f.write("""{
  "name": "web-client",
  "version": "1.0.0",
  "description": "React frontend application",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
""")

    # --- api-server project (Python backend) ---
    api_src = f'{PROJECTS_DIR}/api-server/src'
    os.makedirs(api_src, exist_ok=True)

    # app.py
    with open(f'{api_src}/app.py', 'w') as f:
        f.write("""from flask import Flask, jsonify, request
from typing import Dict, Any

app = Flask(__name__)

users: Dict[str, Any] = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'version': '1.0.0'})


@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'name required'}), 400
    user_id = str(len(users) + 1)
    users[user_id] = {'id': user_id, 'name': data['name']}
    return jsonify(users[user_id]), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
""")

    # requirements.txt
    with open(f'{PROJECTS_DIR}/api-server/requirements.txt', 'w') as f:
        f.write("""flask>=2.3.0
flask-cors>=4.0.0
pytest>=7.4.0
python-dotenv>=1.0.0
""")

    # --- shared-utils project ---
    shared_lib = f'{PROJECTS_DIR}/shared-utils/lib'
    os.makedirs(shared_lib, exist_ok=True)

    # helpers.js
    with open(f'{shared_lib}/helpers.js', 'w') as f:
        f.write("""/**
 * Shared utility helpers for team project
 */

/**
 * Format a date to ISO string (YYYY-MM-DD)
 * @param {Date} date
 * @returns {string}
 */
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * Debounce a function call
 * @param {Function} fn - function to debounce
 * @param {number} delay - delay in milliseconds
 * @returns {Function}
 */
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Deep merge two objects
 * @param {Object} target
 * @param {Object} source
 * @returns {Object}
 */
function deepMerge(target, source) {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object') {
      result[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

module.exports = { formatDate, debounce, deepMerge };
""")

    # shared-utils package.json
    with open(f'{PROJECTS_DIR}/shared-utils/package.json', 'w') as f:
        f.write("""{
  "name": "shared-utils",
  "version": "1.0.0",
  "description": "Shared utility functions for team projects",
  "main": "lib/helpers.js",
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
""")

    print(f'Project directories created under: {PROJECTS_DIR}')
    print('Initial state: NO team.code-workspace file exists (task is to create it)')

    # GUI-ready startup: Open VSCode with no folder (just the projects directory view)
    launch_gui(f'code "{PROJECTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with projects directory, DISPLAY=:0')


create_initial()
