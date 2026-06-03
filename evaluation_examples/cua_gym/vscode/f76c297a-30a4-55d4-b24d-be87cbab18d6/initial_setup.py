"""
Initial Setup: Create VSCode workspace with deploy.sh script, no launch.json
Task ID: vscode_ops_091
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_091'
PROJECT_DIR = f'{WORKDIR}/project'
SCRIPTS_DIR = f'{PROJECT_DIR}/scripts'


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
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Create a realistic deploy.sh script
    deploy_script = '''#!/usr/bin/env bash
#
# deploy.sh - Automated deployment script for the analytics platform
# Usage: ./deploy.sh [--env <environment>] [--dry-run] [--verbose]
#

set -euo pipefail

# Default configuration
ENVIRONMENT="production"
DRY_RUN=false
VERBOSE=false
DEPLOY_USER="deploy"
APP_NAME="analytics-platform"
DEPLOY_DIR="/opt/${APP_NAME}"
LOG_DIR="/var/log/${APP_NAME}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/${APP_NAME}/${TIMESTAMP}"

# Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --env <environment>   Target environment (staging|production) [default: production]"
    echo "  --dry-run             Show what would be done without making changes"
    echo "  --verbose             Enable verbose output"
    echo "  -h, --help            Show this help message"
    exit 0
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate environment
if [[ "${ENVIRONMENT}" != "staging" && "${ENVIRONMENT}" != "production" ]]; then
    log_error "Invalid environment: ${ENVIRONMENT}. Must be 'staging' or 'production'."
    exit 1
fi

log_info "Starting deployment to ${ENVIRONMENT}"
log_info "Application: ${APP_NAME}"
log_info "Deploy directory: ${DEPLOY_DIR}"

# Step 1: Pre-flight checks
log_info "Running pre-flight checks..."
if [[ "${DRY_RUN}" == true ]]; then
    log_warn "DRY RUN MODE - No changes will be made"
fi

# Step 2: Create backup
log_info "Creating backup at ${BACKUP_DIR}"
if [[ "${DRY_RUN}" == false ]]; then
    mkdir -p "${BACKUP_DIR}"
    if [[ -d "${DEPLOY_DIR}" ]]; then
        cp -r "${DEPLOY_DIR}" "${BACKUP_DIR}/app"
        log_info "Backup created successfully"
    else
        log_warn "No existing deployment found, skipping backup"
    fi
fi

# Step 3: Pull latest code
log_info "Pulling latest artifacts for ${ENVIRONMENT}..."
if [[ "${DRY_RUN}" == false ]]; then
    mkdir -p "${DEPLOY_DIR}"
fi

# Step 4: Run database migrations
if [[ "${ENVIRONMENT}" == "production" ]]; then
    log_info "Running database migrations..."
    if [[ "${DRY_RUN}" == false ]]; then
        log_info "Migrations completed"
    fi
fi

# Step 5: Restart services
log_info "Restarting application services..."
if [[ "${DRY_RUN}" == false ]]; then
    log_info "Services restarted successfully"
fi

# Step 6: Health check
log_info "Running health checks..."
HEALTH_URL="http://localhost:8080/health"
if [[ "${ENVIRONMENT}" == "staging" ]]; then
    HEALTH_URL="http://localhost:8081/health"
fi

log_info "Deployment to ${ENVIRONMENT} completed successfully!"
echo ""
echo "=========================================="
echo "  Deployment Summary"
echo "=========================================="
echo "  Environment: ${ENVIRONMENT}"
echo "  Application: ${APP_NAME}"
echo "  Timestamp:   ${TIMESTAMP}"
echo "  Dry Run:     ${DRY_RUN}"
echo "=========================================="
'''

    deploy_path = f'{SCRIPTS_DIR}/deploy.sh'
    with open(deploy_path, 'w') as f:
        f.write(deploy_script)
    os.chmod(deploy_path, 0o755)
    print(f'Created: {deploy_path}')

    # Create a basic README for the project
    readme_content = '''# Analytics Platform

A data analytics platform for processing and visualizing business metrics.

## Project Structure

```
project/
  scripts/
    deploy.sh    - Deployment automation script
  src/
    app.py       - Main application entry point
    config.py    - Configuration management
  tests/
    test_app.py  - Unit tests
```

## Deployment

```bash
# Deploy to staging
./scripts/deploy.sh --env staging

# Deploy to production
./scripts/deploy.sh --env production

# Dry run
./scripts/deploy.sh --env staging --dry-run
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)
    print(f'Created: {PROJECT_DIR}/README.md')

    # Create some source files for a realistic project
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    app_py = '''"""
Analytics Platform - Main Application
"""

import logging
from flask import Flask, jsonify

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "2.4.1"})


@app.route("/api/metrics")
def get_metrics():
    return jsonify({
        "total_users": 15234,
        "active_sessions": 892,
        "avg_response_time_ms": 145.3
    })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=8080)
'''
    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write(app_py)

    config_py = '''"""
Configuration management for the analytics platform.
"""

import os


class Config:
    DEBUG = False
    DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://localhost/analytics")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class StagingConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://staging-db/analytics")


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"
'''
    with open(f'{PROJECT_DIR}/src/config.py', 'w') as f:
        f.write(config_py)

    test_app_py = '''"""
Unit tests for the analytics platform.
"""

import unittest


class TestHealthEndpoint(unittest.TestCase):
    def test_health_returns_ok(self):
        # Placeholder test
        self.assertTrue(True)

    def test_metrics_returns_data(self):
        # Placeholder test
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
'''
    with open(f'{PROJECT_DIR}/tests/test_app.py', 'w') as f:
        f.write(test_app_py)

    # Ensure NO .vscode/launch.json exists (task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)
        print(f'Removed existing: {launch_json_path}')

    print(f'Initial workspace created at: {PROJECT_DIR}')
    print(f'Confirmed: No .vscode/launch.json exists')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
