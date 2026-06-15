"""
Initial Setup: Create workspace with mixed file types for .editorconfig task
Task ID: vscode_ops_054
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_054'
WORKSPACE = f'{WORKDIR}/infra'


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
    # Create workspace directory structure
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(f'{WORKSPACE}/src', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/config', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/scripts', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/docs', exist_ok=True)

    # Python files
    with open(f'{WORKSPACE}/src/app.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
"""Infrastructure monitoring application."""

import logging
import argparse
from datetime import datetime


class MonitorService:
    def __init__(self, config_path):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now()

    def check_health(self, endpoint):
        """Check health of a given service endpoint."""
        self.logger.info(f"Checking health: {endpoint}")
        return {"status": "healthy", "timestamp": self.start_time.isoformat()}

    def collect_metrics(self):
        """Collect system metrics from all monitored services."""
        metrics = {
            "cpu_usage": 42.5,
            "memory_mb": 2048,
            "disk_pct": 67.3,
            "active_connections": 156,
        }
        return metrics


def main():
    parser = argparse.ArgumentParser(description="Infrastructure Monitor")
    parser.add_argument("--config", default="config/settings.yaml")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    service = MonitorService(args.config)
    health = service.check_health("https://api.internal.example.com")
    print(f"Health check result: {health}")


if __name__ == "__main__":
    main()
''')

    with open(f'{WORKSPACE}/src/utils.py', 'w') as f:
        f.write('''"""Utility functions for infrastructure monitoring."""

import hashlib
import socket
from pathlib import Path


def get_hostname():
    return socket.gethostname()


def hash_file(filepath):
    """Generate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def ensure_directory(path):
    """Create directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path
''')

    # Shell scripts
    with open(f'{WORKSPACE}/scripts/deploy.sh', 'w') as f:
        f.write('''#!/bin/bash
# Deployment script for infrastructure services

set -euo pipefail

ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"
DEPLOY_DIR="/opt/infra/releases"

echo "=== Deploying version $VERSION to $ENVIRONMENT ==="

if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir -p "$DEPLOY_DIR"
    echo "Created release directory"
fi

echo "Pulling container images..."
# docker pull registry.internal.example.com/monitor:$VERSION

echo "Running database migrations..."
# python3 manage.py migrate

echo "Restarting services..."
# systemctl restart monitor-api
# systemctl restart monitor-worker

echo "Deployment complete at $(date)"
''')

    with open(f'{WORKSPACE}/scripts/backup.sh', 'w') as f:
        f.write('''#!/bin/bash
# Automated backup script

BACKUP_DIR="/var/backups/infra"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_HOST="db.internal.example.com"

echo "Starting backup at $TIMESTAMP"

pg_dump -h "$DB_HOST" -U monitor -d infra_db > "$BACKUP_DIR/db_$TIMESTAMP.sql"

tar czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" /etc/infra/

find "$BACKUP_DIR" -name "*.sql" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed successfully"
''')

    # YAML config files
    with open(f'{WORKSPACE}/config/settings.yaml', 'w') as f:
        f.write('''---
application:
  name: infra-monitor
  version: 2.4.1
  environment: production

database:
  host: db.internal.example.com
  port: 5432
  name: infra_db
  pool_size: 10
  timeout: 30

monitoring:
  check_interval: 60
  endpoints:
    - name: api-gateway
      url: https://api.internal.example.com/health
      timeout: 5
    - name: auth-service
      url: https://auth.internal.example.com/health
      timeout: 10
    - name: storage-service
      url: https://storage.internal.example.com/health
      timeout: 15

alerts:
  slack_webhook: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
  email_recipients:
    - ops-team@example.com
    - platform-lead@example.com
  severity_threshold: warning
''')

    with open(f'{WORKSPACE}/config/docker-compose.yml', 'w') as f:
        f.write('''version: "3.8"
services:
  monitor-api:
    image: registry.internal.example.com/monitor:latest
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: unless-stopped

  monitor-worker:
    image: registry.internal.example.com/monitor-worker:latest
    environment:
      - DB_HOST=db
      - QUEUE_URL=redis://cache:6379/1
    depends_on:
      - db
      - cache

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=infra_db
      - POSTGRES_USER=monitor
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
''')

    # JSON config
    with open(f'{WORKSPACE}/config/alerts.json', 'w') as f:
        f.write('''{
  "rules": [
    {
      "name": "high_cpu",
      "condition": "cpu_usage > 90",
      "severity": "critical",
      "cooldown_minutes": 15,
      "channels": ["slack", "email"]
    },
    {
      "name": "disk_space_low",
      "condition": "disk_pct > 85",
      "severity": "warning",
      "cooldown_minutes": 30,
      "channels": ["slack"]
    },
    {
      "name": "service_down",
      "condition": "health_check == false",
      "severity": "critical",
      "cooldown_minutes": 5,
      "channels": ["slack", "email", "pagerduty"]
    }
  ],
  "default_channel": "slack",
  "escalation_timeout_minutes": 30
}
''')

    # Documentation
    with open(f'{WORKSPACE}/docs/runbook.md', 'w') as f:
        f.write('''# Infrastructure Runbook

## Service Overview

The infra-monitor stack consists of three main components:

1. **API Gateway** - Handles incoming health check requests
2. **Worker Service** - Processes metrics and alert evaluation
3. **Database** - PostgreSQL for persistent state storage

## Common Operations

### Restart Services
```bash
./scripts/deploy.sh production latest
```

### Check Logs
```bash
journalctl -u monitor-api -f --since "1 hour ago"
```

### Database Backup
```bash
./scripts/backup.sh
```

## Incident Response

| Severity | Response Time | Escalation |
|----------|--------------|------------|
| Critical | 5 minutes    | Immediate  |
| Warning  | 30 minutes   | 1 hour     |
| Info     | Next business day | None  |
''')

    # Ensure no .editorconfig exists (negative constraint)
    editorconfig_path = f'{WORKSPACE}/.editorconfig'
    if os.path.exists(editorconfig_path):
        os.remove(editorconfig_path)

    print(f'Workspace created: {WORKSPACE}')
    print(f'Files: Python, Shell, YAML, JSON, Markdown')

    # Install EditorConfig extension
    subprocess.run(['code', '--install-extension', 'EditorConfig.EditorConfig'],
                   capture_output=True, text=True, timeout=30)
    print('EditorConfig extension installed')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
