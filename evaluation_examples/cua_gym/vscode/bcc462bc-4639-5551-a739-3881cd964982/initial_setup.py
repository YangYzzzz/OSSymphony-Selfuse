"""
Initial Setup: SSH config with production host entries for VSCode Remote-SSH task
Task ID: vscode_rrt_022
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_022'
SSH_DIR = os.path.join(WORKDIR, '.ssh')
SSH_CONFIG = os.path.join(SSH_DIR, 'config')
TEST_KEY = os.path.join(SSH_DIR, 'test_key')


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
    os.makedirs(SSH_DIR, exist_ok=True)
    os.chmod(SSH_DIR, 0o700)

    # Create existing production SSH config entries (NO test-env entry)
    ssh_config_content = """\
# Production SSH Configuration
# Last updated: 2025-11-20

Host prod-web-01
    HostName 10.0.1.50
    User deploy
    Port 22
    IdentityFile ~/.ssh/prod_key
    ForwardAgent yes

Host prod-db-master
    HostName 10.0.2.100
    User dbadmin
    Port 2222
    IdentityFile ~/.ssh/prod_key
    StrictHostKeyChecking yes

Host staging-app
    HostName 172.16.0.25
    User staging
    IdentityFile ~/.ssh/staging_key
    ProxyJump prod-web-01

Host bastion
    HostName 203.0.113.10
    User jumpuser
    Port 22
    IdentityFile ~/.ssh/bastion_key
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
"""
    with open(SSH_CONFIG, 'w') as f:
        f.write(ssh_config_content)
    os.chmod(SSH_CONFIG, 0o600)
    print(f'SSH config created: {SSH_CONFIG}')

    # Create dummy test key file (must exist per task context)
    test_key_content = """\
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBGaWxsZXIga2V5IGZvciB0ZXN0IGVudmlyb25tZW50AAAAAA==
-----END OPENSSH PRIVATE KEY-----
"""
    with open(TEST_KEY, 'w') as f:
        f.write(test_key_content)
    os.chmod(TEST_KEY, 0o600)
    print(f'Test key created: {TEST_KEY}')

    # Also create dummy keys referenced in the config so the environment looks realistic
    for keyname in ['prod_key', 'staging_key', 'bastion_key']:
        keypath = os.path.join(SSH_DIR, keyname)
        if not os.path.exists(keypath):
            with open(keypath, 'w') as f:
                f.write(f'# placeholder key: {keyname}\n')
            os.chmod(keypath, 0o600)

    # Launch VSCode with the SSH config file open
    launch_gui(f'code "{SSH_CONFIG}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with SSH config on DISPLAY=:0')


create_initial()
