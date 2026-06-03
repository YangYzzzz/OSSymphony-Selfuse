"""
Initial Setup: Configure logrotate for /var/log/myapp/app.log
Task ID: os_gff_021
Domain: os
"""

import os
import shlex
import subprocess
import time
from pathlib import Path


WORKDIR = '/home/user'
TASK_ID = 'os_gff_021'


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


def sudo(cmd):
    """Run a command with sudo, piping password via -S."""
    full_cmd = f"echo 'password' | sudo -S {cmd}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'SUDO FAIL: {cmd}')
        print(f'  stdout: {result.stdout.strip()}')
        print(f'  stderr: {result.stderr.strip()}')
    return result


def run(cmd):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result


def create_initial():
    # 1. Create the log directory and a realistic log file
    log_dir = '/var/log/myapp'
    log_file = f'{log_dir}/app.log'
    sudo(f'mkdir -p {log_dir}')

    # Write realistic log content
    log_lines = [
        "2026-04-01 08:00:01 INFO  [main] Application myapp v3.2.1 started",
        "2026-04-01 08:00:01 INFO  [main] Loading configuration from /etc/myapp/config.yaml",
        "2026-04-01 08:00:02 INFO  [db] Connected to PostgreSQL at localhost:5432/myapp_prod",
        "2026-04-01 08:00:02 INFO  [http] Starting HTTP server on :8080",
        "2026-04-01 08:00:03 INFO  [http] Registered 24 API endpoints",
        "2026-04-01 08:05:12 INFO  [http] GET /api/v1/users 200 12ms",
        "2026-04-01 08:05:14 INFO  [http] POST /api/v1/orders 201 45ms",
        "2026-04-01 08:10:33 WARN  [db] Slow query detected: SELECT * FROM inventory WHERE ... (320ms)",
        "2026-04-01 08:15:01 INFO  [scheduler] Running daily cleanup task",
        "2026-04-01 08:15:02 INFO  [scheduler] Removed 142 expired sessions",
        "2026-04-01 08:20:45 INFO  [http] GET /api/v1/products?page=3 200 8ms",
        "2026-04-01 08:25:19 ERROR [http] POST /api/v1/payments 500 Internal Server Error",
        "2026-04-01 08:25:19 ERROR [http] Traceback: PaymentGatewayTimeout after 30s",
        "2026-04-01 08:30:00 INFO  [metrics] CPU: 23%, Memory: 1.2GB/4GB, Goroutines: 847",
        "2026-04-01 09:00:01 INFO  [http] GET /api/v1/dashboard 200 15ms",
        "2026-04-01 09:12:44 INFO  [http] PUT /api/v1/users/5831 200 22ms",
        "2026-04-01 09:30:00 INFO  [metrics] CPU: 31%, Memory: 1.4GB/4GB, Goroutines: 1023",
        "2026-04-01 10:00:00 INFO  [metrics] CPU: 18%, Memory: 1.1GB/4GB, Goroutines: 612",
        "2026-04-01 10:15:33 WARN  [http] Rate limit exceeded for client 192.168.1.45",
        "2026-04-01 10:30:00 INFO  [metrics] CPU: 22%, Memory: 1.3GB/4GB, Goroutines: 789",
    ]

    tmp_log = '/tmp/myapp_app.log'
    Path(tmp_log).write_text('\n'.join(log_lines) + '\n')
    sudo(f'cp {tmp_log} {log_file}')
    sudo(f'chmod 644 {log_file}')

    # 2. Ensure NO logrotate config exists for myapp (clean initial state)
    sudo('rm -f /etc/logrotate.d/myapp')

    # 3. Create a fake myapp process so pidof will work
    myapp_script = '/tmp/myapp_daemon.sh'
    Path(myapp_script).write_text('#!/bin/bash\nwhile true; do sleep 3600; done\n')
    os.chmod(myapp_script, 0o755)
    sudo(f'cp {myapp_script} /usr/local/bin/myapp')
    sudo('chmod 755 /usr/local/bin/myapp')

    # Kill any existing myapp process, then start a new one
    run('pkill -9 -f /usr/local/bin/myapp 2>/dev/null; true')
    time.sleep(0.5)
    run('nohup /usr/local/bin/myapp >/dev/null 2>&1 &')
    time.sleep(1.0)

    # Verify myapp is running
    result = run('pidof myapp')
    print(f'myapp PID: {result.stdout.strip()}')

    # Verify log file exists
    result = run(f'ls -la {log_file}')
    print(f'Log file: {result.stdout.strip()}')

    # Verify no logrotate config
    result = run('test -f /etc/logrotate.d/myapp && echo "EXISTS" || echo "NOT EXISTS"')
    print(f'Logrotate config: {result.stdout.strip()}')

    print(f'\nInitial state created successfully.')

    # 4. GUI-ready: open terminal
    launch_gui('gnome-terminal --working-directory=/var/log/myapp', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
