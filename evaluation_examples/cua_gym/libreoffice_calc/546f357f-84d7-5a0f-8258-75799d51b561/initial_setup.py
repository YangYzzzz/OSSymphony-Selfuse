"""
Initial Setup: Set up Nginx as a load balancer for three upstream application servers
Task ID: os_adm_037
Domain: os (nginx configuration)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_037'
SUDO_PASS = 'password'


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


def sudo_run(cmd_str):
    """Run a command with sudo using password via stdin."""
    result = subprocess.run(
        f"echo '{SUDO_PASS}' | sudo -S {cmd_str}",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        # Filter out the password prompt line
        for line in result.stderr.strip().split('\n'):
            if '[sudo]' not in line:
                print(line)
    return result


def create_initial():
    # 1. Install nginx
    print("Installing nginx...")
    sudo_run("apt-get update -qq")
    sudo_run("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq nginx")

    # 2. Remove any existing loadbalancer config (ensure clean initial state)
    sudo_run("rm -f /etc/nginx/sites-available/loadbalancer")
    sudo_run("rm -f /etc/nginx/sites-enabled/loadbalancer")

    # 3. Ensure default nginx config is present and nginx is running
    sudo_run("systemctl enable nginx")
    sudo_run("systemctl start nginx")

    # 4. Verify nginx is installed and running
    result = sudo_run("nginx -t")
    print(f"Nginx config test: returncode={result.returncode}")
    sudo_run("nginx -v")

    # 5. Create a helper README on the desktop so the agent has context
    os.makedirs(f"{WORKDIR}/Desktop", exist_ok=True)
    Path(f"{WORKDIR}/Desktop/server_info.txt").write_text(
        "Application Server Infrastructure\n"
        "==================================\n\n"
        "Backend Servers:\n"
        "  - app-server-1: 10.0.1.10:8080\n"
        "  - app-server-2: 10.0.1.11:8080\n"
        "  - app-server-3: 10.0.1.12:8080\n\n"
        "Status: All three servers are running and healthy.\n"
        "Load Balancer: Not yet configured.\n\n"
        "Notes:\n"
        "  - The application uses session-based features requiring sticky connections.\n"
        "  - Health check timeouts should be configured for reliability.\n"
    )

    # 6. Verify no loadbalancer config exists
    lb_path = "/etc/nginx/sites-available/loadbalancer"
    if os.path.exists(lb_path):
        print(f"ERROR: {lb_path} still exists!")
    else:
        print(f"Confirmed: {lb_path} does not exist (clean initial state)")

    print(f"Initial state prepared successfully")

    # 7. Launch a terminal so the agent can start working
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
