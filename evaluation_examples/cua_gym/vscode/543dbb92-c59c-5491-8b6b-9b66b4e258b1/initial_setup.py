"""
Initial Setup: Create VSCode workspace with shell scripts, no tasks.json
Task ID: vscode_td_038
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_038'
PROJECT_DIR = f'{WORKDIR}/projects/scripting'

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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create various shell scripts for a realistic scripting workspace
    scripts = {
        'backup_db.sh': '''#!/bin/bash
# Database backup script
# Usage: ./backup_db.sh <database_name>

DB_NAME="${1:-myapp_production}"
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "Starting backup of ${DB_NAME}..."
mkdir -p "$BACKUP_DIR"

pg_dump "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed: $BACKUP_FILE"
    echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "ERROR: Backup failed for ${DB_NAME}" >&2
    exit 1
fi

# Clean up backups older than 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
echo "Old backups cleaned up."
''',
        'deploy.sh': '''#!/bin/bash
# Deployment script for staging/production
# Usage: ./deploy.sh [staging|production]

set -euo pipefail

ENV="${1:-staging}"
APP_NAME="web-dashboard"
DEPLOY_USER="deploy"
REPO_URL="git@github.com:acme-corp/${APP_NAME}.git"

case "$ENV" in
    staging)
        SERVER="staging.acme-internal.net"
        BRANCH="develop"
        ;;
    production)
        SERVER="prod-01.acme-internal.net"
        BRANCH="main"
        ;;
    *)
        echo "Unknown environment: $ENV" >&2
        exit 1
        ;;
esac

echo "=== Deploying ${APP_NAME} to ${ENV} ==="
echo "Server: ${SERVER}"
echo "Branch: ${BRANCH}"

ssh ${DEPLOY_USER}@${SERVER} <<REMOTE
    cd /opt/${APP_NAME}
    git fetch origin
    git checkout ${BRANCH}
    git pull origin ${BRANCH}
    npm ci --production
    pm2 restart ${APP_NAME}
REMOTE

echo "=== Deployment to ${ENV} complete ==="
''',
        'monitor_logs.sh': '''#!/bin/bash
# Log monitoring with keyword alerts
# Usage: ./monitor_logs.sh <logfile> [keyword]

LOG_FILE="${1:-/var/log/app/application.log}"
KEYWORD="${2:-ERROR}"
ALERT_EMAIL="ops-team@acme-corp.com"

echo "Monitoring ${LOG_FILE} for '${KEYWORD}'..."

tail -F "$LOG_FILE" | while read -r line; do
    if echo "$line" | grep -qi "$KEYWORD"; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[${TIMESTAMP}] ALERT: ${line}"
        echo "${line}" | mail -s "Log Alert: ${KEYWORD} detected" "$ALERT_EMAIL" 2>/dev/null
    fi
done
''',
        'cleanup_temp.sh': '''#!/bin/bash
# Clean up temporary files and directories
# Usage: ./cleanup_temp.sh [--dry-run]

DRY_RUN=false
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE ==="
fi

TEMP_DIRS=(
    "/tmp/app-cache"
    "/tmp/build-artifacts"
    "/var/tmp/reports"
)

TOTAL_SIZE=0

for dir in "${TEMP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        SIZE=$(du -sb "$dir" 2>/dev/null | cut -f1)
        TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
        echo "Found: $dir ($(du -sh "$dir" | cut -f1))"
        if [ "$DRY_RUN" = false ]; then
            rm -rf "$dir"
            echo "  Removed."
        fi
    fi
done

echo "Total space recovered: $((TOTAL_SIZE / 1024 / 1024)) MB"
''',
        'setup_env.sh': '''#!/bin/bash
# Development environment setup
# Usage: source ./setup_env.sh

export APP_ENV="development"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="myapp_dev"
export REDIS_URL="redis://localhost:6379/0"
export LOG_LEVEL="debug"
export API_KEY="dev-key-not-for-production"

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Python virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated."
fi

echo "Development environment configured."
echo "  APP_ENV=$APP_ENV"
echo "  DB_HOST=$DB_HOST"
echo "  DB_NAME=$DB_NAME"
''',
    }

    for filename, content in scripts.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        os.chmod(filepath, 0o755)

    # Also create a README for realism
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write('''# Scripting Utilities

A collection of shell scripts for common DevOps tasks at Acme Corp.

## Scripts

| Script | Purpose |
|--------|---------|
| backup_db.sh | PostgreSQL database backup with rotation |
| deploy.sh | Staging/production deployment |
| monitor_logs.sh | Real-time log monitoring with alerts |
| cleanup_temp.sh | Temporary file cleanup |
| setup_env.sh | Development environment configuration |

## Usage

Make sure scripts are executable:
```bash
chmod +x *.sh
```
''')

    # Ensure NO .vscode/tasks.json exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_json = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_json):
        os.remove(tasks_json)

    print(f'Initial workspace created: {PROJECT_DIR}')
    print(f'Scripts: {list(scripts.keys())}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
