"""
Initial Setup: Configure VSCode for shell script linting
Task ID: vscode_cm_062
Domain: vscode

Creates a deployment project with shell scripts containing common shellcheck
warnings (SC2086, SC2164, SC2006). Opens VSCode with the deploy.sh file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_cm_062'
PROJECT_DIR = f'{WORKDIR}/projects/deployment'
SCRIPTS_DIR = f'{PROJECT_DIR}/scripts'
DEPLOY_SH = f'{PROJECT_DIR}/deploy.sh'


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
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/configs', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/logs', exist_ok=True)

    # --- deploy.sh: main deployment script with shellcheck violations ---
    # Contains: SC2086 (unquoted variables), SC2164 (cd without ||), SC2006 (backticks)
    deploy_content = '''#!/bin/bash
# Deployment script for production services
# Maintained by: DevOps Team
# Last updated: 2025-11-20

set -e

APP_NAME="inventory-service"
DEPLOY_DIR="/opt/deployments/$APP_NAME"
LOG_DIR="/var/log/$APP_NAME"
BACKUP_DIR="/opt/backups"
CONFIG_FILE="configs/production.yaml"
VERSION_TAG="v3.2.1"

echo "========================================="
echo "  Deploying $APP_NAME ($VERSION_TAG)"
echo "========================================="

# SC2006: Using backticks instead of $()
TIMESTAMP=`date +%Y%m%d_%H%M%S`
CURRENT_USER=`whoami`
HOSTNAME_STR=`hostname`

echo "Deployment started by $CURRENT_USER on $HOSTNAME_STR at $TIMESTAMP"

# Create backup of current deployment
echo "Creating backup..."
# SC2086: Unquoted variables (word splitting risk)
mkdir -p $BACKUP_DIR/$APP_NAME
cp -r $DEPLOY_DIR/* $BACKUP_DIR/$APP_NAME/$TIMESTAMP/ 2>/dev/null || true

# SC2164: cd without error handling
cd $DEPLOY_DIR

echo "Pulling latest changes..."
git fetch origin main
git checkout $VERSION_TAG

# SC2086: More unquoted variables
echo "Installing dependencies..."
if [ -f $CONFIG_FILE ]; then
    echo "Loading configuration from $CONFIG_FILE"
    source $CONFIG_FILE
fi

# SC2164: Another cd without error handling
cd $LOG_DIR

# SC2006: More backtick usage
DISK_USAGE=`df -h / | tail -1 | awk '{print $5}'`
MEM_FREE=`free -m | grep Mem | awk '{print $4}'`

echo "System status - Disk: $DISK_USAGE, Free memory: ${MEM_FREE}MB"

# Restart the service
echo "Restarting $APP_NAME..."
systemctl restart $APP_NAME || echo "Warning: Service restart failed"

# SC2086: Unquoted variable in test
if [ -d $LOG_DIR/archive ]; then
    echo "Cleaning old logs..."
    find $LOG_DIR/archive -name "*.log" -mtime +30 -delete
fi

# SC2006: Backtick in variable assignment
END_TIME=`date +%H:%M:%S`
echo "Deployment completed at $END_TIME"
echo "========================================="
'''
    with open(DEPLOY_SH, 'w') as f:
        f.write(deploy_content)
    os.chmod(DEPLOY_SH, 0o755)

    # --- scripts/health_check.sh: additional script in scripts/ directory ---
    health_check_content = '''#!/bin/bash
# Health check script for deployed services

SERVICE_NAME="inventory-service"
HEALTH_ENDPOINT="http://localhost:8080/health"
RETRY_COUNT=5
RETRY_DELAY=3

echo "Running health check for $SERVICE_NAME..."

for i in $(seq 1 $RETRY_COUNT); do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_ENDPOINT)
    if [ "$RESPONSE" = "200" ]; then
        echo "Health check passed on attempt $i"
        exit 0
    fi
    echo "Attempt $i failed (HTTP $RESPONSE), retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
done

echo "Health check failed after $RETRY_COUNT attempts"
exit 1
'''
    with open(f'{SCRIPTS_DIR}/health_check.sh', 'w') as f:
        f.write(health_check_content)
    os.chmod(f'{SCRIPTS_DIR}/health_check.sh', 0o755)

    # --- scripts/cleanup.sh: another script in scripts/ ---
    cleanup_content = '''#!/bin/bash
# Cleanup script for old deployment artifacts

RETENTION_DAYS=30
BACKUP_ROOT="/opt/backups"
LOG_ROOT="/var/log"

echo "Starting cleanup (retention: ${RETENTION_DAYS} days)..."

# Remove old backup directories
if [ -d "$BACKUP_ROOT" ]; then
    find "$BACKUP_ROOT" -maxdepth 2 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} + 2>/dev/null
    echo "Old backups cleaned"
fi

# Compress and archive old logs
if [ -d "$LOG_ROOT" ]; then
    find "$LOG_ROOT" -name "*.log" -mtime +7 -exec gzip {} +
    echo "Old logs compressed"
fi

echo "Cleanup complete"
'''
    with open(f'{SCRIPTS_DIR}/cleanup.sh', 'w') as f:
        f.write(cleanup_content)
    os.chmod(f'{SCRIPTS_DIR}/cleanup.sh', 0o755)

    # --- configs/production.yaml: config file for realism ---
    config_content = '''# Production Configuration
app:
  name: inventory-service
  port: 8080
  workers: 4

database:
  host: db-prod-01.internal
  port: 5432
  name: inventory_prod
  pool_size: 20

logging:
  level: INFO
  format: json
  output: /var/log/inventory-service/app.log

monitoring:
  enabled: true
  metrics_port: 9090
  health_endpoint: /health
'''
    with open(f'{PROJECT_DIR}/configs/production.yaml', 'w') as f:
        f.write(config_content)

    # --- README.md for the project ---
    readme_content = '''# Deployment Scripts

Scripts for managing the inventory-service deployment pipeline.

## Structure
- `deploy.sh` — Main deployment script
- `scripts/` — Utility scripts (health checks, cleanup)
- `configs/` — Environment configuration files
- `logs/` — Deployment log output

## Usage
```bash
./deploy.sh
./scripts/health_check.sh
./scripts/cleanup.sh
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Deploy script: {DEPLOY_SH}')

    # Open VSCode with the deploy.sh file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{DEPLOY_SH}"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
