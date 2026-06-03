"""
Initial Setup: Create a multi-root workspace file in VSCode
Task ID: vscode_file_069
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_069'
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
    # Create project directory structure
    os.makedirs(f'{PROJECTS_DIR}/my-frontend-app/src', exist_ok=True)
    os.makedirs(f'{PROJECTS_DIR}/my-backend-api/src', exist_ok=True)

    # Create frontend project files
    with open(f'{PROJECTS_DIR}/my-frontend-app/src/App.js', 'w') as f:
        f.write("""import React, { useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    const response = await fetch('http://localhost:5000/api/data');
    const json = await response.json();
    setData(json);
  };

  return (
    <div className="App">
      <h1>My Frontend App</h1>
      <button onClick={fetchData}>Load Data</button>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item.name}: {item.value}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
""")

    with open(f'{PROJECTS_DIR}/my-frontend-app/package.json', 'w') as f:
        json.dump({
            "name": "my-frontend-app",
            "version": "1.0.0",
            "description": "A React frontend application",
            "main": "src/index.js",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "author": "Developer",
            "license": "MIT"
        }, f, indent=2)

    # Create backend project files
    with open(f'{PROJECTS_DIR}/my-backend-api/src/server.py', 'w') as f:
        f.write("""from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data store
records = [
    {"id": 1, "name": "Revenue Q1", "value": 142500, "date": "2025-01-31"},
    {"id": 2, "name": "Revenue Q2", "value": 158300, "date": "2025-04-30"},
    {"id": 3, "name": "Revenue Q3", "value": 171200, "date": "2025-07-31"},
    {"id": 4, "name": "Revenue Q4", "value": 189600, "date": "2025-10-31"},
]


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(records)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
""")

    with open(f'{PROJECTS_DIR}/my-backend-api/requirements.txt', 'w') as f:
        f.write("""Flask==3.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
""")

    # Ensure no workspace file exists in initial state
    workspace_file = f'{PROJECTS_DIR}/workspace.code-workspace'
    if os.path.exists(workspace_file):
        os.remove(workspace_file)

    print(f'Initial project directories created at: {PROJECTS_DIR}')

    # GUI-ready startup: open VSCode with the projects directory but no workspace file
    launch_gui('code /home/user/projects', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
