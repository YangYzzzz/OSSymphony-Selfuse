"""
Initial Setup: Create SQLite database and project structure for SQLTools task
Task ID: vscode_gf3_028
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_028'
PROJECT_DIR = f'{WORKDIR}/projects/app'
DATA_DIR = f'{PROJECT_DIR}/data'
DB_PATH = f'{DATA_DIR}/app.db'


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
    # 1. Create project directory structure
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # 2. Create an empty SQLite database file (no tables yet)
    conn = sqlite3.connect(DB_PATH)
    conn.close()
    print(f'Created empty SQLite database: {DB_PATH}')

    # 3. Create some realistic project files
    # A simple Python app file
    app_py_content = '''"""
Simple Flask application for managing users.
Database: SQLite (app.db)
"""

from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'app.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/users', methods=['GET'])
def list_users():
    db = get_db()
    # TODO: implement after creating database schema
    db.close()
    return jsonify({"users": []})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
'''
    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write(app_py_content)

    # A requirements file
    requirements_content = '''flask==3.0.0
sqlite3-api==2.0.0
pytest==7.4.3
'''
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # A README
    readme_content = '''# App Project

A lightweight web application using Flask and SQLite.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize the database schema
3. Run: `python src/app.py`

## Database

The application uses SQLite stored at `data/app.db`.
Schema needs to be created before first run.
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # A config file
    config_content = '''{
    "app_name": "User Management App",
    "version": "0.1.0",
    "database": {
        "type": "sqlite",
        "path": "data/app.db"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 5001,
        "debug": true
    }
}
'''
    with open(f'{PROJECT_DIR}/config.json', 'w') as f:
        f.write(config_content)

    print(f'Project structure created at: {PROJECT_DIR}')

    # 4. Launch VSCode with the project folder (GUI-ready state)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
