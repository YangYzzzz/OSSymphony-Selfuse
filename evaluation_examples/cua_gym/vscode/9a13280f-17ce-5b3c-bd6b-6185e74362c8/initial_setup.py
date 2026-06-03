"""
Initial Setup: Configure SSH multiplexing - pre-task state
Task ID: vscode_rrt_016
Domain: vscode

Creates ~/.ssh/config with three host entries but NO wildcard Host * entry.
Does NOT create ~/.ssh/sockets/ directory.
Opens VSCode with the SSH config file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
SSH_DIR = os.path.join(WORKDIR, '.ssh')
SSH_CONFIG = os.path.join(SSH_DIR, 'config')


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
    # Ensure .ssh directory exists with correct permissions
    os.makedirs(SSH_DIR, exist_ok=True)
    os.chmod(SSH_DIR, 0o700)

    # Create SSH config with three realistic host entries, NO wildcard Host *
    config_content = """\
# SSH Configuration File
# Generated for development environment

Host dev-server
    HostName 192.168.10.50
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519_dev
    ForwardAgent yes

Host staging-bastion
    HostName 10.200.1.5
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_rsa_staging
    ProxyJump none
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host prod-db
    HostName db.internal.example.com
    User dbadmin
    Port 22
    IdentityFile ~/.ssh/id_ed25519_prod
    LocalForward 5432 localhost:5432
    StrictHostKeyChecking yes
"""

    with open(SSH_CONFIG, 'w') as f:
        f.write(config_content)
    os.chmod(SSH_CONFIG, 0o600)

    print(f'Initial SSH config created: {SSH_CONFIG}')

    # Verify no sockets directory exists (remove if somehow present)
    sockets_dir = os.path.join(SSH_DIR, 'sockets')
    if os.path.exists(sockets_dir):
        import shutil
        shutil.rmtree(sockets_dir)

    # Open VSCode with the SSH config file
    launch_gui(f'code "{SSH_CONFIG}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/.ssh/config on DISPLAY=:0')


create_initial()
