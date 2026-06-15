"""
Initial Setup: Create sysadmin workspace with scripts and SSH config, open in VSCode.
Task ID: vscode_td_026
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_026'
SCRIPTS_DIR = os.path.join(WORKDIR, 'sysadmin', 'scripts')
SSH_DIR = os.path.join(WORKDIR, '.ssh')


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
    # Create the sysadmin/scripts directory
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Create some realistic sysadmin scripts
    with open(os.path.join(SCRIPTS_DIR, 'backup_logs.sh'), 'w') as f:
        f.write("""#!/bin/bash
# Backup server logs to /backup/logs
# Run daily via cron at 02:00 UTC

BACKUP_DIR="/backup/logs/$(date +%Y%m%d)"
SERVERS=("prod-server" "staging-server" "dev-server")

mkdir -p "$BACKUP_DIR"

for server in "${SERVERS[@]}"; do
    echo "[$(date)] Backing up logs from $server..."
    scp "$server:/var/log/syslog" "$BACKUP_DIR/${server}_syslog.log"
    scp "$server:/var/log/auth.log" "$BACKUP_DIR/${server}_auth.log"
done

echo "[$(date)] Log backup complete."
""")

    with open(os.path.join(SCRIPTS_DIR, 'check_services.sh'), 'w') as f:
        f.write("""#!/bin/bash
# Check critical services across all servers

SERVICES=("nginx" "postgresql" "redis-server" "docker")

check_service() {
    local server=$1
    local service=$2
    status=$(ssh "$server" "systemctl is-active $service" 2>/dev/null)
    if [ "$status" = "active" ]; then
        echo "  [OK] $service"
    else
        echo "  [FAIL] $service ($status)"
    fi
}

for server in prod-server staging-server; do
    echo "=== $server ==="
    for svc in "${SERVICES[@]}"; do
        check_service "$server" "$svc"
    done
done
""")

    with open(os.path.join(SCRIPTS_DIR, 'deploy.sh'), 'w') as f:
        f.write("""#!/bin/bash
# Deploy application to staging or production
# Usage: ./deploy.sh [staging|production] [version]

ENV=${1:-staging}
VERSION=${2:-latest}

if [ "$ENV" = "production" ]; then
    SERVER="prod-server"
    echo "WARNING: Deploying to PRODUCTION"
    read -p "Are you sure? (y/N) " confirm
    [ "$confirm" != "y" ] && exit 1
else
    SERVER="staging-server"
fi

echo "Deploying version $VERSION to $SERVER..."
ssh "$SERVER" "cd /opt/app && git pull origin main && git checkout $VERSION"
ssh "$SERVER" "systemctl restart app-service"
echo "Deploy complete. Verifying..."
ssh "$SERVER" "curl -s http://localhost:8080/health"
""")

    with open(os.path.join(SCRIPTS_DIR, 'monitor_resources.py'), 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Monitor server resource usage and alert on thresholds.\"\"\"

import subprocess
import sys

THRESHOLDS = {
    'cpu_percent': 85.0,
    'memory_percent': 90.0,
    'disk_percent': 95.0,
}

SERVERS = ['prod-server', 'staging-server']


def get_resource_usage(server):
    \"\"\"Get CPU, memory, and disk usage from remote server.\"\"\"
    try:
        cpu = subprocess.check_output(
            ['ssh', server, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'"],
            text=True, timeout=10
        ).strip()
        mem = subprocess.check_output(
            ['ssh', server, "free | awk '/Mem:/{printf(\"%.1f\", $3/$2*100)}'"],
            text=True, timeout=10
        ).strip()
        disk = subprocess.check_output(
            ['ssh', server, "df -h / | awk 'NR==2{print $5}' | tr -d '%'"],
            text=True, timeout=10
        ).strip()
        return float(cpu), float(mem), float(disk)
    except Exception as e:
        print(f"Error checking {server}: {e}")
        return None, None, None


def main():
    alerts = []
    for server in SERVERS:
        cpu, mem, disk = get_resource_usage(server)
        if cpu is not None:
            print(f"{server}: CPU={cpu}%, MEM={mem}%, DISK={disk}%")
            if cpu > THRESHOLDS['cpu_percent']:
                alerts.append(f"HIGH CPU on {server}: {cpu}%")
            if mem > THRESHOLDS['memory_percent']:
                alerts.append(f"HIGH MEM on {server}: {mem}%")
            if disk > THRESHOLDS['disk_percent']:
                alerts.append(f"HIGH DISK on {server}: {disk}%")

    if alerts:
        print("\\n--- ALERTS ---")
        for alert in alerts:
            print(f"  !! {alert}")
        sys.exit(1)
    else:
        print("\\nAll systems nominal.")


if __name__ == '__main__':
    main()
""")

    # Make shell scripts executable
    for script in ['backup_logs.sh', 'check_services.sh', 'deploy.sh']:
        os.chmod(os.path.join(SCRIPTS_DIR, script), 0o755)

    # Set up SSH config with prod-server and staging-server
    os.makedirs(SSH_DIR, exist_ok=True)
    ssh_config_path = os.path.join(SSH_DIR, 'config')
    with open(ssh_config_path, 'w') as f:
        f.write("""Host prod-server
    HostName 10.0.1.50
    User deploy
    IdentityFile ~/.ssh/prod_key
    Port 22
    StrictHostKeyChecking no

Host staging-server
    HostName 10.0.2.30
    User deploy
    IdentityFile ~/.ssh/staging_key
    Port 22
    StrictHostKeyChecking no

Host dev-server
    HostName 10.0.3.10
    User developer
    IdentityFile ~/.ssh/dev_key
    Port 22
    StrictHostKeyChecking no
""")
    os.chmod(ssh_config_path, 0o600)

    # Ensure NO .vscode folder exists (task requires creating it)
    vscode_dir = os.path.join(SCRIPTS_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial workspace created: {SCRIPTS_DIR}')
    print(f'SSH config created: {ssh_config_path}')
    print(f'No .vscode folder present (as required by task)')

    # Launch VSCode with the sysadmin/scripts folder
    launch_gui(f'code "{SCRIPTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
