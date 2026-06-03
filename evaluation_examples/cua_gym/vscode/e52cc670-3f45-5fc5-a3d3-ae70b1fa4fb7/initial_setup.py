"""
Initial Setup: Configure VSCode Remote-SSH settings
Task ID: vscode_rrt_007
Domain: vscode

Creates ~/.ssh/work_config with realistic host entries.
VSCode settings remain at defaults (no remote.SSH.configFile or connectTimeout).
Launches VSCode.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_007'
SSH_DIR = os.path.join(WORKDIR, '.ssh')
WORK_CONFIG = os.path.join(SSH_DIR, 'work_config')
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


def create_ssh_work_config():
    """Create ~/.ssh/work_config with realistic host entries."""
    os.makedirs(SSH_DIR, exist_ok=True)

    config_content = """\
# Work SSH Configuration

Host dev-server
    HostName 10.200.1.50
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    ForwardAgent yes

Host staging-web
    HostName 10.200.2.101
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_rsa_staging
    StrictHostKeyChecking no

Host prod-db-primary
    HostName 10.200.3.10
    User dbadmin
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    LocalForward 5432 localhost:5432

Host ci-runner
    HostName 10.200.4.200
    User ci
    Port 22
    IdentityFile ~/.ssh/id_rsa_ci
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host analytics-gpu
    HostName 10.200.5.80
    User mlops
    Port 22
    IdentityFile ~/.ssh/id_ed25519_work
    ForwardX11 yes
"""

    with open(WORK_CONFIG, 'w') as f:
        f.write(config_content)
    os.chmod(WORK_CONFIG, 0o600)
    print(f'Created SSH work config: {WORK_CONFIG}')


def ensure_default_settings():
    """Ensure VSCode settings exist but do NOT contain remote.SSH settings."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any remote.SSH settings if they happen to exist
    settings.pop('remote.SSH.configFile', None)
    settings.pop('remote.SSH.connectTimeout', None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings cleaned (no remote.SSH overrides): {SETTINGS_PATH}')


def main():
    create_ssh_work_config()
    ensure_default_settings()

    # Launch VSCode
    launch_gui('code "/home/user"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
