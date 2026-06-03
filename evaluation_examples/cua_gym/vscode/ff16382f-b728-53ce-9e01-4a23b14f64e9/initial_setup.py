"""
Initial Setup: Configure VSCode terminal with automatic shell command
Task ID: vscode_rrt_087
Domain: vscode

Creates a workspace with sample files and opens VSCode.
No terminal profile configuration is set -- that is the task for the agent.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_087'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'workspace')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # Create a workspace directory with sample project files
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a sample Python file
    main_py = os.path.join(PROJECT_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Server Health Monitor - Checks system metrics and reports status.
"""

import os
import platform
import datetime


def get_system_info():
    """Gather basic system information."""
    info = {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }
    return info


def get_uptime():
    """Read system uptime from /proc/uptime."""
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except FileNotFoundError:
        return "N/A"


def check_disk_usage(path="/"):
    """Check disk usage for a given path."""
    statvfs = os.statvfs(path)
    total = statvfs.f_frsize * statvfs.f_blocks
    free = statvfs.f_frsize * statvfs.f_bfree
    used = total - free
    percent = (used / total) * 100 if total > 0 else 0
    return {
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "percent_used": round(percent, 1),
    }


def main():
    print("=" * 50)
    print("  Server Health Monitor")
    print(f"  Report generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("\\nSystem Information:")
    for key, value in get_system_info().items():
        print(f"  {key}: {value}")

    print(f"\\nUptime: {get_uptime()}")

    print("\\nDisk Usage (/):")
    disk = check_disk_usage()
    for key, value in disk.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
''')

    # Create a README
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''# Server Health Monitor

A lightweight Python utility to check system health metrics.

## Features
- System information gathering (hostname, OS, architecture)
- Uptime monitoring
- Disk usage analysis

## Usage
```bash
python3 main.py
```

## Requirements
- Python 3.6+
- Linux environment (uses /proc filesystem)
''')

    # Create a config file
    config_file = os.path.join(PROJECT_DIR, 'config.json')
    with open(config_file, 'w') as f:
        json.dump({
            "monitor": {
                "interval_seconds": 300,
                "alerts_enabled": True,
                "disk_threshold_percent": 85,
                "log_file": "/var/log/health_monitor.log"
            },
            "notifications": {
                "email": "ops-team@acme-corp.com",
                "slack_webhook": ""
            }
        }, f, indent=4)

    # Ensure VSCode settings directory exists, load existing settings
    # and make sure there is NO terminal profile config (that's the task)
    settings = load_settings()
    # Remove any existing terminal profile config if present
    settings.pop('terminal.integrated.profiles.linux', None)
    save_settings(settings)
    print(f'Settings cleaned: no terminal profiles configured')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print(f'Initial setup complete: workspace at {PROJECT_DIR}')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
