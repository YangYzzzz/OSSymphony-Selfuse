"""
Initial Setup: Prometheus alerting pipeline setup
Task ID: os_gff_074
Domain: os
"""

import os
import shlex
import subprocess
import time
import tempfile
from pathlib import Path

SUDO_PASS = 'password'

def sudo_run(cmd):
    """Run a command with sudo, piping in the password."""
    full_cmd = f"echo '{SUDO_PASS}' | sudo -S {cmd}"
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

def sudo_write(path, content):
    """Write content to a file that requires sudo access."""
    # Write to a temp file first, then sudo move it
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False)
    tmp.write(content)
    tmp.close()
    sudo_run(f"cp {tmp.name} {path}")
    sudo_run(f"chmod 644 {path}")
    os.unlink(tmp.name)

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
    # 1. Create directory structure for Prometheus
    sudo_run("mkdir -p /etc/prometheus")
    sudo_run("mkdir -p /etc/alertmanager")
    # Do NOT create /etc/prometheus/alerts/ — that's what the task asks the agent to do

    # 2. Write initial Prometheus config (NO rule_files for alerts)
    prometheus_yml = """\
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
"""
    sudo_write("/etc/prometheus/prometheus.yml", prometheus_yml)
    print("Created /etc/prometheus/prometheus.yml")

    # 3. Write PagerDuty integration key
    sudo_write("/etc/prometheus/pagerduty_key.txt", "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
    print("Created /etc/prometheus/pagerduty_key.txt")

    # 4. Write minimal/default Alertmanager config (NO PagerDuty, NO email, NO repeat_interval: 15m)
    alertmanager_yml = """\
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'

receivers:
  - name: 'default'
"""
    sudo_write("/etc/alertmanager/alertmanager.yml", alertmanager_yml)
    print("Created /etc/alertmanager/alertmanager.yml")

    # 5. Set ownership to user for easier editing
    sudo_run("chown -R user:user /etc/prometheus")
    sudo_run("chown -R user:user /etc/alertmanager")

    # 6. Install promtool (Prometheus) so the agent can run promtool check config
    result = sudo_run("which promtool")
    if 'promtool' not in result.stdout:
        print("Installing Prometheus (for promtool)...")
        sudo_run("apt-get update -qq")
        sudo_run("apt-get install -y prometheus 2>/dev/null || true")
        result2 = sudo_run("which promtool")
        if 'promtool' not in result2.stdout:
            cmds = [
                "cd /tmp && wget -q https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz",
                "cd /tmp && tar xzf prometheus-2.45.0.linux-amd64.tar.gz",
                "cp /tmp/prometheus-2.45.0.linux-amd64/promtool /usr/local/bin/",
                "chmod +x /usr/local/bin/promtool",
            ]
            for c in cmds:
                sudo_run(c)
            print("Installed promtool from binary release")
    else:
        print("promtool already available")

    # 7. Verify configs were written
    result = subprocess.run(["cat", "/etc/prometheus/prometheus.yml"], capture_output=True, text=True)
    print(f"Prometheus config length: {len(result.stdout)} bytes")
    result = subprocess.run(["cat", "/etc/alertmanager/alertmanager.yml"], capture_output=True, text=True)
    print(f"Alertmanager config length: {len(result.stdout)} bytes")

    # 8. Open a terminal showing the current state for the agent
    launch_gui('gnome-terminal -- bash -c "echo Prometheus Alerting Pipeline Setup; echo =================================; echo; echo Current Prometheus config:; cat /etc/prometheus/prometheus.yml; echo; echo Current Alertmanager config:; cat /etc/alertmanager/alertmanager.yml; echo; echo PagerDuty key:; cat /etc/prometheus/pagerduty_key.txt; echo; exec bash"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
