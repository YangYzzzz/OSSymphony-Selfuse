"""
Initial Setup: Configure custom file associations for .env files in VSCode
Task ID: vscode_web_089
Domain: vscode

Creates a webapp project with various .env files and opens VSCode.
The DotENV extension is installed but files.associations is NOT configured,
so .env.local, .env.development, .env.production show as plain text.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_089'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
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


def create_project_files():
    """Create a realistic webapp project with .env variant files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main .env file
    env_content = """\
# Application Configuration
APP_NAME=WebApp Dashboard
APP_ENV=production
APP_DEBUG=false
APP_PORT=3000
APP_SECRET_KEY=sk_live_8f3a2b7c9d1e4f6a

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=webapp_prod
DB_USER=webapp_admin
DB_PASSWORD=secureP@ss2025

# Redis Cache
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

# External APIs
STRIPE_API_KEY=sk_live_abc123def456
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxx
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
"""
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    # .env.local - local developer overrides
    env_local = """\
# Local Development Overrides
APP_ENV=local
APP_DEBUG=true
APP_PORT=3001

# Local database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=webapp_dev
DB_USER=dev_user
DB_PASSWORD=localdev123

# Local Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Mock API keys for local testing
STRIPE_API_KEY=sk_test_mock_local_key
SENDGRID_API_KEY=SG.local_test_key
"""
    with open(os.path.join(PROJECT_DIR, '.env.local'), 'w') as f:
        f.write(env_local)

    # .env.development - shared dev environment config
    env_dev = """\
# Development Environment Configuration
APP_ENV=development
APP_DEBUG=true
APP_PORT=3000
APP_LOG_LEVEL=debug

# Development Database (shared dev server)
DB_HOST=dev-db.internal.example.com
DB_PORT=5432
DB_NAME=webapp_dev_shared
DB_USER=dev_team
DB_PASSWORD=devTeam2025!

# Development Redis
REDIS_HOST=dev-cache.internal.example.com
REDIS_PORT=6379
REDIS_DB=1

# Development API Keys
STRIPE_API_KEY=sk_test_dev_shared_key
SENDGRID_API_KEY=SG.dev_environment_key
SENTRY_DSN=https://dev@sentry.example.com/1
"""
    with open(os.path.join(PROJECT_DIR, '.env.development'), 'w') as f:
        f.write(env_dev)

    # .env.production - production config template
    env_prod = """\
# Production Environment Configuration
APP_ENV=production
APP_DEBUG=false
APP_PORT=8080
APP_LOG_LEVEL=error

# Production Database (RDS)
DB_HOST=prod-db.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=webapp_production
DB_USER=webapp_prod_svc
DB_PASSWORD=${DB_PASSWORD_FROM_VAULT}

# Production Redis (ElastiCache)
REDIS_HOST=prod-cache.abc123.use1.cache.amazonaws.com
REDIS_PORT=6379
REDIS_DB=0

# Production API Keys
STRIPE_API_KEY=${STRIPE_LIVE_KEY_FROM_VAULT}
SENDGRID_API_KEY=${SENDGRID_PROD_KEY_FROM_VAULT}
SENTRY_DSN=https://prod@sentry.example.com/2
NEW_RELIC_LICENSE_KEY=${NR_KEY_FROM_VAULT}
"""
    with open(os.path.join(PROJECT_DIR, '.env.production'), 'w') as f:
        f.write(env_prod)

    # Create some additional project files for realism
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "webapp-dashboard",
            "version": "2.4.1",
            "description": "Internal analytics dashboard",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest --coverage",
                "build": "webpack --mode production"
            },
            "dependencies": {
                "express": "^4.18.2",
                "dotenv": "^16.3.1",
                "pg": "^8.11.3",
                "redis": "^4.6.10",
                "stripe": "^14.5.0"
            }
        }, f, indent=2)

    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write("""\
require('dotenv').config();
const express = require('express');

const app = express();
const PORT = process.env.APP_PORT || 3000;

app.get('/health', (req, res) => {
    res.json({ status: 'ok', env: process.env.APP_ENV });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
""")

    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("""\
node_modules/
.env
.env.local
dist/
coverage/
""")

    print(f'Project files created in {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up VSCode with basic settings but NO files.associations."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add basic settings but explicitly NO files.associations
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "workbench.colorTheme": "Default Dark Modern",
        "terminal.integrated.defaultProfile.linux": "bash"
    })

    # Make sure files.associations is NOT set
    settings.pop("files.associations", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written to {SETTINGS_PATH}')


def install_dotenv_extension():
    """Install the DotENV extension for syntax highlighting."""
    try:
        result = subprocess.run(
            ['code', '--install-extension', 'mikestead.dotenv', '--force'],
            capture_output=True, text=True, timeout=60
        )
        print(f'Extension install: {result.stdout.strip()}')
        if result.returncode != 0:
            print(f'Extension install stderr: {result.stderr.strip()}')
    except Exception as e:
        print(f'Extension install warning: {e}')


def main():
    create_project_files()
    setup_vscode_settings()
    install_dotenv_extension()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with ~/projects/webapp/')


main()
