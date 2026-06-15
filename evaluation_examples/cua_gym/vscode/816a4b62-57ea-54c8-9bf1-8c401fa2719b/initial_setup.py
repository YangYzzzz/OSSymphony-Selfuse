"""
Initial Setup: Sort and organize Python imports in VSCode
Task ID: vscode_rrt_049
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_049'
PROJECT_DIR = f'{WORKDIR}/projects/app'
OUTPUT = f'{PROJECT_DIR}/server.py'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # The initial server.py with messy, unsorted imports and a duplicate 'import json'
    content = '''\
import json
import os
import sys
from flask import Flask, request
import json
from datetime import datetime
import logging
from pathlib import Path
from flask import jsonify


app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data storage path
DATA_DIR = Path('/home/user/projects/app/data')
DATA_DIR.mkdir(parents=True, exist_ok=True)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    """Retrieve all users from the data store."""
    users_file = DATA_DIR / 'users.json'
    if not users_file.exists():
        return jsonify({'users': [], 'count': 0})

    with open(users_file, 'r') as f:
        users = json.load(f)

    return jsonify({
        'users': users,
        'count': len(users)
    })


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    users_file = DATA_DIR / 'users.json'
    users = []
    if users_file.exists():
        with open(users_file, 'r') as f:
            users = json.load(f)

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data.get('email', ''),
        'created_at': datetime.now().isoformat()
    }
    users.append(new_user)

    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)

    logger.info(f"Created user: {new_user['name']}")
    return jsonify(new_user), 201


@app.route('/api/config', methods=['GET'])
def get_config():
    """Return server configuration."""
    config_path = DATA_DIR / 'config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        return jsonify(config)
    return jsonify({
        'debug': False,
        'version': '1.0.0',
        'data_dir': str(DATA_DIR)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
'''

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
