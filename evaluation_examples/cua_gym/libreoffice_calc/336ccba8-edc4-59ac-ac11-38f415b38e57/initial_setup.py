"""
Initial Setup: Configure VSCode to associate .env files with properties language mode
Task ID: vscode_lp_020
Domain: vscode (settings)

Creates a project workspace with .env files and opens VSCode with empty user settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_020'
WORKSPACE_DIR = f'{WORKDIR}/workspace'
VSCODE_USER_DIR = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER_DIR, 'settings.json')


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
    # --- Create workspace directory ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # --- Create .env file with realistic key=value content ---
    env_content = """# Application Configuration
APP_NAME=InventoryTracker
APP_ENV=development
APP_DEBUG=true
APP_PORT=3000

# Database Settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_dev
DB_USER=admin
DB_PASSWORD=s3cur3_p@ssw0rd

# Redis Cache
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PREFIX=inv_

# External API Keys
STRIPE_API_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
AWS_S3_BUCKET=inventory-uploads

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/inventory/app.log

# JWT Authentication
JWT_SECRET=my_super_secret_jwt_key_2025
JWT_EXPIRATION=86400
"""
    with open(os.path.join(WORKSPACE_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # --- Create .env.example file ---
    env_example_content = """# Copy this file to .env and fill in the values
APP_NAME=
APP_ENV=development
APP_DEBUG=false
APP_PORT=3000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PREFIX=

STRIPE_API_KEY=
SENDGRID_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
AWS_S3_BUCKET=
"""
    with open(os.path.join(WORKSPACE_DIR, '.env.example'), 'w') as f:
        f.write(env_example_content)

    # --- Create a sample Python file ---
    main_py_content = """#!/usr/bin/env python3
\"\"\"Inventory Tracker - Main Application Entry Point\"\"\"

import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('APP_DEBUG', 'false').lower() == 'true'

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'app': os.getenv('APP_NAME', 'unknown'),
        'environment': os.getenv('APP_ENV', 'production')
    })

@app.route('/api/items')
def list_items():
    # TODO: Connect to database
    return jsonify({'items': [], 'total': 0})

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 3000))
    app.run(host='0.0.0.0', port=port)
"""
    with open(os.path.join(WORKSPACE_DIR, 'main.py'), 'w') as f:
        f.write(main_py_content)

    # --- Create a README ---
    readme_content = """# Inventory Tracker

A simple inventory management application built with Flask.

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your configuration values
3. Run `pip install -r requirements.txt`
4. Start the server: `python main.py`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/items` - List inventory items
"""
    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # --- Create requirements.txt ---
    with open(os.path.join(WORKSPACE_DIR, 'requirements.txt'), 'w') as f:
        f.write("flask==3.0.0\npython-dotenv==1.0.0\npsycopg2-binary==2.9.9\nredis==5.0.1\n")

    # --- Ensure VSCode user settings is empty (no file associations) ---
    os.makedirs(VSCODE_USER_DIR, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings reset to empty: {SETTINGS_PATH}')

    print(f'Workspace created: {WORKSPACE_DIR}')

    # --- Launch VSCode with the workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    # Open the .env file specifically so the user sees it as plain text
    launch_gui(f'code "{WORKSPACE_DIR}/.env"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
