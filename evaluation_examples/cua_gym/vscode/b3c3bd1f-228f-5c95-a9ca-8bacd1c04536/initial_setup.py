"""
Initial Setup: Set up SSH config with existing hosts, VSCode open with Remote-SSH
Task ID: vscode_rrt_012
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_012'
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
    # Ensure .ssh directory exists with proper permissions
    os.makedirs(SSH_DIR, mode=0o700, exist_ok=True)

    # Create ~/.ssh/config with two existing host entries (NO secure-server)
    ssh_config_content = """\
# SSH Configuration File

Host dev-gateway
    HostName gateway.devops.internal
    Port 22
    User deploy
    IdentityFile ~/.ssh/id_ed25519_deploy
    ForwardAgent yes

Host staging-db
    HostName db-staging.corp.net
    Port 22
    User dbadmin
    IdentityFile ~/.ssh/id_rsa_staging
    StrictHostKeyChecking no
    ServerAliveInterval 60
"""

    with open(SSH_CONFIG, 'w') as f:
        f.write(ssh_config_content)
    os.chmod(SSH_CONFIG, 0o600)
    print(f'SSH config created: {SSH_CONFIG}')

    # Also create dummy key files so config references are realistic
    for keyfile in ['id_ed25519_deploy', 'id_rsa_staging']:
        keypath = os.path.join(SSH_DIR, keyfile)
        if not os.path.exists(keypath):
            with open(keypath, 'w') as f:
                f.write(f'# Placeholder key: {keyfile}\n')
            os.chmod(keypath, 0o600)

    # Install Remote-SSH extension if not already present
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'ms-vscode-remote.remote-ssh' not in result.stdout.lower():
            subprocess.run(
                ['code', '--install-extension', 'ms-vscode-remote.remote-ssh'],
                capture_output=True, text=True, timeout=60
            )
            print('Installed Remote-SSH extension')
        else:
            print('Remote-SSH extension already installed')
    except Exception as e:
        print(f'Extension check/install note: {e}')

    # Launch VSCode and open the SSH config file
    launch_gui(f'code "{SSH_CONFIG}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with SSH config and DISPLAY=:0')


create_initial()
